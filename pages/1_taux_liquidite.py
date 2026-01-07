import streamlit as st
import pandas as pd

st.header("🏦 Taux & Liquidité")

st.markdown("""
Ce bloc analyse la structure des taux d’intérêt.
Il sert de fondation à l’analyse macroéconomique.
""")

data = pd.DataFrame({
    "Année": [2019, 2020, 2021, 2022, 2023, 2024],
    "Taux 2Y (%)": [2.5, 0.5, 0.8, 3.5, 4.8, 5.0],
    "Taux 10Y (%)": [2.7, 0.7, 1.5, 3.0, 4.0, 4.2]
}).set_index("Année")

st.subheader("Évolution des taux US (exemple)")
st.line_chart(data)
