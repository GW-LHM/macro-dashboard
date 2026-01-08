import streamlit as st
import altair as alt
import pandas as pd


def render_tips_altair(df_tips):
    st.subheader("🔪 Taux réels US (TIPS) – Pression sur les bull markets")

    # Préparation des données
    data = df_tips.copy().reset_index()
    data.columns = ["Date", "Taux réel US 10Y (%)", "Taux réel US 5Y (%)"]

    data = data.melt(
        id_vars="Date",
        var_name="Maturité",
        value_name="Taux réel",
    )

    # Limiter la période pour lisibilité
    data = data[data["Date"] >= "2010-01-01"]

    # Graphique Altair
    chart = (
        alt.Chart(data)
        .mark_line(strokeWidth=0.8)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(
                "Taux réel:Q",
                title="Taux réel (%)",
                scale=alt.Scale(domain=[-2, 4])
            ),
            color=alt.Color(
                "Maturité:N",
                scale=alt.Scale(
                    domain=[
                        "Taux réel US 10Y (%)",
                        "Taux réel US 5Y (%)",
                    ],
                    range=[
                        "#dc2626",  # rouge foncé 10Y
                        "#f97316",  # orange 5Y
                    ],
                ),
                legend=alt.Legend(title="Maturité"),
            ),
        )
        .properties(height=420)
        .interactive()
    )

    # Ligne zéro (clé macro)
    zero_line = alt.Chart(
        pd.DataFrame({"y": [0]})
    ).mark_rule(
        color="black",
        strokeDash=[4, 4],
        strokeWidth=1
    ).encode(y="y:Q")

    st.altair_chart(chart + zero_line, use_container_width=True)

    # Texte macro
    st.markdown(
        """
**Comment lire les taux réels ?**

- 🔵 **Taux réels < 0** : capital bon marché, soutien aux actifs risqués  
- ⚠️ **Taux réels > 0** : pression sur les valorisations  
- 🔪 **Hausse durable des taux réels** : érosion progressive des bull markets  

Les taux réels n’agissent pas par choc brutal,
mais par **compression lente des multiples**.
"""
    )
