import streamlit as st
import altair as alt
import pandas as pd


def render_spread_altair(df):
    st.subheader("📉 Spread des taux US 10Y – 3M")

    # Préparer les données
    data = df[["Spread 10Y-3M"]].reset_index()
    data.columns = ["Date", "Spread"]

    # Sélection zoom / pan
    brush = alt.selection_interval(bind="scales")

    # Ligne du spread
    spread_line = alt.Chart(data).mark_line(
        color="#1f2937",  # gris foncé élégant
        strokeWidth=1.8
    ).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y(
            "Spread:Q",
            title="Spread (%)",
            scale=alt.Scale(zero=False)
        )
    ).add_selection(
        brush
    )

    # Ligne zéro (référence)
    zero_line = alt.Chart(
        pd.DataFrame({"y": [0]})
    ).mark_rule(
        color="red",
        strokeDash=[4, 4],
        strokeWidth=1
    ).encode(
        y="y:Q"
    )

    chart = (
        (spread_line + zero_line)
        .properties(height=420)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # Texte pédagogique
    st.markdown(
        """
**Comment lire ce graphique ?**

- 🟢 **Au-dessus de 0** : courbe des taux normale  
- 🔴 **Sous 0** : inversion des taux (signal macro avancé)  

Le spread est un **indicateur de régime**, pas un outil de timing.
"""
    )
