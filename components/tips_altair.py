import streamlit as st
import altair as alt
import pandas as pd


def render_tips_altair(df_tips):
    st.subheader("🔪 Taux réels US (TIPS) – Pression sur les bull markets")

    # Préparation des données
    data = df_tips.copy().reset_index()
    data.columns = ["Date", "Taux réel US 10Y (%)", "Taux réel US 5Y (%)"]

    data = data.melt(
        id_vars="Date",
        var_name="Maturité",
        value_name="Taux réel",
    )

    # Limiter la période pour lisibilité
    data = data[data["Date"] >= "2010-01-01"]

    # Graphique Altair
    chart = (
        alt.Chart(data)
        .mark_line(strokeWidth=0.8)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(
                "Taux réel:Q",
                title="Taux réel (%)",
                scale=alt.Scale(domain=[-2, 4])
            ),
            color=alt.Color(
                "Maturité:N",
                scale=alt.Scale(
                    domain=[
                        "Taux réel US 10Y (%)",
                        "Taux réel US 5Y (%)",
                    ],
                    range=[
                        "#dc2626",  # rouge foncé 10Y
                        "#f97316",  # orange 5Y
                    ],
                ),
                legend=alt.Legend(title="Maturité"),
            ),
        )
        .properties(height=420)
        .interactive()
    )

    # Ligne zéro (clé macro)
    zero_line = alt.Chart(
        pd.DataFrame({"y": [0]})
    ).mark_rule(
        color="black",
        strokeDash=[4, 4],
        strokeWidth=1
    ).encode(y="y:Q")

    st.altair_chart(chart + zero_line, use_container_width=True)

    # Texte macro
    st.markdown("""
### 📉 Taux réels (TIPS) — Pourquoi c’est crucial

#### 🧠 Définition simple
Les **taux réels** représentent le **vrai coût de l’argent**, une fois l’inflation retirée.  
Ils indiquent combien on gagne (ou perd) **réellement** en prêtant de l’argent à l’État américain.

👉 Quand on parle de **TIPS**, on parle directement de **taux réels**.

---

#### 💡 Pourquoi ça impacte les marchés
Les marchés actions évoluent plus facilement quand :

- 💰 l’argent est peu cher  
- 📉 les rendements *sans risque* sont faibles  

À l’inverse, lorsque les **taux réels montent** :

- 📈 les obligations deviennent plus attractives  
- ⚠️ les investisseurs prennent moins de risques  
- 📉 les **valorisations boursières sont sous pression**

---

#### ⚠️ Le signal à surveiller
Ce n’est pas seulement le **niveau** des taux réels qui compte,  
mais surtout **la vitesse de leur hausse**.

📈 **Hausse rapide des taux réels**  
→ pression sur les actions  
→ fragilisation du bull market  

---

#### 🟢🟠🔴 Lecture simple
- 🟢 **Taux réels bas ou stables** → environnement favorable aux actions  
- 🟠 **Taux réels positifs mais calmes** → marché plus fragile  
- 🔴 **Taux réels en forte hausse** → réduction du risque recommandée  

---

#### 🧩 À retenir
Les bull markets vivent avec de l’**argent bon marché**.  
Quand l’argent devient **cher en termes réels**,  
les marchés finissent **toujours par ralentir**.
""")

