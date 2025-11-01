# Développement d'une WebApp Interactive avec Streamlit - Lina Ibouchichene & Alexandre Mégard

# ONG Explorer 2.0 - Une vue d'ensemble sur les actions humanitaires mondiales

# Objectif du projet
ONG Explorer 2.0 est une application web interactive développée avec Streamlit qui a pour objectif de répertorier les organisations non gouvernementales (ONG)  à travers le monde, de permettre leur visualisation sur une carte interactive, de visualiser leurs zones d’intervention, leurs domaines d’action, et de réaliser des dons en ligne de manière simplifiée via une redirection vers la page de l'ONG sélectionnée. Ce projet vise à rendre l’action humanitaire plus accessible et plus claire pour celles et ceux qui veulent donner, mais ne savent pas comment s'y prendre. Cette application facilite la découverte des ONG par pays et par domaine d’intervention.
Nous avons voulu nous intéresser à un domaine qui nous tient à cœur personnellement, avec l'idee d'une application qui n'existe pas encore mais qui pourrait avoir un impact important dans un domaine qui en a besoin, en combinant plusieurs fonctionnalités : carte interactive, recherche par thème/pays, don, historique utilisateur. Cela ajoute de la valeur, le don directement depuis l'application reste un point complexe à notre stade mais très pertinent. 

## Les Différentes Fonctionnalités principales

### Connexion utilisateur (page d'accueil)
- Système de connexion simple via une adresse e-mail crée avec st.session_state["user_email"].
- Possibilité de connexion et déconnexion.

### L'Actualité humanitaire (page d’accueil)
- Affichage automatique d’un article issu de l’API ReliefWeb.
- Bouton pour recharger une nouvelle actualité humanitaire.
- Contenu formaté en HTML (titre, date, source, lien complet), le but est d'informer les utilisateurs des crises humanitaires en cours.  

### Une Carte interactive mondiale
- Affichage de toutes les ONG répertoriées dans le fichier `bdd_ong.csv` sur une carte mondiale.
- Intégration de la carte avec Folium pour avoir un rendu dynamique et un zoom fluide: lorsque l'on clique sur un pays, ça affichage des ONG locales et internationales.
- Visualisation des pays selon leur Indice de Développement Humain (IDH) (source : ONU 2023) avec une légende en dessous de la carte.
- Affichage des informations clés (nom, domaine, pays, site officiel).
- Cliquer sur un pays affiche les ONG locales et internationales présentes sur place,
- Informations issues de RestCountries API (capitale, population, langues, drapeau).

### Barre horizontale 
- Filtres par pays, domaine d’intervention et nom d’association.

### Recherche et filtrage des ONG
- Recherche par pays d’intervention, nom et domaine d’action.
- Filtrage dynamique et affichage clair des résultats avec lien vers le site officiel et la page de dons via la fonction filter_data(df, country, domains, search_name).

### Une Analyse par thématique
- Classement des ONG par domaine humanitaire: éducation, santé, environnement,eau etc.

### Une Page de dons et paiement
- Possibilité de selectionner une ONG via la liste dérouante ou de l'écrire et de faire un don
- Choix du moyen de paiement (CB, PayPal, Apple Pay) et du montant.
- Enregistrement automatique du don dans l’historique utilisateur avec st.session_state["historique_dons"].
- Rediriger vers le lien de la page de don officielle de l’association.

### Un Historique des dons 
- Tableau récapitulatif des dons effectués (montant, ONG, catégories...).
- Calcul du total des dons classés par catégories.
- Visualisation graphique avec Plotly (barres colorées par domaine).

### Les Différentes Fonctions utilisées sur python
- Streamlit : Pour créer l'interface utilisateur soit l'application web
- Pandas : Pour la gestion des données
- Folium et streamlit-folium : Pour avoir une carte interactive
- Plotly Express : Pour les visualisations graphiques
- Requests : Appels d’API externes (ReliefWeb, RestCountries)
- CSV : Pour la base de données simplifiée des ONG avec leur localisation, leur noms, leur site internat etc.

