import streamlit as st
import altair as alt
import pandas as pd


def render_taux_altair(df):
    st.subheader("📈 Taux US – 10Y / 2Y / 3M")

    # Sécuriser l'index date
    data = df[
        [
            "Taux US 10Y (%)",
            "Taux US 2Y (%)",
            "Taux US 3M (%)",
        ]
    ].copy()

    data = data.reset_index()
    data.columns = ["Date", "Taux US 10Y (%)", "Taux US 2Y (%)", "Taux US 3M (%)"]

    # Passage au format long (Altair)
    data = data.melt(
        id_vars="Date",
        var_name="Maturité",
        value_name="Taux",
    )

    # Zoom / pan
    brush = alt.selection_interval(bind="scales")

    chart = (
        alt.Chart(data)
        .mark_line(strokeWidth=0.8)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(
    "Taux:Q",
    title="Taux (%)",
    scale=alt.Scale(domain=[0, 12])
),

            color=alt.Color(
                "Maturité:N",
                scale=alt.Scale(
                    domain=[
                        "Taux US 10Y (%)",
                        "Taux US 2Y (%)",
                        "Taux US 3M (%)",
                    ],
                    range=[
                        "#1f77b4",  # bleu 10Y
                        "#ff7f0e",  # orange 2Y
                        "#2ca02c",  # vert 3M
                    ],
                ),
                legend=alt.Legend(title="Maturité"),
            ),
        )
        .add_selection(brush)
        .properties(height=420)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
