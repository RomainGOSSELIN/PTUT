import streamlit as st
import pandas as pd

# Paramètres de la page
st.set_page_config(page_title = "STID ET APRES ?", page_icon = "🎓")
st.image("IMG/graduation_hat.png", width = 100)
st.title("STID ET APRES ?")

# Importation de la DB
df = pd.read_excel("formations.xlsx", header = 0)

# Titre - Critères
st.title("Critères", anchor = None)
region = st.selectbox("Région 📍", df["Région"].unique())
diplome = st.selectbox("Diplôme délivré 🏆", df["Diplôme délivré"].unique())

# Titre - Résultat
st.title("Résultats", anchor = None)

df_restreint = df.loc[(df["Diplôme délivré"] == (diplome)) & (df["Région"] == (region))]

st.dataframe(df_restreint)