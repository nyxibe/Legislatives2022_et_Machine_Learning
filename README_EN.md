# HISTO POLITIK : M.L. & Sciences Sociales

#### The idea: Who votes for whom and why?
What is the social structure of the electorates of the various political movements and currents?
By combining Julia Cagé and Thomas Piketty's groundbreaking digitization of electoral and socio-economic data with Machine Learning tools, could we predict and/or explain the results of the various political currents in the last legislative elections (2022)?

## Table of Contents

- [HISTO POLITIK : M.L. & Sciences Sociales](#HISTO-POLITIK-:-M.L.-&-Sciences-Sociales)
- [Table of Contents](#Table-of-Contents)
- [Instructions](#Instructions)
    -[Prerequisites](#Prerequisites)
    -[Instructions](#Instructions)
  - [Steps taken to complete the project](#Steps-taken-to-complete-the-project)
    - [EDA - Data creation](#EDA---Data-creation)
      - EDA0_import_files.ipynb: Import, premieres analyse, document de synthèse 
      - EDA1_Analysis_2cities.ipynb: Analyse de la data focalisée sur 2 communes 
      - EDA2_Target.ipynb : Fichiers de noscibles 
      - Select, prepare and format data by file 
      - Integration engine merging and validating data for our models
    - [MODEL - Analysis / Exploitation of 3 Models](#MODEL---Analysis-/-Exploitation-of-3-Models)
    - [Setting up the SQL database](#Setting-up-the-SQL-database)
    - [Delivery_FRONT: Final data visualization](#Delivery_FRONT:-Final-data-visualization)
- [streamlit_app](#streamlit_app)
- [HuggingFace space](#HuggingFace-space)
- [Authors](#Authors)


## Instructions

Follow these instructions to set up the application and run it locally on your machine.

### Prerequisites

Before you begin, ensure you have met the following requirements:


- [Python 3.10.4](https://www.python.org/downloads/release/python-3104/) ou une version plus récente.
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (afin de créer un environnement virtuel).

### Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/nyxibe/HistoPolitik_2.git
```

2. Navigate to the project directory:
```bash
cd HistoPolitik_2
```

3. Create a virtual environment (recommended):
```bash
virtualenv venv
```

4. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS and Linux:
```bash
source venv/bin/activate
```

5. Install the required dependencies:
```bash
pip install -r requirements_dev.txt
```
## Steps taken to complete the project

### EDA - Data creation

Due to the size of the original data, it does not appear on the GitHub repository (DATA_SOURCES/HCP = empty). We invite you to download the data yourself [here].(https://unehistoireduconflitpolitique.fr/telecharger.html)

#### > EDA0_import_files.ipynb:
After retrieving all files in CSV format from the website.
Construction of a dataframe cataloguing the explored files.
Import of these same files into individual dataframes, followed by analysis of dimensions, values and column exploration.
The aim is to filter these documents, identify links and, above all, build a summary file in Excel format of all the documents with :
- 1: a tab containing the list and summary of documents.
- 2: a tab with one column per file, where each line includes :
  - Column headings.
  - Range of values, for numerical data.
  - The total number of lines, as well as the number and proportion of missing values (NaN).
- 3: A tab with the same structure as the previous tab, but presenting 2 random examples.
PS: We focused on the 2022 legislative elections because :
Party structures are constantly evolving, and transcribing these changes would be too time-consuming (requiring questionable arbitration).
National structures of communes and cantons are also evolving, and working on time scales would require prolonged transcoding work.

#### > EDA1_Analysis_2cities.ipynb:
This notebook analyzes the dataframe catalog and regenerates, for each file, a dataframe reduced to the perimeter of 2 communes. This makes it possible to perform advanced analyses to validate the uniqueness or absence of line units per commune, and to create graphs.

#### > EDA2_Target.ipynb :
This notebook focuses on our target: the results of the 2022 legislative elections in communes with more than 200 registered voters. It allows us to explore the structure and form of this data, the implementation of groupings, and to observe the breakdown of votes according to the number of registered voters per commune.

#### > Select, prepare and format data by file :
After the exploration phase, it was time to build the DATA support for our models. Each source file has been treated individually in a note bearing the name "df_create_COD_NomDuFichierSource.ipynb".
This file will take as input the source file to which it refers, and will have unique 3-letter codes encoding that same source.
This notebook will filter, note and output the information concerning it to be exported for our study in a CSV file.

#### > Integration engine merging and validating data for our models:
This notebook scans the /DATA/EXPORT_CSV/ directory and processes all .csv files. Tests & actions :
- A: file name must begin with final
- B: validate number of lines
- C: header validation
- D: key validation (from list_codecommune_leg2022_200inscrits.txt)
- E: retrieve list of correct prefixes to process (file_name.split('_')[1:-1])
- F: retrieve dataframe with columns containing the desired prefixes
- G: merge on common codec column
Once all the files have been processed, our global dataframe is exported as a flat file.

### MODEL - Analysis / Exploitation of 3 Models

This directory contains all the models trained for our Data. First, build the best-performing models. Export them. Exploit the results of their predictions in 2 formats:
- Predictions for each line of the score perimeter for all referenced groups (parties).
- Export for each group the weight of each importance factor for later examination.
In concrete terms, each of us used the same data to work on a model, and was responsible for providing the 2 types of information expected in the form of SQL data or a flat file.

### Setting up the SQL database

All our input and output information will be centralized in a SQL database with the following tables:
- villes_tbl [information on towns]
- X_col_titr_tbl [table transcoding the index and name of the important feature].
- y_resultats200_tbl [list of results for legislative elections 2022, our "y"]
- data_tbl [our global data, our "X"]
For our models:
- LGB_reg200_importance_tbl [list of weights and indices for each group for model LGB]
- LGB_reg200_resultats_tbl [list of weights and indices for each group for model LGB]
- RandomF_reg200_importance_tbl
- RandomF_reg200_result_tbl
- XGBoost_reg200_importance_tbl
- XGBoost_reg200_resultats_tbl
This database will be the only DATA to be exported for the online publication of our work (production environment: streamlit).

### Delivery_FRONT: Final data visualization

Before even getting started and formatting our results, we had to observe them, analyze them and see how they could be presented. These 3 documents are the basis for this work.
- Front_france.ipynb: global data analysis
- Front_Models.ipynb: model visualization (performance/features importance)
- Front_Results.ipynb

## streamlit_app

Streamlit directory for local testing.
```bash
streamlit run Accueil.py
```
### pages allow you to :

- Home.py: Presentation of the project and sources. Also presentation of political party groupings.
- pages/Cartographie-et-Data.py : View part of the data in map form.
- pages/Predictions.py: Compare predictions and reality for all French communes with at least 200 registered voters in the 2022 legislative elections.
- pages/Models.py : Visualize factors of importance (e.g. age, diploma, number of crimes...) by political party supporting our prediction.

## HuggingFace space

In case you want to test the AI models used in this project, without having to install anything on your machine, you can take a look at the [HuggingFace Space](https://huggingface.co/spaces/Caicaire93/Histo_politik) créé pour l'occasion.

## Authors

- [NYX](https://github.com/nyxibe)
- [Caicaire93](https://github.com/Caicaire93)
- [Anouaradyel2](https://github.com/anouaradyel2)