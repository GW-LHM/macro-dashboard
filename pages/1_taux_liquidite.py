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
    "Taux US 3M (%)": "DGS3MO",
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
df = df[df.index >= "2022-01-01"]

# Calcul des spreads
df["Spread 10Y-2Y"] = df["Taux US 10Y (%)"] - df["Taux US 2Y (%)"]
df["Spread 10Y-3M"] = df["Taux US 10Y (%)"] - df["Taux US 3M (%)"]

# =========================
# État macro & temporalité
# =========================
latest_spread = df["Spread 10Y-3M"].iloc[-1]

# Détection de la période négative en cours
negative_period = df["Spread 10Y-3M"] < 0

if negative_period.iloc[-1]:
    # nombre de jours consécutifs sous 0
    days_negative = (negative_period[::-1].idxmax() - df.index[-1]).days
    days_negative = abs(days_negative)
    spread_status = "alerte"
else:
    days_negative = 0
    spread_status = "normal"

# -------------------------
# Affichage
# -------------------------
st.subheader("Évolution des taux US (10Y vs 2Y vs 3M)")
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Taux US 10Y (%)"],
    mode="lines",
    name="Taux US 10Y",
    line=dict(width=0.8, color="#1f77b4")  # bleu foncé

))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Taux US 2Y (%)"],
    mode="lines",
    name="Taux US 2Y",
    line=dict(width=0.8, color="#F54927")
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Taux US 3M (%)"],
    mode="lines",
    name="Taux US 3M",
    line=dict(width=0.8, color="#2ca02c")  # vert
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

st.subheader("Spread des taux 10Y - 3M")

if spread_status == "alerte":
    st.error(f"🔴 **Alerte macro** — Spread négatif depuis **{days_negative} jours**")
else:
    st.success("🟢 **Situation normale** — Spread positif")

fig_spread = go.Figure()

fig_spread.add_trace(go.Scatter(
    x=df.index,
    y=df["Spread 10Y-3M"],
    mode="lines",
    name="Spread 10Y – 3M",
    line=dict(width=2, color="#000000")
))

fig_spread.add_hline(
    y=0,
    line_dash="dash",
    line_color="red"
)

fig_spread.update_layout(
    height=350,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Spread (%)",
    margin=dict(l=40, r=40, t=40, b=40)
)

fig_spread.update_xaxes(rangeslider_visible=True, showgrid=True)
fig_spread.update_yaxes(showgrid=True)

st.plotly_chart(fig_spread, use_container_width=True)

st.markdown("""
### 🧠 Comment lire le spread **10Y – 3M** ?

Ce graphique montre la **différence entre le taux d’intérêt à long terme (10 ans)**  
et le **taux à très court terme (3 mois)** aux États-Unis.  
Il permet d’évaluer **l’état du cycle économique**.

---

### 🟢 **Au-dessus de 0** 📈  
➡️ Situation économique **normale**

- Les taux longs sont plus élevés que les taux courts  
- Les marchés anticipent **croissance et stabilité**  
- Contexte généralement **favorable aux actifs risqués**

---

### 🔴 **En dessous de 0** 📉 *(inversion des taux)*  
⚠️ **Signal d’alerte macroéconomique**

- Les taux courts dépassent les taux longs  
- Les marchés anticipent un **ralentissement économique**  
- Historiquement, ce phénomène a souvent **précédé des récessions**

👉 Le signal devient **significatif** lorsqu’il dure **plusieurs mois consécutifs**  
Les inversions très courtes peuvent être du **bruit de marché**

---

### ⏳ À retenir
- Ce n’est **pas une prévision immédiate**  
- Le délai entre l’inversion et ses effets peut varier  
- C’est un **indicateur de cycle**, pas un outil de timing précis

---

### 🧭 Lecture rapide
- 🟢 **Spread durablement positif** → cycle normal  
- 🔴 **Spread négatif prolongé** → alerte macro confirmée  
- 🔁 **Retour au-dessus de 0 après inversion** → phase tardive du cycle
""")
