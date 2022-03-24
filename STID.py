import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

# Paramètres de la page
st.set_page_config(page_title = "STID ET APRES ?", page_icon = "🎓")
st.image("IMG/graduation_hat.png", width = 100)
st.title("STID ET APRES ?")

# Importation de la DB
df = pd.read_excel("formations.xlsx", header = 0)

# Titre - Critères
st.title("Critères", anchor = None)

# Critères de recherche
region = st.selectbox("Région 📍", df["Région"].unique())
diplome = st.selectbox("Diplôme délivré 🏆", df["Diplôme délivré"].unique())
statut = st.selectbox("Statut 💼", df["Statut"].unique())

# Titre - Résultat
st.title("Résultats", anchor = None)

# Sélection des lignes selon le respect des critères
df_restreint = df.loc[(df["Diplôme délivré"] == (diplome)) & (df["Région"] == (region)) & (df["Statut"] == (statut))]

# Affichage du dataframe restreint
st.dataframe(df_restreint)

# Fonction de conversion DF -> XLSX
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine = 'xlsxwriter')
    df.to_excel(writer, index = False, sheet_name = 'Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
liste_formations = to_excel(df_restreint)

# Bouton de téléchargement du résultat
st.download_button(label='✅ Télécharger le résultat', data = liste_formations, file_name = 'liste_formations.xlsx')

# Titre - Questionnaire
st.title("Questionnaire", anchor = None)

with st.container():
    prenom = st.text_input("Indiquez votre prénom :")
    nom = st.text_input("Indiquez votre nom :")
    bac = st.radio("Quel Bac avez-vous fait ?",("Bac S (ou équivalent)", "Bac ES (ou équivalent)", "Bac L (ou équivalent)", "Bac STI2D", "Bac Professionnel", "Autre"))
    mention = st.radio("Quelle a été votre mention ? ",("Très Bien", "Bien", "Assez Bien", "Sans mention"))
    choix = st.text_input("Pourquoi avoir choisi STID et spécialement celui d'Aurillac ?")
    integration = st.radio("Avez-vous intégré STID :", ("Directement après le Bac", "1 an après le Bac", "2 ans après le Bac", "3 ans ou plus après le Bac"))
    stage = st.text_input("Dans quelle entreprise avez-vous effectué votre stage de fin de DUT ?")
    satisfaction_STID = st.select_slider("A quel point avez-vous apprécié le DUT STID", options = ["Pas du tout", "Pas vraiment", "Moyennement", "Plutôt", "Énormément"])
        
    poursuite = st.radio("Que faites-vous actuellement ?", ("École d'ingénieur (en initial)", "École d'ingénieur (en alternance)", "Licence puis Master", "Licence professionelle", "Vie Active", "Autre"))
    if poursuite == "École d'ingénieur (en initial)" or poursuite == "École d'ingénieur (en alternance)" or poursuite == "Licence puis Master" or poursuite == "Licence professionelle":
        statut = st.text_input("Quel est l'intitulé de votre formation ?")
        ville = st.text_input("Dans quelle se déroule cette formation ?")
        choix = st.radio("Avez-vous été accepté dans la formation que vous préfériez ?", ("Oui", "Non"))
        satisfaction_formation = st.radio("Êtes-vous satisfait de votre formation actuelle ?", ("Oui", "Moyennement", "Non"))
        metier = st.text_input("Quel métier voudriez-vous faire après vos études ?")
    elif poursuite == "Vie Active":
        statut = st.text_input("Dans quelle entreprise travaillez-vous ?")
        ville = st.text_input("Précisez la ville où vous travaillez")
        metier = st.text_input("Quel poste occupez-vous ?")
    elif poursuite == "Autre":
        statut = st.text_input("Précisez votre réponse")

    recommandation = st.radio("Recommanderiez-vous STID à d'autres personnes ?", ("Oui", "Non"))
    if recommandation == "Non":
        pourquoi = st.text_input("Pourquoi ?")

    contact = st.text_input("Donnez-nous un moyen de vous recontacter pour de futurs forums d'anciens étudiants par exemple")
    autorisation = st.checkbox("Autorisez-vous l'utilisation et le traitement de vos données personnelles dans le but d'une analyse statistique ? (Les données personnelles telles que les notes et noms seront bien sûr anonymisées)")