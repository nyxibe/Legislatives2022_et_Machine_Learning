# HISTO POLITIK : M.L. & Sciences Sociales

#### L'idée : Qui vote pour qui et pourquoi ?

Comment se compose la structure sociale des électorats des différents courants et mouvements politiques ?
En associant : le travail inédit de numérisation des données électorales et socio-économiques établit par Julia Cagé et Thomas Piketty et les outils de Machine Learning pourrait on prédire et/ou expliquer les résultats des différents courants politiques aux dernières législatives (2022) ?

## Table des matières

- [HISTO POLITIK : M.L. & Sciences Sociales](#HISTO-POLITIK-:-M.L.-&-Sciences-Sociales)
- [Table des matières](#Table-des-matières)
- [Instructions](#Instructions)
    -[Prérequis](#Prérequis)
    -[Instructions](#Instructions)
  - [Etapes réalisées pour la réalisation du projet](#Etapes-réalisées-pour-la-réalisation-du-projet)
    - [EDA - Création de la Data](#EDA---Création-de-la-Data)
      - EDA0_import_files.ipynb: Import, premieres analyse, document de synthèse 
      - EDA1_Analysis_2cities.ipynb: Analyse de la data focalisée sur 2 communes 
      - EDA2_Target.ipynb : Fichiers de noscibles 
      - Sélection, préparation et mise en forme des données par fichier
      - Moteur d’intégration fusionnant et validant les données pour nos modèles
    - [MODEL - Analyse / exploitations de 3 Modèles](#MODEL---Analyse-/-exploitations-de-3-Modèles)
    - [Mise en place de la base SQL](#Mise-en-place-de-la-base-SQL)
    - [Livraison_FRONT - Visualisation finale des données](#Livraison_FRONT---Visualisation-finale-des-données)
- [streamlit_app](#streamlit_app)
- [HuggingFace space](#HuggingFace-space)
- [Auteurs](#Auteurs)


## Instructions

Suivez les instructions suivantes pour mettre en place l'application et la faire tourner en local sur votre machine.

### Prérequis

Avant de commencer, assurez vous d'avoir ces 2 programmes d'installés:


- [Python 3.10.4](https://www.python.org/downloads/release/python-3104/) ou une version plus récente.
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (afin de créer un environnement virtuel).

### Installation

1. Cloner le dépôt sur votre machine:
```bash
git clone https://github.com/nyxibe/HistoPolitik_2.git
```

2. Naviguer jusqu'au dossier:
```bash
cd HistoPolitik_2
```

3. Créer un environnement (recommandé):
```bash
virtualenv venv
```

4. Activer l'environnement virtuel:
- Windows:
```bash
venv\Scripts\activate
```
- macOS and Linux:
```bash
source venv/bin/activate
```

5. Installer les dépendances nécessaires:
```bash
pip install -r requirements_dev.txt
```
## Etapes réalisées pour la réalisation du projet

### EDA - Création de la Data

En raison du poids de la data d'origine, celle ci n'apparait pas sur le dépôt GitHub (DATA_SOURCES/HCP = vide). Nous vous invitons à télécharger vous même la data [ici](https://unehistoireduconflitpolitique.fr/telecharger.html)

#### > EDA0_import_files.ipynb:

Après la récupération de l'intégralité des fichiers au format CSV à partir du site web.
Construction d’un dataframe cataloguant les fichiers explorés.
Importation de ces mêmes fichiers dans des dataframes individuelles, suivie d'une analyse des dimensions, des valeurs, et de l'exploration des colonnes.
L'objectif est de filtrer ces documents, identifier les liaisons, et surtout construire un fichier synthétique au format Excel de l'ensemble des documents avec :

- 1 : un onglet contenant la liste et la synthèse des documents.
- 2 : un onglet avec une colonne par fichier, où chaque ligne comprend :
  - L'intitulé des colonnes.
  - L'intervalle des valeurs, pour les données numériques.
  - Le nombre total de lignes, ainsi que le nombre et la proportion des valeurs manquantes (NaN).
- 3 : un onglet avec la même structure que l'onglet précédent, mais présentant 2 exemples aléatoires

PS : Nous nous sommes arrété sur les législatives 2022 car :
Les structures des partis évoluent constamment, et transcoder ces évolutions serait trop chronophage (nécessiterait des arbitrages discutables). 
Les structures nationales des communes et cantons évoluent également, et vouloir travailler sur des échelles de temps nécessiterait des travaux de transcodage prolongés.

#### > EDA1_Analysis_2cities.ipynb:
Ce notebook analyse le catalogue de dataframes et régénère, pour chaque fichier, une dataframe réduite au périmètre de 2 communes. Cela permet de faire des analyses poussées pour valider l'unicité ou l'absence d'unité de ligne par commune et de créer des graphiques.

#### > EDA2_Target.ipynb :
Ce notebook se focalise sur notre cible : les résultats aux législatives de 2022 des communes de plus de 200 inscrits. Il nous permet d'explorer la structure et la forme de ces données, la mise en place de regroupements, d'observer la ventilation des votes en fonction du nombre d'inscrits par commune.

#### > Sélection, préparation et mise en forme des données par fichier :
Après la phase d'exploration, vient la cinstruction de la DATA support pour nos modèles. Chaque fichier source a été traité individuellement dans une note portant le nom "df_create_COD_NomDuFichierSource.ipynb". 
Ce fichier prendra en entrée le fichier source auquel il fait référence, et disposera de codes uniques à 3 lettres codifiant cette même source. 
Ce notebook filtrera, notera et fournira en sortie les informations le concernant à exporter pour notre étude dans un fichier CSV. 

#### > Moteur d’intégration fusionnant et validant les données pour nos modèles :

Ce notebook parcourt le répertoire /DATA/EXPORT_CSV/ et traite tous les fichiers .csv. Tests & actions :
- A: le nom du fichier doit commencer par final
- B: validation du nombre de lignes
- C: validation des entêtes
- D: validation des clés (depuis list_codecommune_leg2022_200inscrits.txt)
- E: récupération de la liste des bons préfixes à traiter (file_name.split('_')[1:-1])
- F: récupération de la dataframe avec les colonnes qui disposent des préfixes souhaités
- G: fusion (merge) sur la colonne codecommune

Une fois tous les fichiers traités, notre dataframe globale est exportée sous forme de fichier plat.

### MODEL - Analyse / exploitations de 3 Modèles

Ce répertoire contient tous les modèles entraînés pour notre Data. Dans un premier temps, construire les modèles les plus performants. Les exporter. Exploiter le fruit de leurs prédictions sous 2 formats :
- Prédictions pour chaque ligne du périmètre des scores pour tous les groupes (partis) référencés.
- Exporter pour chaque groupe le poids de chaque facteur d’importance pour plus tard les examiner. 
Concrètement, chacun de nous a depuis la même data travailler sur un modèle et s’est chargé de fournir sous forme de données SQL ou de fichier plat les 2 types d’informations attendues.

### Mise en place de la base SQL

Toutes nos informations en entrée comme en sortie seront centralisées dans une base SQL avec les tables ci-dessous :
- villes_tbl [informations sur les communes]
- X_col_titr_tbl [table de transcodage de l’indice et du nom de la feature importante]
- y_resultats200_tbl [liste des résultats aux législatives 2022, notre « y »]
- data_tbl [notre data globale notre « X »]

Pour nos modèles : 
  - LGB_reg200_importance_tbl [liste des poids et indices pour chaque groupe pour model LGB]
  - LGB_reg200_resultats_tbl [liste des poids et indices pour chaque groupe pour model LGB]
  - RandomF_reg200_importance_tbl
  - RandomF_reg200_resultats_tbl
  - XGBoost_reg200_importance_tbl
  - XGBoost_reg200_resultats_tbl

Ainsi cette base sera la seule DATA à exporter pour la mise en ligne de notre travail (environnement de production : streamlit).

### Livraison_FRONT : Visualisation finale des données

Avant même de se lancer et de mettre en forme nos résultats, il nous a fallu observer ces derniers, les analyser et voir comment les présenter. Ces 3 documents sont le support de ce travail.
- Front_france.ipynb : analyse des données globales
- Front_Models.ipynb : visualisation des modèles (performances / facteurs d’importances)
- Front_Resultats.ipynb 

## streamlit_app
Répertoire streamlit pour faire les tests en local. 
```bash
streamlit run Accueil.py
```
### les pages permettent de :

- Accueil.py : Présentation du projet et des sources. Ainsi que présentation des regroupements des partis politiques.

- pages/Cartographie-et-Data.py : Visualiser d'une partie des données sous forme de cartes.

- pages/Prédictions.py : Comparer les prédictions et la realité sur toutes les communes de France qui disposaient d'au moins de 200 inscrits lors des éléctions législatives de 2022.

- pages/Modèles.py : Visualiser les facteurs d'importances (ex: age, diplôme, nombre de crimes...) par partis politiques support à notre prédiction.

## HuggingFace space
Dans le cas où vous ne voulez rien installer. Vous pouvez aller directement sur [Hugging Face Space](https://huggingface.co/spaces/Caicaire93/Histo_politik) créé pour l'occasion.

## Auteurs
- [NYX](https://github.com/nyxibe)
- [Caicaire93](https://github.com/Caicaire93)
- [Anouaradyel2](https://github.com/anouaradyel2)