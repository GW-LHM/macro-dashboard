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

    # Bandes d'inversion mensuelles
    for start, end, months in periods:
        if months >= 9:
            fill = "rgba(214,39,40,0.15)"   # rouge
        elif months >= 6:
            fill = "rgba(255,127,14,0.12)"  # orange
        else:
            continue

        fig.add_vrect(
            x0=start,
            x1=end,
            fillcolor=fill,
            line_width=0
        )

    # Layout explicite (clé pour éviter les bugs Plotly/Streamlit)
    fig.update_layout(
        height=450,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="S&P 500",
        xaxis=dict(
            range=[sp500.index.min(), sp500.index.max()],
            fixedrange=False
        )
    )

    fig.update_xaxes(
        showgrid=True,
        rangeslider_visible=True
    )

    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)
