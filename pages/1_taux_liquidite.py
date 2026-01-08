import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from data.fred import load_fred_series
from components.taux_altair import render_taux_altair
from components.spread_altair import render_spread_altair



# =========================
# PAGE HEADER
# =========================
st.header("🏦 Taux & Liquidité")

st.markdown("""
Le **marché obligataire américain** est le principal moteur du système financier mondial.  
Les taux d’intérêt et la liquidité déterminent le **coût du capital**, influencent
le crédit, et façonnent les **cycles économiques**.

Les marchés actions réagissent souvent **avec retard** aux déséquilibres
qui apparaissent d’abord sur les taux.  
C’est pourquoi l’analyse du marché obligataire est une **étape fondamentale**
avant toute lecture des marchés financiers.
""")

st.divider()


# =========================
# CONFIGURATION FRED
# =========================
SERIES_TAUX = {
    "Taux US 3M (%)": "DGS3MO",
    "Taux US 2Y (%)": "DGS2",
    "Taux US 10Y (%)": "DGS10",
}


# =========================
# CHARGEMENT DES DONNÉES
# =========================
df = pd.DataFrame()

for label, series_id in SERIES_TAUX.items():
    df[label] = load_fred_series(series_id)["value"]

# Nettoyage
df = df.dropna()
df = df[df.index >= "2000-01-01"]

# Calcul du spread
df["Spread 10Y-3M"] = df["Taux US 10Y (%)"] - df["Taux US 3M (%)"]


# =========================
# AFFICHAGE — COURBES DE TAUX
# =========================
render_taux_altair(df)

st.divider()


# =========================
# AFFICHAGE — SPREAD 10Y–3M
# =========================
render_spread_altair(df)

# =========================
# Séries TIPS (taux réels)
# =========================
SERIES_TIPS = {
    "Taux réel US 10Y (%)": "DFII10",
    "Taux réel US 5Y (%)": "DFII5",
}

df_tips = pd.DataFrame()

for label, series_id in SERIES_TIPS.items():
    df_tips[label] = load_fred_series(series_id)["value"]

df_tips = df_tips.dropna()
df_tips = df_tips[df_tips.index >= "2010-01-01"]

