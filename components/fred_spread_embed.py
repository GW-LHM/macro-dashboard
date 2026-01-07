import streamlit as st
import streamlit.components.v1 as components


def render_fred_spread():
    st.subheader("📉 Spread des taux US 10Y – 3M (source FRED)")

    fred_iframe = """
    <iframe
        src="https://fred.stlouisfed.org/graph/graph-landing.php?g=1q8f"
        width="100%"
        height="500"
        style="border:0;">
    </iframe>
    """

    components.html(fred_iframe, height=520)
