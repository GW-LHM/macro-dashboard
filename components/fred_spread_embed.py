import streamlit.components.v1 as components

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
