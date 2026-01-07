import streamlit as st
import pandas as pd
import requests

st.header("🏦 Taux & Liquidité")

st.markdown("""
Analyse des taux d’intérêt américains à partir des données officielles FRED.
Ce bloc constitue la fondation du cycle macroéconomique.
""")

# -------------------------
# Configuration FRED
# -------------------------
SERIES = {
    "Taux US 2Y (%)": "DGS2",
    "Taux US 10Y (%)": "DGS10"
}

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

@st.cache_data
def load_fred_series(series_id):
    params = {
        "series_id": series_id,
        "api_key": None,          # clé non obligatoire pour usage simple
        "file_type": "json"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()["observations"]
    df = pd.DataFrame(data)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")

# Chargement des données
df = pd.DataFrame()

for label, series_id in SERIES.items():
    series = load_fred_series(series_id)
    df[label] = series["value"]

df = df.dropna()

# -------------------------
# Affichage
# -------------------------
st.subheader("Évolution des taux US (2Y vs 10Y)")
st.line_chart(df)
