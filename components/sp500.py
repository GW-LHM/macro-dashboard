import streamlit as st
import plotly.graph_objects as go


def render_sp500(sp500, periods):
    st.subheader("📈 S&P 500 et inversions du spread 10Y – 3M (mensuel)")

    fig = go.Figure()

    # Courbe S&P 500
    fig.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500["S&P 500"],
        mode="lines",
        name="S&P 500",
        line=dict(color="#1f77b4", width=2)
    ))

    # Bandes mensuelles d'inversion
    for start, end, months in periods:
        if months >= 9:
            color = "rgba(214,39,40,0.15)"   # 🔴 ≥ 9 mois
        elif months >= 6:
            color = "rgba(255,127,14,0.12)"  # 🟠 ≥ 6 mois
        else:
            continue

        fig.add_vrect(
            x0=start,
            x1=end,
            fillcolor=color,
            line_width=0
        )

    fig.update_layout(
        height=450,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="S&P 500",
        xaxis_range=[
            sp500.index.min(),
            sp500.index.max()
        ]
    )

    fig.update_xaxes(
        showgrid=True,
        rangeslider_visible=True,
        autorange=True,
        fixedrange=False
    )

    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)
