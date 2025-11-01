## 🌍 ONG Explorer 2.0

**Développement d'une WebApp Interactive avec Streamlit — Lina Ibouchichene & Alexandre Mégard**

### 🎯 Objectif du projet

**ONG Explorer 2.0** est une application web interactive développée avec **Streamlit** qui vise à **répertorier et visualiser les organisations non-gouvernementales (ONG)** à travers le monde.
Elle permet aux utilisateurs de découvrir les **zones d’intervention**, les **domaines d’action** et d’effectuer des **dons en ligne** via une redirection vers la page officielle de l’association sélectionnée.
L’objectif principal est de **rendre l’action humanitaire plus accessible** pour celles et ceux qui veulent contribuer sans savoir vers qui se tourner.
Le projet combine plusieurs fonctionnalités inédites : carte interactive, recherche par pays et par thématique, actualité humanitaire en temps réel et historique de dons personnalisé.

---

### 🚀 Fonctionnalités principales

#### 🔐 Connexion utilisateur

* Système de connexion simple par adresse e-mail (`st.session_state["user_email"]`)
* Possibilité de connexion et déconnexion à tout moment via la barre latérale

#### 📰 Actualité humanitaire

* Intégration de l’API **ReliefWeb** pour afficher automatiquement les dernières actualités humanitaires mondiales
* Contenu formaté en HTML (titre, date, source, lien complet)
* Bouton “🔁 Voir une autre actualité” pour actualiser l’article

#### 🗺️ Carte interactive mondiale

* Carte dynamique réalisée avec **Folium** intégrée à Streamlit via `streamlit-folium`
* Affichage des ONG issues du fichier `bdd_ong.csv`
* Coloration des pays selon leur **Indice de Développement Humain (IDH – ONU 2023)**
* Informations RestCountries API (capitale, population, langues, drapeau)
* Zoom fluide et affichage des **ONG locales** et **internationales** par pays

#### 🔍 Recherche et filtrage des ONG

* Barre de recherche horizontale : par **pays d’intervention**, **domaine d’action** ou **nom**
* Fonction `filter_data(df, country, domains, search_name)` pour un filtrage dynamique
* Résultats affichés avec nom, domaine, pays, et lien direct vers le site officiel ou la page de don

#### 📊 Analyse par thématique

* Classement des ONG par **domaine humanitaire** (éducation, santé, environnement, eau, etc.)
* Interface claire pour parcourir chaque thématique et accéder aux associations correspondantes

#### 💳 Page de dons

* Sélection d’une ONG dans un menu déroulant
* Choix du **montant** et du **moyen de paiement** (Carte bancaire, PayPal, Apple Pay)
* Sauvegarde automatique du don dans `st.session_state["historique_dons"]`
* Redirection vers la **page officielle de don** de l’association sélectionnée

#### 📈 Historique des dons

* Tableau récapitulatif des dons effectués (montant, ONG, catégorie, méthode de paiement)
* Calcul automatique du total des dons
* Visualisation graphique avec **Plotly Express** (barres colorées par domaine)

---

### 🧰 Technologies utilisées

| Composant                     | Description                                             |
| ----------------------------- | ------------------------------------------------------- |
| **Python**                    | Langage principal                                       |
| **Streamlit**                 | Création de l’interface web interactive                 |
| **Pandas**                    | Gestion et manipulation des données                     |
| **Folium / streamlit-folium** | Carte interactive mondiale                              |
| **Plotly Express**            | Visualisations graphiques dynamiques                    |
| **Requests**                  | Appels aux API externes (ReliefWeb, RestCountries)      |
| **CSV**                       | Base de données locale des ONG et de leurs informations |

---

### 🗂️ Structure du projet

```
ong-explorer/
├── app.py                 # Script principal Streamlit
├── bdd_ong.csv            # Base de données des ONG
├── requirements.txt       # Liste des dépendances
├── README.md              # Documentation du projet
└── data/                  # (optionnel) fichiers annexes
```

---

### 💡 Notes techniques

* L’IDH est basé sur les données **ONU 2023** et sert à colorer la carte par niveau de développement.
* Le système de session (`st.session_state`) gère à la fois la **connexion utilisateur** et **l’historique des dons**.
* Les appels API sont sécurisés avec une gestion d’erreurs pour assurer la stabilité de l’application.
* L’application est totalement **responsive** et fonctionne sur **Windows, macOS et Linux**.

---

### 🧠 Auteurs

👩‍💻 **Lina Ibouchichene**
👨‍💻 **Alexandre Mégard**
