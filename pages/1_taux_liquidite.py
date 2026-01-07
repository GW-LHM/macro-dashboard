import streamlit as st
import pandas as pd

from data.fred import load_fred_series
from components.taux_us import render_taux_us
from components.spread import render_spread
from components.fred_spread_embed import render_fred_spread
from components.spread_altair import render_spread_altair


st.header("🏦 Taux & Liquidité")

st.divider()
render_spread_altair(df)

st.markdown("""
Cette page analyse les taux d’intérêt américains et leur impact
sur le cycle économique et les marchés financiers.
""")


# =========================
# Séries FRED
# =========================
SERIES = {
    "Taux US 3M (%)": "DGS3MO",
    "Taux US 2Y (%)": "DGS2",
    "Taux US 10Y (%)": "DGS10"
}

SERIES_SP500 = "SP500"


# =========================
# Chargement des données
# =========================
df = pd.DataFrame()

for label, series_id in SERIES.items():
    df[label] = load_fred_series(series_id)["value"]

df = df.dropna()
df = df[df.index >= "2000-01-01"]

df["Spread 10Y-3M"] = df["Taux US 10Y (%)"] - df["Taux US 3M (%)"]


sp500 = load_fred_series(SERIES_SP500)
sp500 = sp500.rename(columns={"value": "S&P 500"})


# =========================
# Inversions mensuelles
# =========================
df_monthly = df[["Spread 10Y-3M"]].resample("M").mean()

inversion_monthly = df_monthly["Spread 10Y-3M"] < 0

periods_monthly = []
start = None
count = 0

for date, is_neg in inversion_monthly.items():
    if is_neg:
        if start is None:
            start = date
            count = 1
        else:
            count += 1
    else:
        if start is not None:
            periods_monthly.append((start, date, count))
            start = None
            count = 0

if start is not None:
    periods_monthly.append((start, inversion_monthly.index[-1], count))


# =========================
# Affichage
# =========================
render_taux_us(df)

st.divider()

render_spread(df)

st.divider()
render_tradingview_sp500()

