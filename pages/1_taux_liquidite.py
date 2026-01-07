import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go


st.header("🏦 Taux & Liquidité")

st.markdown("""
Analyse des taux d’intérêt américains à partir des données officielles FRED.
Ce bloc constitue la fondation du cycle macroéconomique.
""")

# -------------------------
# Configuration FRED
# -------------------------
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES = {
    "Taux US 2Y (%)": "DGS2",
    "Taux US 10Y (%)": "DGS10"
}

# -------------------------
# Chargement des données
# -------------------------
@st.cache_data
def load_fred_series(series_id):
    api_key = st.secrets["FRED_API_KEY"]  # 👈 LIGNE CLÉ ICI

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()["observations"]
    df = pd.DataFrame(data)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    return df.set_index("date")

# -------------------------
# Assemblage des séries
# -------------------------
df = pd.DataFrame()

for label, series_id in SERIES.items():
    series = load_fred_series(series_id)
    df[label] = series["value"]

df = df.dropna()

# Limiter l'historique (ex : depuis 2000)
df = df[df.index >= "2000-01-01"]


# -------------------------
# Affichage
# -------------------------
st.subheader("Évolution des taux US (2Y vs 10Y)")
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Taux US 10Y (%)"],
    mode="lines",
    name="Taux US 10Y",
    line=dict(width=2)
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Taux US 2Y (%)"],
    mode="lines",
    name="Taux US 2Y",
    line=dict(width=2)
))

fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Taux (%)",
    legend=dict(orientation="h", y=1.1),
    margin=dict(l=40, r=40, t=40, b=40)
)

fig.update_xaxes(
    rangeslider_visible=True,
    showgrid=True
)

fig.update_yaxes(showgrid=True)

st.plotly_chart(fig, use_container_width=True)

