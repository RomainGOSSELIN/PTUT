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

# Titre - Résultat
st.title("Résultats", anchor = None)

# Sélection des lignes selon le respect des critères
df_restreint = df.loc[(df["Diplôme délivré"] == (diplome)) & (df["Région"] == (region))]

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
st.download_button(label='✅ Télécharger le résultatt', data = liste_formations, file_name = 'liste_formations.xlsx')