import streamlit as st
st.set_page_config(layout="wide")

st.sidebar.write("- Claire PORTIER \n - Nicolas-Yves XIBERAS \n  - Anouar ADYEL CAMILLE")

st.title("M.L. & Sciences Sociales : Exploration Pratique")
st.write("Qui vote pour qui et pourquoi ?")
st.write("Comment se compose la structure sociale des électorats des différents courants et mouvements politiques ?  \n En associant : \n- le travail inédit de numérisation des données électorales et socio-économiques etablit par Julia Cagé et Thomas Piketty \n- et les outils de Machine Learning  \npourrait on prédire et/ou expliquer les résultats des différents courants politiques aux dernieres legislaties (2022) ?")



st.header("Ce site vous permet :")
link_cart = '<a href="Cartographie_et_Data" target="_self">Cartographie et Data</a>'
link_pred = '<a href="Prédictions" target="_self">Prédictions</a>'
link_model = '<a href="Modèls" target="_self">Modèles</a>'

images = ['img/NUP.PNG', 'img/ECO.PNG', 'img/ENS.PNG', 'img/LR_UDI.PNG', 'img/EXTREMD.PNG', 'img/CENTRE.PNG', 'img/OTR.PNG']

# Liste de texte associé à chaque image
textes = [
    "La Nouvelle Union populaire écologique et sociale, ou Nupes, est une coalition de partis politiques de la gauche française. \n[Codification : NUP]",
    "Partis écologiste n'ayant pas souhaités s'intégrer à la Nupes  \n[Codification : ECO]",
    "7 partis la composent initialement : La République en marche, le Mouvement démocrate, Horizons, Agir, Territoires de progrès, Parti radical et En commun. Lors des élections législatives de 2022, les candidats se présentent tous sous l'étiquette « Ensemble ! majorité présidentielle  \n[Codification : ENS]",
    "- L'Union des démocrates et indépendants (UDI) est un parti politique français de centre droit, fondé par Jean-Louis Borloo le 21 octobre 2012, à partir du groupe parlementaire du même nom à l'Assemblée nationale. Jusqu'en 2018, l'UDI est composée de différents partis qui conservent leur existence, formant ainsi une fédération de partis. Se voulant comme la continuatrice des idées de l'UDF, son orientation est social-libérale, démocrate chrétienne et pro-européenne. \n - Les Républicains (LR) est un parti politique français, classé à droite sur l'échiquier politique. Issu en 2015 du changement de nom et de statuts de l'Union pour un mouvement populaire (UMP), fondé en 2002, il s'inscrit dans la continuité des grands partis conservateurs et gaullistes français : UNR, UDR, RPR et UMP. \n[Codification : LR_UDI]",
    "- Reconquêtea (R! ou REC29) est un parti politique français d'extrême droite. Fondé en avril 2021 dans la perspective de soutenir la candidature d'Éric Zemmour à l'élection présidentielle de 2022. \n - Le Rassemblement national (RN) — Front national (FN) jusqu'en 2018 — est un parti politique français d'extrême droite présidé par Jean-Marie Le Pen (1972-2011), Marine Le Pen (2011-2021) puis Jordan Bardella depuis septembre 2021. . \n[Codification : EXTREMD]",
    "Partis Centristes ayant souhaités restés indépendants.  \n[Codification : CENTRE]",
    "Autres partis (beaucoup d'indépendentistes notamment en Corse)  \n[Codification : OTR]"    
]



st.write(f'- Visualiser nos données sous forme de cartes [{link_cart}]', unsafe_allow_html=True)
st.write(f'- Comparer nos prédictions et la realités sur toutes les communes de France qui disposaient d\'au moins de 200 inscrits lors des éléctions législatives de 2022 [{link_pred}]', unsafe_allow_html=True)
st.write(f'- Visualiser les facteurs d\'importances par partis politiques support à notre prédiction [{link_model}]', unsafe_allow_html=True)

st.header("Les Sources")
st.image("img/UneHistoireDuConflitPolitique0.PNG")
# Créer un lien autour de l'image pour ouvrir dans une nouvelle fenêtre
st.markdown(f'<a href="https://unehistoireduconflitpolitique.fr" target="_blank">unehistoireduconflitpolitique.fr</a>', unsafe_allow_html=True)
st.write("Un travail inédit de numérisation des données électorales et socio-économiques couvrant plus de deux siècles. Toutes les données collectées au niveau des quelques 36 000 communes de France sont disponibles en ligne en accès libre sur ce site, qui comprend des centaines de cartes, graphiques et tableaux interactifs. ")

st.header("Les partis politiques : nos regroupements")
# Création du tableau
for i in range(7):
    st.image(images[i], width=225)
    st.write(textes[i])
    st.write("---")  # Ligne horizontale pour séparer les entrées du tableau        
    

st.header("L'emission à l'origine du projet")
st.image('img/UneHistoireDuConflitPolitique1.PNG')
# Créer un lien autour de l'image pour ouvrir dans une nouvelle fenêtre
st.markdown(f'<a href="https://www.thinkerview.com/julia-cage-et-thomas-piketty-deux-economistes-sous-stress-test/" target="_blank">Julia Cagé et Thomas Piketty sur THINKERVIEW</a>', unsafe_allow_html=True)

st.subheader("Nous contacter")
# Afficher le lien de contact avec mailto
st.markdown(f" - [Nicolas-Yves](mailto:{'nicolasyves@gmail.com'})")
