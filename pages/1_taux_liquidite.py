import streamlit as st
import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime

st.header("🏦 Taux & Liquidité")

st.markdown("""
Analyse des taux d’intérêt américains via les données officielles de la Réserve fédérale (FRED).
Ce bloc constitue la fondation du cycle macroéconomique.
""")

# Paramètres
start_date = datetime(2000, 1, 1)
end_date = datetime.today()

@st.cache_data
def load_rates():
    taux_2y = pdr.DataReader("DGS2", "fred", start_date, end_date)
    taux_10y = pdr.DataReader("DGS10", "fred", start_date, end_date)

    df = pd.concat([taux_2y, taux_10y], axis=1)
    df.columns = ["Taux US 2Y (%)", "Taux US 10Y (%)"]
    df = df.dropna()
    return df

df_rates = load_rates()

st.subheader("Évolution des taux US (2Y vs 10Y)")
st.line_chart(df_rates)
