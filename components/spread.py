import streamlit as st
import plotly.graph_objects as go

# =========================
# Calcul de la temporalité
# =========================
def compute_spread_state(df):
    spread = df["Spread 10Y-3M"]

    is_negative_now = spread.iloc[-1] < 0
    days_negative = 0

    if is_negative_now:
        for value in spread[::-1]:
            if value >= 0:
                break
            days_negative += 1

    if not is_negative_now:
        state = "normal"
    elif days_negative < 60:
        state = "alerte_en_cours"
    else:
        state = "alerte_confirmee"

    return state, days_negative


# =========================
# Rendu visuel du spread
# =========================
def render_spread(df):
    st.subheader("Spread des taux 10Y – 3M")

    state, days_negative = compute_spread_state(df)

    # Encadré macro
    if state == "normal":
        st.success("🟢 **Situation normale** — spread positif")
    elif state == "alerte_en_cours":
        st.warning(
            f"🟠 **Alerte en cours** — spread négatif depuis **{days_negative} jours**"
        )
    else:
        st.error(
            f"🔴 **Alerte confirmée** — spread négatif depuis **{days_negative} jours**"
        )

    # Texte pédagogique
    st.markdown("""
**Comment lire ce graphique ?**

- 🟢 Spread positif → cycle économique normal  
- 🔴 Spread négatif durable → alerte macroéconomique  
- 🔁 Retour positif après inversion → phase de transition

Le spread donne une information de **régime**, pas un timing précis.
""")

    # Graphique du spread
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Spread 10Y-3M"],
        mode="lines",
        name="Spread 10Y – 3M",
        line=dict(width=2, color="#000000")
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="red")

    fig.update_layout(
        height=350,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Spread (%)"
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)
