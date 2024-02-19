import streamlit as st
st.set_page_config(layout="wide")
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn.preprocessing import MinMaxScaler
import matplotlib.colors as mcolors
from matplotlib.colors import PowerNorm

st.title('Des données encore des données')
st.set_option('deprecation.showPyplotGlobalUse', False)

DB_filpath = '../DATA/HistoPlotik.db'

st.subheader("Résultats législatives 2022")

options_resultats = ['NUP', 'ENS', 'LR_UDI', 'EXTREMD', 'CENTRE', 'OTR']

# Sélection des résultats des législatives
resultats_selectionnes = st.radio("Sélectionnez le parti politique qui vous intéresse", options_resultats)
button = st.button("click")
if button:
    conn = sqlite3.connect(DB_filpath)
    query = """
        SELECT 
            V.latitude, 
            V.longitude,
            R.*
        FROM 
            villes_tbl V
            JOIN y_resultats200_tbl R ON V.key = R.key
        ;
    """.format(','.join(resultats_selectionnes))

    data = pd.read_sql_query(query, conn)

    conn.close()

    # Normalize the data between 0 and 1 for color mapping
    scaler = MinMaxScaler()
    data[resultats_selectionnes] = scaler.fit_transform(data[[resultats_selectionnes]])

    # Scatter plot with Matplotlib
    plt.figure(figsize=(10, 8))

    # Scatter plot with small points, alpha, and reversed color scale
    scatter = plt.scatter(
        data['longitude'],
        data['latitude'],
        s=5,
        alpha=0.8,
        c=data[resultats_selectionnes],
        cmap='viridis_r',  # Reversed viridis colormap
    )

    plt.colorbar(scatter, label=resultats_selectionnes)

    plt.axis('off')
    plt.title('Scatter Plot with Alpha and {}'.format(resultats_selectionnes))

    # Show the plot
    st.pyplot()


st.subheader("Sélectionner une colonne de la table data_tbl")
conn = sqlite3.connect(DB_filpath)
data_columns_names = ['AGE_poph014_12','DIP_supf2017','CED_nvolsvoitures2016','CED_ncambriolages2016', 'CED_nvolsvoitures2020','CED_ncambriolages2020','KP1_prixbien02','KP1_prixbien12','REV_revmoyfoy2022','REV_revmoyfoy2012']
name_selection = st.selectbox("Sélectionner une colonne", data_columns_names)
button2 = st.button("Afficher les données sur une carte")

# Si le bouton est cliqué pour afficher les données en fonction de la colonne
if button2:
    conn = sqlite3.connect(DB_filpath)
    query = f"""
        SELECT 
            V.latitude, 
            V.longitude,
            D.AGE_poph014_12 ,D.DIP_supf2017,D.CED_nvolsvoitures2016,D.CED_ncambriolages2016, D.CED_nvolsvoitures2020,D.CED_ncambriolages2020,D.KP1_prixbien02,D.KP1_prixbien12,D.REV_revmoyfoy2022,D.REV_revmoyfoy2012
        FROM 
            villes_tbl V
            JOIN data_tbl D ON V.key = D.key
        ;
    """

    data = pd.read_sql_query(query, conn)

    conn.close()
    # Ajustez la normalisation des couleurs
    norm = PowerNorm(gamma=0.6)  # Ajustez gamma pour changer la dynamique du dégradé
    norm = colors.Normalize(data[name_selection].min(), data[name_selection].quantile(0.75))
    plt.figure(figsize=(10, 8))

    scatter = plt.scatter(
        data['longitude'],
        data['latitude'],
        s=5,
        alpha=0.8,
        c=data[name_selection],
        cmap='viridis_r',
        norm=norm,
    )

    plt.colorbar(scatter, label=name_selection)

    plt.axis('off')
    plt.title('Scatter Plot with Alpha and {}'.format(name_selection))

    # Afficher le graphique
    st.pyplot()