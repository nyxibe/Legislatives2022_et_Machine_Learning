import streamlit as st
st.set_page_config(layout="wide")

import sqlite3
import numpy as np

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

DB_filpath = '../DATA/HistoPlotik.db'

# DATA

titr_part = ['NUP', 'ECO', 'ENS', 'LR_UDI', 'EXTREMD', 'CENTRE', 'OTR']

dico_perf = {'mse_moy': [0.011047658221418547, 0.00045765054495667303, 0.010372182986578304, 0.015036222494032608, 0.011667350420367715, 0.010671522614056612, 0.0035062020754255247], 'LGB_reg200': [0.0033958852315906503, 0.0002443474564698635, 0.004143222765996065, 0.006946201984190602, 0.0028293664323298167, 0.004622804941894148, 0.00047806641343941587], 'XGBoost_reg200': [0.002190349018291624, 0.00019058591708881516, 0.002737929451386264, 0.004938271011016184, 0.0018107279166872854, 0.003415542751482656, 0.0004289619852793093], 'RandomF_reg200': [0.0018771754150696829, 0.00014310619048045286, 0.0017846895966924503, 0.004673477002255421, 0.0011821959903784592, 0.0029879500168552217, 0.00029222167578787223]}

dico_perf_moy = {'mse_moy': 0.008965541336690854, 'LGB_reg200': 0.0032371278894157947, 'XGBoost_reg200': 0.0022446240073188766, 'RandomF_reg200': 0.0018486879839313658}


def prefix_transco (prefix) :
    dico_prefix_transco = {
        'KP0':'capital immobilier dans la commune fichier 1/2','BFL':'Bases FiscaLes de la commune','TER':'TERres surface agriculteurs dans la commune','KP1':'capital immobilier dans la commune fichier 2/2','RSA':'personnes au RSA dans la commune','CED':'Crimes Et Delits dans la commune','EMP':'EMPloies dans la communes','CSP':'Classification CSP dans la commune','PUB':'PUBlic prive dans la commune en 2021','PRO':'PROprietaires dans la commune','DIP':'DIPlomés dans la commune','PO0':'POp commune selecteurs fichier 1/2','PO1':'POp commune selecteurs fichier 2/2','NAT':'NATionalités dans la commune','ETR':'ETRANGERS dans la communes','REV':'REVenus dans la commune','PIB':'PIB commune','AGE':'AGE et Sexe population de la commune','YYY':'Données ciblées','TAR':'Données de notre fichier resultats'}
    if prefix in dico_prefix_transco :
        return dico_prefix_transco[prefix]
    else : 
        return 'prefix N.R.'



# PAGE
st.title("3 modeles : Performances")    
# Créer des sections avec des ancres
st.header("Comparaisons des performances \n De nos 3 modeles contre moy. nationale")

models = list(dico_perf.keys())
mse_values = list(dico_perf.values())

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

for i, model in enumerate(models):
    ax.bar([j + i * 0.2 for j in range(len(mse_values[0]))], mse_values[i], width=0.2, label=model)

    # Add a line for the mean MSE
    ax.axhline(y=dico_perf_moy[model], color=f'C{i}', linestyle='--', label=f'Mean MSE ({model})')

ax.set_xticks([j + 0.3 for j in range(len(mse_values[0]))])
ax.set_xticklabels(titr_part)
ax.set_ylabel('Mean Squared Error (MSE)')
ax.set_title('MSE Comparison for Different Models')

# Show legend
ax.legend()

# Show the plot
st.pyplot(fig)

# Autre texte
st.write("Random Forest meilleur partout mais attention au surapprentissage \n Nous utiliserons XGBoost")

# Sous-titre équivalent à <h2>
st.subheader("En chiffres")


# Création d'une liste de listes représentant un tableau
tab_perf = []

for i, p in enumerate(titr_part):
    tab_perf.append([
        p,
        dico_perf['mse_moy'][i],
        dico_perf['RandomF_reg200'][i],
        dico_perf['mse_moy'][i] / dico_perf['RandomF_reg200'][i],
        dico_perf['XGBoost_reg200'][i],
        dico_perf['mse_moy'][i] / dico_perf['XGBoost_reg200'][i],
        dico_perf['LGB_reg200'][i],
        dico_perf['mse_moy'][i] / dico_perf['LGB_reg200'][i]
    ])   

# Création d'un dataframe Pandas à partir de la liste de listes
df = pd.DataFrame( tab_perf, columns=['partie politique','mse_moy','Random forest','RF / mse_moy','XGBoost','XGB /mse_moy','LGB','LGB / mse_moy'])

# Affichage du tableau dans Streamlit avec les titres de colonnes et lignes
st.table(df)


st.header("features Importance")
# Affichage du titre du tableau



def importance_graf(db_path, model_tbl, cat='NUP', size=15):
    connection = sqlite3.connect(db_path)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query for the join
    col_value = f"{cat}_import"
    col_indice_var = f"{cat}_estim_indice"

    # Use string formatting to insert variable values into the query
    sql_query = f"""
    SELECT 
        C.titr_col_value,
        FI.{col_value}
    FROM     
        {model_tbl} FI
        JOIN X_col_titr AS C ON C.indice = FI.{col_indice_var}
    ORDER BY 
        FI.{col_value} DESC
    LIMIT {size}
    """

    # Execute the SQL query and fetch the result into a DataFrame
    imp_df = pd.read_sql_query(sql_query, connection)   

    # Plotting
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.bar(imp_df['titr_col_value'], imp_df[col_value], color='skyblue', edgecolor='black')
    ax.set_xticklabels(imp_df['titr_col_value'], rotation='vertical')
    ax.set_xlabel('Columns')
    ax.set_ylabel('Importance')
    ax.set_title(f'{model_tbl[0:-15]} & {cat} : {size} first features Importance Histogram')
    plt.tight_layout()

    # Close the database connection
    connection.close()
    txt_write = ''
    for i in range (0,6) :
        txt_write+=imp_df['titr_col_value'][i]+' | '
    st.write(txt_write)
    return fig, ax

def importance_distrib_graf (db_path, model_tbl, cat='NUP') :
    connection = sqlite3.connect(db_path)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query for the join
    col_value = f"{cat}_import"
    col_indice_var = f"{cat}_estim_indice"

    # Use string formatting to insert variable values into the query
    sql_query = f"""
        SELECT 
            SUBSTR(C.titr_col_value, 1, 3) AS col_value_prefix,
            AVG(FI.{col_value}) AS avg_col_value
        FROM     
            {model_tbl} FI
            JOIN X_col_titr AS C ON C.indice = FI.{col_indice_var}
        GROUP BY 
            col_value_prefix
        ORDER BY 
            avg_col_value
    """
    sql_query = f"""
        SELECT 
        SUBSTR(C.titr_col_value, 1, 3) AS col_value_prefix,
        SUM(FI.{col_value}) AS sum_col_value
    FROM     
        {model_tbl} FI
        JOIN X_col_titr AS C ON C.indice = FI.{col_indice_var}
    GROUP BY 
        col_value_prefix
    ORDER BY 
        sum_col_value DESC
    """

    # print(sql_query)
    # Execute the SQL query and fetch the result into a DataFrame
    imp_df = pd.read_sql_query(sql_query, connection) 
    # df_tri = imp_df['avg_col_value'].sort_values(ascending=False)

    # Plotting Pie Chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(imp_df['sum_col_value'], labels=imp_df['col_value_prefix'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(f'{model_tbl[0:-15]} & {cat} Importance Distribution')

    # Close the database connection
    txt_write = ''
    connection.close()
    for i in range (1,4) :
        txt_write+="- "+prefix_transco (imp_df['col_value_prefix'][i])+"\n"
    st.write(txt_write)
    return fig, ax


model_tbl_list = ['XGBoost_reg200_importance_tbl','LGB_reg200_importance_tbl','RandomF_reg200_importance_tbl']
for model_tbl in model_tbl_list :
    st.subheader(model_tbl[0:-22]) 
    # Layout using st.beta_columns
    for part in titr_part:
        image_path = 'img/'+part+'.PNG'
        st.image(image_path, width=150)

        # Create two columns
        col1, col2 = st.columns([2, 1])

        # Plot histogram for XGBoost in the left column
        with col1:
            fig_xgboost, ax_xgboost = importance_graf(DB_filpath, model_tbl, cat=part)
            fig_xgboost.set_size_inches(15, 9)  # Adjust the figure size
            st.pyplot(fig_xgboost)

        # Plot histogram for LGB in the right column
        with col2:
            fig_lgb, ax_lgb = importance_distrib_graf(DB_filpath, model_tbl, cat=part)
            fig_lgb.set_size_inches(10, 9)  # Adjust the figure size
            st.pyplot(fig_lgb)
        
    st.markdown("---")


