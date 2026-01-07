import streamlit as st
import altair as alt
import pandas as pd


def render_spread_altair(df):
    st.subheader("📉 Spread des taux US 10Y – 3M")

    # Préparer les données
    data = df[["Spread 10Y-3M"]].reset_index()
    data.columns = ["Date", "Spread"]

    # Sélection zoom / pan
    brush = alt.selection_interval(bind="scales")

    # Ligne du spread
    spread_line = alt.Chart(data).mark_line(
        color="#1f2937",  # gris foncé élégant
        strokeWidth=1.8
    ).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y(
            "Spread:Q",
            title="Spread (%)",
            scale=alt.Scale(zero=False)
        )
    ).add_selection(
        brush
    )

    # Ligne zéro (référence)
    zero_line = alt.Chart(
        pd.DataFrame({"y": [0]})
    ).mark_rule(
        color="red",
        strokeDash=[4, 4],
        strokeWidth=1
    ).encode(
        y="y:Q"
    )

    chart = (
        (spread_line + zero_line)
        .properties(height=420)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # Texte pédagogique
    st.markdown("""
### 🧭 Comment interpréter le spread 10Y – 3M ?

Ce graphique n’a pas pour objectif de prévoir un point haut ou bas du marché,  
mais d’**identifier les phases de fragilité du cycle économique** et les périodes
où le **risque systémique augmente**.

---

#### 🟠 1️⃣ Entrée en inversion (passage sous 0)
➡️ La politique monétaire devient restrictive  
➡️ Le crédit commence à se tendre  
➡️ **Alerte macro** : le régime change, sans signal de timing immédiat  

> ⚠️ Le marché peut encore progresser dans cette phase.

---

#### 🔴 2️⃣ Inversion prolongée (plusieurs mois sous 0)
➡️ Le stress s’accumule dans l’économie réelle  
➡️ Banques, entreprises et ménages sont sous pression  
➡️ **Le risque systémique augmente progressivement**

> ⏱️ **La durée de l’inversion est plus importante que son amplitude.**

---

#### ⚠️ 3️⃣ Sortie d’inversion après une longue période négative
➡️ Les effets retardés du resserrement monétaire apparaissent  
➡️ Des accidents économiques ou financiers se matérialisent  
➡️ **Les corrections des marchés actions surviennent souvent dans cette phase**

> 💥 Le danger n’est pas l’inversion elle-même,  
> mais **la combinaison d’une inversion longue suivie d’un retournement**.

---

### 🎯 À retenir
- Le spread est un **indicateur de régime**, pas un outil de timing court terme  
- Les phases les plus risquées apparaissent **après une inversion prolongée**  
- Ce graphique sert à **adapter son niveau de risque**, pas à trader
""")
