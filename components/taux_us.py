import plotly.graph_objects as go
import streamlit as st

def render_taux_us(df):
    st.subheader("Évolution des taux US (10Y / 2Y / 3M)")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Taux US 10Y (%)"],
        mode="lines",
        name="Taux US 10Y",
        line=dict(width=1, color="#1f77b4")
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Taux US 2Y (%)"],
        mode="lines",
        name="Taux US 2Y",
        line=dict(width=1, color="#F54927")
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Taux US 3M (%)"],
        mode="lines",
        name="Taux US 3M",
        line=dict(width=1, color="#2ca02c")
    ))

    fig.update_layout(
        height=500,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Taux (%)"
    )

    st.plotly_chart(fig, use_container_width=True)
