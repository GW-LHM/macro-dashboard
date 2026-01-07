import streamlit as st
import streamlit.components.v1 as components


def render_fred_spread():
    st.subheader("📉 Spread des taux US 10Y – 3M (source FRED)")

    iframe = """
    <iframe
        src="https://fred.stlouisfed.org/graph/graph-landing.php?g=1YfH"
        width="100%"
        height="500"
        style="border:0;">
    </iframe>
    """

    components.html(iframe, height=520)
