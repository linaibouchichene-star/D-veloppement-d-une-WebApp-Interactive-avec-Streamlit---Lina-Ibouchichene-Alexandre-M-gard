import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
import plotly.express as px
import requests
import re

# --- Initialisation du stockage de l’historique ---
if "historique_dons" not in st.session_state:
    st.session_state["historique_dons"] = []

def user_login():
    """Système simple et propre de connexion utilisateur avec vérification e-mail"""
    with st.sidebar.expander("🔐 Connexion", expanded=True):
        if "user_email" not in st.session_state:
            st.session_state["user_email"] = None

        if not st.session_state["user_email"]:
            email_input = st.text_input(
                "Adresse e-mail :",
                placeholder="ex: nom@exemple.com"
            )
            login_button = st.button("Se connecter", use_container_width=True)

            if login_button:
                if "@" in email_input and "." in email_input:
                    st.session_state["user_email"] = email_input
                    st.success(f"Bienvenue {email_input}")
                    st.rerun()  # recharge proprement la page
                else:
                    st.error("Adresse e-mail invalide.")
        else:
            st.success(f"Connecté : {st.session_state['user_email']}")
            if st.button("Se déconnecter", use_container_width=True):
                st.session_state["user_email"] = None
                st.rerun()


# ---------------------------
# FONCTIONS DE BASE
# ---------------------------

@st.cache_data
def load_data(csv_path):
    """Charge le fichier CSV des ONG"""
    return pd.read_csv(csv_path, sep=";")


def filter_data(df, country, domains, search_name):
    """Filtre les données selon pays d'intervention, domaine et recherche"""
    filtered = df.copy()

    # 🔹 Filtrage par pays d'intervention
    if country != "Tous":
        filtered = filtered[filtered["pays_intervention"].str.contains(country, case=False, na=False)]

    # 🔹 Filtrage par domaine
    if domains:
        filtered = filtered[filtered["domaine"].isin(domains)]

    # 🔹 Filtrage par nom d'association
    if search_name:
        filtered = filtered[filtered["nom"].str.contains(search_name, case=False, na=False)]

    return filtered


def create_map(df):
    """Crée une carte Folium colorée selon l'IDH"""

    # Dictionnaire IDH simplifié (ONU 2023)
    idh_data = {
        "Iceland": 0.972, "Norway": 0.970, "Switzerland": 0.970, "Denmark": 0.962, "Germany": 0.959, "Sweden": 0.959, "Australia": 0.958, "Hong Kong, China (SAR)": 0.955, "Netherlands": 0.955, "Belgium": 0.951, "Ireland": 0.949, "Finland": 0.948, "Singapore": 0.946, "United Kingdom": 0.946, "United Arab Emirates": 0.940, "Canada": 0.939, "Liechtenstein": 0.938, "New Zealand": 0.938, "United States of America": 0.938, "South Korea": 0.937, "Slovenia": 0.931, "Austria": 0.930, "Japan": 0.925, "Malta": 0.924, "Luxembourg": 0.922, "France": 0.920, "Israel": 0.919, "Spain": 0.918, "Czechia": 0.915, "Italy": 0.915, "San Marino": 0.915, "Andorra": 0.913, "Cyprus": 0.913, "Greece": 0.908, "Poland": 0.906, "Estonia": 0.905, "Saudi Arabia": 0.900, "Bahrain": 0.899, "Lithuania": 0.895, "Portugal": 0.890, "Croatia": 0.889, "Latvia": 0.889, "Qatar": 0.886, "Slovakia": 0.880, "Chile": 0.878, "Hungary": 0.870, "Argentina": 0.865, "Montenegro": 0.862, "Uruguay": 0.862, "Oman": 0.858, "Türkiye": 0.853, "Kuwait": 0.852, "Antigua and Barbuda": 0.851, "Seychelles": 0.848, "Bulgaria": 0.845, "Romania": 0.845, "Georgia": 0.844, "Saint Kitts and Nevis": 0.840, "Panama": 0.839, "Brunei": 0.837, "Kazakhstan": 0.837, "Costa Rica": 0.833, "Republic of Serbia": 0.833, "Russia": 0.832, "Belarus": 0.824, "Bahamas": 0.820, "Malaysia": 0.819, "Macedonia": 0.815, "Armenia": 0.811, "Barbados": 0.811, "Albania": 0.810, "Trinidad and Tobago": 0.807, "Mauritius": 0.806, "Bosnia and Herzegovina": 0.804, "Iran (Islamic Republic of)": 0.799, "Saint Vincent and the Grenadines": 0.798, "Thailand": 0.798, "China": 0.797, "Peru": 0.794, "Grenada": 0.791, "Azerbaijan": 0.789, "Mexico": 0.789, "Colombia": 0.788, "Brazil": 0.786, "Palau": 0.786, "Moldova": 0.785, "Ukraine": 0.779, "Ecuador": 0.777, "Dominican Republic": 0.776, "Guyana": 0.776, "Sri Lanka": 0.776, "Tonga": 0.769, "Maldives": 0.766, "Viet Nam": 0.766, "Turkmenistan": 0.764, "Algeria": 0.763, "Cuba": 0.762, "Dominica": 0.761, "Paraguay": 0.756, "Egypt": 0.754, "Jordan": 0.754, "Lebanon": 0.752, "Saint Lucia": 0.748, "Mongolia": 0.747, "Tunisia": 0.746, "Kosovo": 0.742, "South Africa": 0.741, "Uzbekistan": 0.740, "Bolivia": 0.733, "Gabon": 0.733, "Marshall Islands": 0.733, "Botswana": 0.731, "Fiji": 0.731, "Indonesia": 0.728, "Suriname": 0.722, "Belize": 0.721, "Libya": 0.721, "Jamaica": 0.720, "Kyrgyzstan": 0.720, "Philippines": 0.720, "Morocco": 0.710, "Venezuela (Bolivarian Republic of)": 0.709, "Samoa": 0.708, "Nicaragua": 0.706, "Nauru": 0.703, "Bhutan": 0.698, "Eswatini (Kingdom of)": 0.695, "Iraq": 0.695, "Tajikistan": 0.691, "Tuvalu": 0.689, "Bangladesh": 0.685, "India": 0.685, "El Salvador": 0.678, "Equatorial Guinea": 0.674, "Palestine, State of": 0.674, "Cabo Verde": 0.668, "Namibia": 0.665, "Guatemala": 0.662, "Republic of the Congo": 0.649, "Honduras": 0.645, "Kiribati": 0.644, "Sao Tome and Principe": 0.637, "Timor-Leste": 0.634, "Ghana": 0.628, "Kenya": 0.628, "Nepal": 0.622, "Vanuatu": 0.621, "Lao People's Democratic Republic": 0.617, "Angola": 0.616, "Micronesia (Federated States of)": 0.615, "Myanmar": 0.609, "Cambodia": 0.606, "Comoros": 0.603, "Zimbabwe": 0.598, "Zambia": 0.595, "Cameroon": 0.588, "Solomon Islands": 0.584, "Ivory Coast": 0.582, "Uganda": 0.582, "Rwanda": 0.578, "Papua New Guinea": 0.576, "Togo": 0.571, "Syrian Arab Republic": 0.564, "Mauritania": 0.563, "Nigeria": 0.560, "Tanzania (United Republic of)": 0.555, "Haiti": 0.554, "Lesotho": 0.550, "Pakistan": 0.544, "Senegal": 0.530, "Gambia": 0.524, "Congo (Democratic Republic of the)": 0.522, "Malawi": 0.517, "Benin": 0.515, "Guinea Bissau": 0.514, "Djibouti": 0.513, "Sudan": 0.511, "Liberia": 0.510, "Eritrea": 0.503, "Guinea": 0.500, "Ethiopia": 0.497, "Afghanistan": 0.496, "Mozambique": 0.493, "Madagascar": 0.487, "Yemen": 0.470, "Sierra Leone": 0.467, "Burkina Faso": 0.459, "Burundi": 0.439, "Mali": 0.419, "Niger": 0.419, "Chad": 0.416, "Central African Republic": 0.414, "Somalia": 0.404, "South Sudan": 0.388
    }

    # Corrections de noms entre GeoJSON et IDH
    name_corrections = {
        "Czech Republic": "Czechia",
        "Turkey": "Türkiye",
        "Congo": "Republic of the Congo",
        "Democratic Republic of the Congo": "Congo (Democratic Republic of the)",
        "Palestine": "Palestine, State of",
        "Tanzania": "Tanzania (United Republic of)",
        "Vietnam": "Viet Nam",
        "Swaziland": "Eswatini (Kingdom of)",
        "Iran": "Iran (Islamic Republic of)",
        "Venezuela": "Venezuela (Bolivarian Republic of)",
        "Laos": "Lao People's Democratic Republic",
        "Syria": "Syrian Arab Republic",
    }

    # Charger le GeoJSON mondial
    url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"
    geojson_data = requests.get(url).json()

    # Étendre le dictionnaire IDH pour inclure les deux versions (originale + corrigée)
    idh_full = idh_data.copy()
    for wrong, correct in name_corrections.items():
        if correct in idh_data:
            idh_full[wrong] = idh_data[correct]

    # Carte moderne
    m = folium.Map(location=[20, 0], zoom_start=2.3, tiles="CartoDB Voyager")

    # Supprimer le contour bleu
    m.get_root().html.add_child(folium.Element("""
        <style>
            path:focus { outline: none !important; }
        </style>
    """))

    # Couleur selon IDH
    def style_function(feature):
        country = feature["properties"]["name"]
        country = name_corrections.get(country, country)
        idh = idh_data.get(country)
        if idh is None:
            color = "#e0e0e0"
        elif idh >= 0.9:
            color = "#2c7bb6"
        elif idh >= 0.8:
            color = "#abd9e9"
        elif idh >= 0.7:
            color = "#ffffbf"
        elif idh >= 0.6:
            color = "#fdae61"
        else:
            color = "#d7191c"
        return {"fillColor": color, "color": "#555", "weight": 0.4, "fillOpacity": 0.8}

    highlight = lambda _: {"fillColor": "#ffcc66", "color": "#333", "weight": 1, "fillOpacity": 0.9}

    for feature in geojson_data["features"]:
        folium.GeoJson(
            feature,
            style_function=style_function,
            highlight_function=highlight,
            tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Pays :"])
        ).add_to(m)

    return m


# ---------------------------
# THÉMATIQUES ONG
# ---------------------------

def show_theme_analysis(df):
    st.subheader("Associations par thématique")
    themes = sorted(df["domaine"].dropna().unique())
    selected_theme = st.selectbox("Choisissez un thème :", themes)

    theme_df = df[df["domaine"] == selected_theme]
    st.markdown(f"### {len(theme_df)} associations dans le domaine **{selected_theme}**")

    for _, row in theme_df.iterrows():
        lien_don = row.get("liens_dons", "")
        bouton_don = f"[🤲 Faire un don]({lien_don})" if isinstance(lien_don, str) and lien_don.strip() != "" else ""
        
        st.markdown(f"""
        **{row['nom']}**  
        *{row['pays']}*  
        **Domaine :** {row['domaine']}  
        [🌐 Site officiel]({row['site_web']}) {bouton_don}
        ---
        """)

# ---------------------------
# PAGE DE DONS
# ---------------------------

def donation_page(df):
    st.subheader("Faire un don à une association")

    # Vérifier si l'utilisateur est connecté
    user = st.session_state.get("user_email")
    if not user:
        st.warning("Veuillez vous connecter dans la barre latérale avant de faire un don.")
        return

    # Sélection de l'association
    ong_names = sorted(df["nom"].dropna().astype(str).unique())
    selected_ong = st.selectbox("Choisissez une association :", ong_names, key="select_ong")

    # Récupération des infos
    ong_info = df[df["nom"] == selected_ong].iloc[0]
    lien_don = str(ong_info.get("liens_dons") or ong_info.get("lien_don") or "").strip()

    # Affichage des infos de l'ONG
    st.markdown(f"""
    **Pays :** {ong_info['pays']}  
    **Domaine :** {ong_info['domaine']}  
    **Site officiel :** [🌐 Voir le site officiel]({ong_info['site_web']})  
    """)

    st.divider()

    # Formulaire
    st.markdown("### Don en ligne")
    montant = st.number_input("Montant du don (€)", min_value=1, step=1)
    methode = st.selectbox("Méthode de paiement :", ["Carte bancaire", "PayPal", "Apple Pay"])

    if st.button("Payer"):
        st.success(f"Merci {user} 🙏 Vous avez choisi de donner **{montant} €** à **{selected_ong}** via **{methode}**.")

        # Enregistrement dans l'historique
        st.session_state["historique_dons"].append({
            "utilisateur": user,
            "association": selected_ong,
            "pays": ong_info["pays"],
            "domaine": ong_info["domaine"],
            "montant": montant,
            "methode_de_paiement": methode
        })

        # Lien de don officiel
        if lien_don:
            st.markdown(f"""
            ---
            ### 🎯 Finaliser votre don :
            👉 [Cliquez ici pour accéder à la page officielle de don de **{selected_ong}**]({lien_don})
            """, unsafe_allow_html=True)
        else:
            st.warning("Cette association n’a pas encore de lien de don disponible.")


# ---------------------------
# HISTORIQUE DES DONS
# ---------------------------

def show_don_history():
    st.subheader("Historique de mes dons")
    if "historique_dons" not in st.session_state or not st.session_state["historique_dons"]:
        st.info("Aucun don enregistré.")
        return

    dons_df = pd.DataFrame(st.session_state["historique_dons"])
    st.dataframe(dons_df)
    st.metric("Total des dons", f"{dons_df['montant'].sum()} €")

    fig = px.bar(dons_df, x="domaine", y="montant", color="domaine", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# BARRE DE RECHERCHE
# ---------------------------

def search_bar(df):
    """Affiche la barre de recherche horizontale et retourne les paramètres saisis"""
    st.markdown("### 🔍 Recherche d'associations")

    col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 1])

    with col_a:
        countries = ["Tous"] + sorted(set(sum([p.split(";") for p in df["pays_intervention"].dropna()], [])))
        countries = [c.strip() for c in countries if c.strip()]
        selected_country = st.selectbox("🌍 Pays", countries)

    with col_b:
        search_name = st.text_input("🔎 Nom de l'association")

    with col_c:
        selected_domains = st.multiselect("🎯 Domaine", sorted(df["domaine"].dropna().astype(str).unique()))

    with col_d:
        search_button = st.button("Rechercher", use_container_width=True)

    return selected_country, selected_domains, search_name, search_button


# ---------------------------
# AFFICHAGE DES RÉSULTATS
# ---------------------------

def show_search_results(df, country, domains, search_name):
    """Affiche les résultats d'une recherche"""
    filtered_df = filter_data(df, country, domains, search_name)

    st.markdown(f"### 🔸 {len(filtered_df)} ONG trouvées")

    if len(filtered_df) == 0:
        st.info("Aucune ONG ne correspond à votre recherche.")
    else:
        for _, row in filtered_df.iterrows():
            lien_don = row.get("liens_dons", "")
            bouton_don = f"[🤲 Faire un don]({lien_don})" if isinstance(lien_don, str) and lien_don.strip() != "" else ""
            
            st.markdown(f"""
            **{row['nom']}** — *{row['domaine']}*  
            _{row['pays']}_  
            [🌐 Site officiel]({row['site_web']}) {bouton_don}
            ---
            """)

def show_login_page():
    """Page d'accueil stylisée avec connexion et actualité humanitaire"""
    st.set_page_config(page_title="ONG Explorer 2.0", layout="centered")

    # 🌍 TITRE PRINCIPAL
    st.markdown("""
        <div style='text-align: center; padding: 40px 20px;'>
            <h1 style='font-size: 36px; color: #1a1a1a;'>🌍 Bienvenue sur <span style='color:#0078ff;'>ONG Explorer 2.0</span></h1>
            <p style='font-size:17px; color:#555;'>Connectez-vous pour accéder à la carte interactive des ONG dans le monde.</p>
        </div>
    """, unsafe_allow_html=True)

    # 📩 CONNEXION
    email = st.text_input("Adresse e-mail :", placeholder="ex : nom@exemple.com")
    if st.button("Se connecter"):
        if "@" in email and "." in email:
            st.session_state["user_email"] = email
            st.success(f"Bienvenue {email} 👋")
            st.rerun()
        else:
            st.error("Adresse e-mail invalide.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📰 Actualité humanitaire du jour")

    # 🟦 Bouton de nouvelle actu
    if st.button("🔁 Voir une autre actualité"):
        # On change la seed de recherche pour forcer ReliefWeb à renvoyer un autre résultat
        st.session_state["reliefweb_offset"] = st.session_state.get("reliefweb_offset", 0) + 1
        st.rerun()

    # ⚙️ API ReliefWeb
    try:
        offset = st.session_state.get("reliefweb_offset", 0)
        url = f"https://api.reliefweb.int/v1/reports?appname=apidoc&profile=full&limit=1&offset={offset}&sort[]=date:desc"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            report = data["data"][0]["fields"]

            # 📰 Mise en forme claire et encadrée
            st.markdown("<div style='background-color:white;padding:20px 25px;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)

            st.markdown(f"### {report['title']}")
            st.write(f"**Date :** {report['date']['created'][:10]}")
            st.write(f"**Source :** {', '.join([s['name'] for s in report['source']])}")

            body_text = re.sub('<[^<]+?>', '', report.get("body-html", ""))
            st.markdown(body_text[:800] + "...", unsafe_allow_html=True)
            st.markdown(f"[🔗 Lire l’article complet sur ReliefWeb]({report['url']})")

            st.markdown("</div>", unsafe_allow_html=True)


        else:
            st.warning("Impossible de récupérer les dernières actualités pour le moment.")
    except Exception as e:
        st.error(f"Erreur API : {e}")

    # 🎨 Style global
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f7fa;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        button {
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)



# ---------------------------
# APPLICATION PRINCIPALE
# ---------------------------

def main():
    if not st.session_state.get("user_email"):
        show_login_page()
        return  # on quitte ici pour ne pas exécuter la suite tant que pas connecté
    # 🔒 Si connecté, affichage du contenu principal
    st.set_page_config(page_title="ONG Explorer 2.0", layout="wide")
    st.title("🌍 ONG Explorer 2.0 — Vue d'ensemble des actions humanitaires mondiales")

    df = load_data("bdd_ong.csv")
    user_login()

    tabs = st.tabs([" Carte interactive", " Par thématique", " Faire un don", " Mes dons"])

    # --- Onglet Carte interactive ---
    with tabs[0]:
        # --- BARRE DE RECHERCHE ---
        selected_country, selected_domains, search_name, search_button = search_bar(df)

        if search_button:
            # Quand on clique sur "Rechercher"
            filtered_df = filter_data(df, selected_country, selected_domains, search_name)
            st.markdown(f"### 🔸 {len(filtered_df)} ONG trouvées")

            if len(filtered_df) == 0:
                st.info("Aucune ONG ne correspond à votre recherche.")
            else:
                for _, row in filtered_df.iterrows():
                    st.markdown(f"""
                    **{row['nom']}** — *{row['domaine']}*  
                    _{row['pays']}_  
                    [Site officiel]({row['site_web']})
                    ---
                    """)

            if st.button("↩️ Revenir à la carte"):
                st.rerun()

        else:
            # --- Affichage par défaut : la carte ---
            st.subheader("Carte des ONG dans le monde")
            col1, col2 = st.columns([2, 1])
            m = create_map(df)

            with col1:
                map_data = st_folium(m, width=750, height=500)

            # 💡 Légende IDH propre sous la carte
            st.markdown("""
            <div style="
                background-color: white;
                border: 1px solid #bbb;
                border-radius: 8px;
                padding: 10px 20px;
                margin-top: 10px;
                width: 720px;
                font-size: 13px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            ">
            <b>Indice de Développement Humain (IDH)</b> — <i>Source : ONU 2023</i><br><br>
            <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 25px; height: 15px; background-color: #2c7bb6; margin-right: 6px;"></div> Très élevé (≥ 0.9)
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 25px; height: 15px; background-color: #abd9e9; margin-right: 6px;"></div> Élevé (0.8–0.9)
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 25px; height: 15px; background-color: #ffffbf; margin-right: 6px;"></div> Moyen (0.7–0.8)
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 25px; height: 15px; background-color: #fdae61; margin-right: 6px;"></div> Faible (0.6–0.7)
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 25px; height: 15px; background-color: #d7191c; margin-right: 6px;"></div> Très faible (< 0.6)
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            # --- Infos pays cliqué ---
            with col2:
                if map_data and map_data.get("last_active_drawing"):
                    selected_country = map_data["last_active_drawing"]["properties"]["name"]
                    st.markdown(f"### 🌍 {selected_country}")

                    try:
                        r = requests.get(f"https://restcountries.com/v3.1/name/{selected_country}?fullText=true")
                        info = r.json()[0] if r.status_code == 200 else None
                    except Exception:
                        info = None

                    if info:
                        st.image(info["flags"]["png"], width=120)
                        st.markdown(f"**Capitale :** {', '.join(info.get('capital', []))}")
                        st.markdown(f"**Population :** {info.get('population', 'Inconnue'):,}")
                        st.markdown(f"**Langues :** {', '.join(info.get('languages', {}).values())}")
                    else:
                        st.info("Aucune donnée disponible pour ce pays.")

                    # --- ONG présentes dans le pays cliqué ---
                    ong_list = df[df["pays_intervention"].str.contains(selected_country, case=False, na=False)]
                    st.markdown("---")

                    if len(ong_list) > 0:
                        locales = ong_list[ong_list["pays"].str.lower() == selected_country.lower()]
                        internationales = ong_list[ong_list["pays"].str.lower() != selected_country.lower()]

                        st.write(f"### 🤝 ONG présentes : {len(ong_list)}")

                        # --- ONG locales ---
                        st.markdown("#### 🏠 ONG locales")
                        if len(locales) > 0:
                            for _, row in locales.iterrows():
                                lien_don = row.get("liens_dons", "")
                                bouton_don = f"[🤲 Faire un don]({lien_don})" if isinstance(lien_don, str) and lien_don.strip() != "" else ""
                                st.markdown(f"**{row['nom']}** — *{row['domaine']}*  \n[🌐 Site officiel]({row['site_web']}) {bouton_don}")
                        else:
                            st.info("Aucune ONG locale recensée pour ce pays.")

                        # --- ONG internationales ---
                        st.markdown("#### 🌍 ONG internationales")
                        if len(internationales) > 0:
                            for _, row in internationales.iterrows():
                                lien_don = row.get("liens_dons", "")
                                bouton_don = f"[🤲 Faire un don]({lien_don})" if isinstance(lien_don, str) and lien_don.strip() != "" else ""
                                st.markdown(f"**{row['nom']}** — *{row['domaine']}*  \n[🌐 Site officiel]({row['site_web']}) {bouton_don}")
                        else:
                            st.info("Aucune ONG internationale recensée pour ce pays.")

                    else:
                        st.info("Aucune ONG répertoriée pour ce pays.")

                else:
                    st.info("Cliquez sur un pays pour afficher ses informations.")


    # --- Onglet Thématiques ---
    with tabs[1]:
        show_theme_analysis(df)

    # --- Onglet Don ---
    with tabs[2]:
        donation_page(df)

    # --- Onglet Historique ---
    with tabs[3]:
        show_don_history()


# ---------------------------
# LANCEMENT
# ---------------------------

if __name__ == "__main__":
    main()