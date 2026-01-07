import streamlit as st
import streamlit.components.v1 as components


def render_fred_spread():
    st.subheader("📉 Spread des taux US 10Y – 3M (source FRED)")

    components.html(
        """
        <iframe
          src="https://fred.stlouisfed.org/graph/?id=T10Y3M"
          width="100%"
          height="520"
          style="border:0;">
        </iframe>
        """,
        height=540
    )
