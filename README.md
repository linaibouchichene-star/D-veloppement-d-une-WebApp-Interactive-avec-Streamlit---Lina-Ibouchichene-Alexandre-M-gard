# Développement d'une WebApp Interactive avec Streamlit - Lina Ibouchichene & Alexandre ””Mégard

# ONG Explorer 2.0 - Une vue d'ensemble sur les actions humanitaires mondiales

# Objectif du projet
ONG Explorer 2.0 est une application web interactive développée avec Streamlit qui a pour objectif de répertorier les organisations humanitaires (ONG) à travers le monde et de permettre leur visualisation sur une carte interactive, afin d’offrir la possibilité de faire des dons directement depuis l’application et etre redirigé vers la page en question. Ce projet vise à rendre l’action humanitaire plus accessible et plus clair pour les personnes qui sont intéréssés par ces actions, cela facilite la découverte des ONG par pays et par domaine d’intervention.

## Les Différentes Fonctionnalités principales

### Une Carte interactive
- Affichage de toutes les ONG répertoriées dans le fichier `bdd_ong.csv` sur une carte mondiale.
- Filtres par **pays**, **domaine d’intervention**, et **nom d’association**.
- Affichage des informations clés (nom, domaine, pays, site officiel).

### Une Analyse par thématique
- Classement des ONG par **domaine humanitaire** (éducation, santé, environnement, etc.).
- Consultation détaillée de chaque ONG par thème.

### Une Page de dons
- Système de **connexion utilisateur par e-mail**.
- Possibilité de **sélectionner une ONG** et de **faire un don simulé**.
- Enregistrement des dons dans un **historique local (CSV)**.
- Redirection vers le **site officiel** de l’ONG pour finaliser le don réel.

### Un Historique et statistiques
- Affichage de l’**historique des dons simulés** avec montant, date, et domaine.
- Visualisation des **montants par domaine** à l’aide d’un graphique interactif Plotly.

## Les Différentes Fonctions utilisées sur python
- Streamlit : (pour créer l'interface utilisateur soit l'application web)
- Pandas : (pour la gestion des données)
- Folium : et streamlit-folium (pour avoir une cartographie interactive)
- Plotly Express : (U visualisations graphiques)
- CSV : (Pour la base de données simplifiée des ONG avec leur localisation, leur noms, leur site internat etc)

