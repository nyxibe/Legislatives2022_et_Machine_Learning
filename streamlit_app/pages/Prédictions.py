import streamlit as st
st.set_page_config(layout="wide")
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

DB_filpath = '../DATA/HistoPlotik.db'
def pouce_aff (value, size=70) :
    if value < 0.95 :
        img='nil'
    else : 
        if value > 1.05 : 
            img ='good'
        else : 
            img = 'medium'
    image_path = 'img/'+img+'.PNG'
    st.image(image_path, width=size)
    
def prefix_transco (prefix) :
    dico_prefix_transco = {
        'KP0':'capital immobilier dans la commune fichier 1/2','BFL':'Bases FiscaLes de la commune','TER':'TERres surface agriculteurs dans la commune','KP1':'capital immobilier dans la commune fichier 2/2','RSA':'personnes au RSA dans la commune','CED':'Crimes Et Delits dans la commune','EMP':'EMPloies dans la communes','CSP':'Classification CSP dans la commune','PUB':'PUBlic prive dans la commune en 2021','PRO':'PROprietaires dans la commune','DIP':'DIPlomés dans la commune','PO0':'POp commune selecteurs fichier 1/2','PO1':'POp commune selecteurs fichier 2/2','NAT':'NATionalités dans la commune','ETR':'ETRANGERS dans la communes','REV':'REVenus dans la commune','PIB':'PIB commune','AGE':'AGE et Sexe population de la commune','YYY':'Données ciblées','TAR':'Données de notre fichier resultats'}
    if prefix in dico_prefix_transco :
        return dico_prefix_transco[prefix]
    else : 
        return 'prefix N.R.'


def afficher_informations_commune(selected_nom):
    conn = sqlite3.connect(DB_filpath)
    cursor = conn.cursor()

    # Exécuter une requête SQL pour récupérer la clé de la commune sélectionnée dans la table villes_tbl
    cursor.execute('SELECT key FROM villes_tbl WHERE nomcommune = ?', (selected_nom,))
    key = cursor.fetchone()[0]  # Récupérer la clé (premier élément de la première ligne)

    conn.close()

    if key:
        conn = sqlite3.connect(DB_filpath)
        query = """
          SELECT 
              V.codepostale, V.nomregion, V.latitude, V.longitude, V.superficie, 
              R.*,
              XGB.pred_NUP AS XGB_NUP, XGB.pred_ECO AS XGB_ENS, XGB.pred_LR_UDI AS XGB_LR_UDI,  
              XGB.pred_EXTREMD AS XGB_EXTREMD,  XGB.pred_CENTRE as XGB_CENTRE, XGB.pred_OTR AS XGB_OTR,
              LGB.pred_NUP AS LGB_NUP, LGB.pred_ECO AS LGB_ENS, LGB.pred_LR_UDI AS LGB_LR_UDI,  
              LGB.pred_EXTREMD AS LGB_EXTREMD,  LGB.pred_CENTRE as LGB_CENTRE, LGB.pred_OTR AS LGB_OTR,
              RF.pred_NUP AS RF_NUP, RF.pred_ECO AS RF_ENS, RF.pred_LR_UDI AS RF_LR_UDI,  
              RF.pred_EXTREMD AS RF_EXTREMD,  RF.pred_CENTRE as RF_CENTRE, RF.pred_OTR AS RF_OTR,
              0.26780330618314363 AS moy_NUP,
              0.026840317879397668 AS moy_ECO,
              0.2613130117529952 AS moy_ENS,
              0.12340510077085327 AS moy_LR_UDI,
              0.23044994449024447 AS moy_EXTREMD,
              0.062083856325418664 AS moy_CENTRE,
              0.028104462597947067 AS moy_OTR,
              D.*
          FROM 
              villes_tbl V,
              y_resultats200_tbl R,
              XGBoost_reg200_resultats_tbl XGB,
              LGB_reg200_resultats_tbl LGB,
              RandomF_reg200_resultats_tbl RF,
              data_tbl D
          WHERE 
              V.key = ?
              AND R.key = V.key
              AND XGB.key = V.key
              AND LGB.key = V.key
              AND RF.key = V.key
              AND D.key = V.key
          ;
        """
        data = pd.read_sql_query(query, conn, params=(key,))

        conn.close()

        st.markdown(f"<h1 id='info_syn'>{selected_nom}</h1>", unsafe_allow_html=True)

        data_info = data[['codepostale', 'nomregion', 'superficie', 'nomdep', 'TAR_inscrits', 'TAR_exprimes', 'AGE_pop_22']]
        st.write(data_info)

        st.markdown("<h1 id='pred'>Prédictions</h1>", unsafe_allow_html=True)

        scorelist = ['NUP','ENS','LR_UDI','EXTREMD','CENTRE','OTR']
        scorelist_XGB = ['XGB_NUP','XGB_ENS','XGB_LR_UDI','XGB_EXTREMD','XGB_CENTRE','XGB_OTR']
        scorelist_LGB = ['LGB_NUP','LGB_ENS','LGB_LR_UDI','LGB_EXTREMD','LGB_CENTRE','LGB_OTR']
        scorelist_RF = ['RF_NUP','RF_ENS','RF_LR_UDI','RF_EXTREMD','RF_CENTRE','RF_OTR']
        scorelist_moy = ['moy_NUP','moy_ENS','moy_LR_UDI','moy_EXTREMD','moy_CENTRE','moy_OTR']



        values1 = data[scorelist].values[0]
        values2 = data[scorelist_RF].values[0] 
        values3 = data[scorelist_moy].values[0]

        mse_values1_values2 = mean_squared_error(values1, values2)
        mse_values1_values3 = mean_squared_error(values1, values3)
        perf = mse_values1_values3/mse_values1_values2
        pouce_aff(perf)

        fig, axs = plt.subplots(1, 3, figsize=(20, 8))

        # Plot the first pie chart
        axs[0].pie(values1, labels=scorelist , autopct='%1.1f%%', startangle=90)
        axs[0].set_title('REALITE' ,fontsize=22)

        # Plot the second pie chart
        axs[1].pie(values2, labels=scorelist, autopct='%1.1f%%', startangle=90)
        axs[1].set_title(f'RF PREDICT\n(mse {mse_values1_values2:.2e})', fontsize=20)

        # Plot the third pie chart
        axs[2].pie(values3, labels=scorelist, autopct='%1.1f%%', startangle=90)
        axs[2].set_title(f'Moyenne Nationale \n(mse {mse_values1_values3:.2e})', fontsize=20)
        # Global title
        # plt.suptitle(f'MSE moy divisé par {perf:.1f}\n', fontsize=22)


        # Adjust layout
        plt.tight_layout()

        st.pyplot(fig)

        all_values = np.vstack([values1, values2, values3])

        # Create a figure for the grouped bar chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotting
        models = ['REALITE', f'RF PREDICT mse \n(mse {mse_values1_values2:.2e})', f'Moyenne Nationale \n(mse {mse_values1_values3:.2e})']  # You can adjust model names
        bar_width = 0.2

        for i, model in enumerate(models):
            ax.bar([j + i * bar_width for j in range(len(all_values[0]))], all_values[i], width=bar_width, label=model)

        # Add a line for the mean value
        # ax.axhline(y=np.mean(all_values), color='black', linestyle='--', label='Mean Value')

        ax.set_xticks([j + bar_width * (len(models) - 1) / 2 for j in range(len(scorelist))])
        ax.set_xticklabels(scorelist)
        ax.set_ylabel('Values')
        # ax.set_title(f'MSE moyen')
                # Global title
        plt.suptitle(f'MSE moy divisé par {perf:.1f}\n', fontsize=10)


        ax.legend()
        st.pyplot(fig)

        # TEST MSE SANS ENSEMBLE
        values1_dropENS = np.delete(values1, 1)
        values2_dropENS = np.delete(values2, 1)
        values3_dropENS = np.delete(values3, 1)

        mse_values1_values2_dropENS = mean_squared_error(values1_dropENS, values2_dropENS)
        mse_values1_values3_dropENS = mean_squared_error(values1_dropENS, values3_dropENS)

        perf_dropENS = mse_values1_values3_dropENS/mse_values1_values2_dropENS
        pouce_aff(perf_dropENS,35)

        st.write('SANS ENS : ',mse_values1_values2_dropENS, ' / ', mse_values1_values3_dropENS)
        st.write('(facteur :',mse_values1_values3_dropENS/mse_values1_values2_dropENS,') ')
        
        st.markdown("<h1 id='loc'>Localisation</h1>", unsafe_allow_html=True)
        
        fig = px.scatter_geo(data, lat='latitude', lon='longitude',
                            scope='europe', labels={'nomcommune': 'Nome de la commune'})
        fig.update_geos(projection_type="natural earth", scope="europe", center=dict(lat=46, lon=2), lataxis_range=[41, 52], lonaxis_range=[-5, 10])

        st.plotly_chart(fig)

        def importance_graf(DB_filpath, model_tbl, cat, size=15):
            connection = sqlite3.connect(DB_filpath)

            cursor = connection.cursor()

            # Define the SQL query for the join
            col_value = f"{cat}_import"
            col_indice_var = f"{cat}_estim_indice"

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
            ax.set_xticklabels(imp_df['titr_col_value'], rotation=75, fontsize=16)
            ax.set_ylabel('Importance', fontsize=16)
            ax.set_title(f'{cat} : {size} first features Importance Histogram', fontweight='bold', fontsize=16)
            plt.tight_layout()

            connection.close()

            txt_write = ''
            for i in range (0,6) :
                txt_write+=imp_df['titr_col_value'][i]+' | '
            st.write(txt_write)
            return fig, ax
        
        def importance_distrib_graf (DB_path, model_tbl, cat) :
            connection = sqlite3.connect(DB_path)

            cursor = connection.cursor()

            # Define the SQL query for the join
            col_value = f"{cat}_import"
            col_indice_var = f"{cat}_estim_indice"
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

            # Execute the SQL query and fetch the result into a DataFrame
            imp_df = pd.read_sql_query(sql_query, connection)   

            # Plotting Pie Chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(imp_df['sum_col_value'], labels=imp_df['col_value_prefix'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f'{cat} Importance Distribution')

            connection.close()

            txt_write = ''
            for i in range (1,5) :
                # OLD txt_write+=imp_df['col_value_prefix'][i]+' | '
                txt_write+="- "+prefix_transco (imp_df['col_value_prefix'][i])+"\n"
            st.write(txt_write)
            return fig, ax

        st.header('Infos du partis gagnant')
        colonne_max = max(scorelist, key=lambda col: data[col].iloc[0])
        model_tbl_list = ['XGBoost_reg200_importance_tbl']
        for model in model_tbl_list :
            image_path = 'img/'+colonne_max+'.PNG'
            st.image(image_path, width=150)

            col1, col2 = st.columns([2, 1])
            with col1:
                fig_xgboost, ax_xgboost = importance_graf(DB_filpath, model, cat=colonne_max)
                fig_xgboost.set_size_inches(15, 9)
                st.pyplot(fig_xgboost)
            
            with col2:
                fig_lgb, ax_lgb = importance_distrib_graf(DB_filpath, model, cat=colonne_max)
                fig_lgb.set_size_inches(10, 9)
                st.pyplot(fig_lgb)


        current_prefix ='   '
        for c in data.columns:
            prefix = c[0:3]
            if prefix != current_prefix:
                st.markdown(f"<h2>{prefix}</h2>", unsafe_allow_html=True)
                current_prefix = prefix
            st.write(f"{c}: {data.iloc[0][c]}")


        def importance_graf2(db_path, model_tbl, cat, size=15):
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
            ax.set_xticklabels(imp_df['titr_col_value'], rotation=75, fontsize=16)
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

        def importance_distrib_graf2 (db_path, model_tbl, cat) :
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

            # Plotting Pie Chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(imp_df['sum_col_value'], labels=imp_df['col_value_prefix'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f'{model_tbl[0:-15]} & {cat} Importance Distribution')

            # Close the database connection
            connection.close()
            txt_write = ''
            for i in range (1,5) :
                txt_write+="- "+prefix_transco (imp_df['col_value_prefix'][i])+"\n"
            st.write(txt_write)
            return fig, ax


    st.markdown("<h2 id='section2'>Tous les facteurs importants par Partis</h2>", unsafe_allow_html=True)

    model_tbl_list = ['XGBoost_reg200_importance_tbl']
    for model_tbl in model_tbl_list :
        st.subheader(model_tbl[0:-22]) 
        # Layout using st.beta_columns
        for part in scorelist:
            image_path = 'img/'+part+'.PNG'
            st.image(image_path, width=150)

            # Create two columns
            col1, col2 = st.columns([2, 1])

            # Plot histogram for XGBoost in the left column
            with col1:
                fig_xgboost, ax_xgboost = importance_graf2(DB_filpath, model_tbl, cat=part)
                fig_xgboost.set_size_inches(15, 9)  # Adjust the figure size
                st.pyplot(fig_xgboost)

            # Plot histogram for LGB in the right column
            with col2:
                fig_lgb, ax_lgb = importance_distrib_graf2(DB_filpath, model_tbl, cat=part)
                fig_lgb.set_size_inches(10, 9)  # Adjust the figure size
                st.pyplot(fig_lgb)

        



# Code Streamlit
st.title("Données connues sur les communes")

st.header("Qu'elle commune vous intéresse?")
user_text = st.text_input("Entrez le code postal")
if st.button("Rechercher par code postal"):
    conn = sqlite3.connect(DB_filpath)
    cursor = conn.cursor()

    # Exécuter une requête SQL pour récupérer le nom de la commune basé sur le code postal
    cursor.execute('SELECT nomcommune FROM villes_tbl WHERE codepostale = ?', (user_text,))
    selected_nom = cursor.fetchone()[0]  # Récupérer le nom de la commune

    conn.close()

    afficher_informations_commune(selected_nom)

conn = sqlite3.connect(DB_filpath)
# Charger les noms de communes depuis la table villes_tbl
query = "SELECT nomcommune FROM villes_tbl"
communes_data = pd.read_sql_query(query, conn)

# Fermer la connexion à la base de données
conn.close()

# Récupérer la liste des noms de communes
communes = communes_data['nomcommune'].tolist()

user_commune = st.text_input("Ou, entrez le nom de la commune")
suggestions = [nom for nom in communes if user_commune.lower() in nom.lower()]
selected_nom = st.selectbox("Suggestions :", suggestions)
if st.button("Rechercher par nom de commune"):
    afficher_informations_commune(selected_nom)
