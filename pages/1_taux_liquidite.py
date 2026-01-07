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

st.markdown(
    """
Cette page analyse les **taux d’intérêt américains** et leur rôle
dans le **cycle macroéconomique**.

Les taux courts reflètent la politique monétaire,  
les taux longs anticipent la croissance future.
"""
)

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
