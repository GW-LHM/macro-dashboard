import streamlit as st
import plotly.graph_objects as go


def render_sp500(sp500, periods):
    st.subheader("📈 S&P 500 et contexte macro (spread 10Y – 3M)")

    fig = go.Figure()

    # Courbe S&P 500
    fig.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500["S&P 500"],
        mode="lines",
        name="S&P 500",
        line=dict(color="#1f77b4", width=2)
    ))

    # Barres verticales d'inversion
    for start, end, days in periods:
        if days >= 90:
            color = "rgba(214,39,40,0.25)"   # 🔴 rouge
        elif days >= 60:
            color = "rgba(255,127,14,0.25)"  # 🟠 orange
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
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)
