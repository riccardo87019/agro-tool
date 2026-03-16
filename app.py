import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# CONFIGURAZIONE ESTETICA "DARK LUXURY"
st.set_page_config(page_title="AgroLog IA | Executive", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background: #1f2937; border-radius: 10px; padding: 20px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AgroLog IA: Executive Carbon Intelligence")

# --- LOGICA AI DI INTERPRETAZIONE (L'Unicità) ---
def genera_insight(pratica, so):
    if pratica == "Agricoltura Rigenerativa" and so < 2.0:
        return "⚡ POTENZIALE MASSIMO: Il tuo suolo è pronto per una transizione esplosiva. Con questa pratica, prevediamo un recupero della fertilità del 15% annuo."
    elif so > 3.0:
        return "🌟 ECCELLENZA: Sei già un leader del carbonio. Il tuo obiettivo ora è la monetizzazione premium sui mercati internazionali."
    else:
        return "📈 OPPORTUNITÀ: Cambiando la gestione dei residui colturali, potresti sbloccare circa 400€/ha di incentivi residui."

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2510/2510158.png", width=100)
    st.header("Parametri Strategici")
    azienda = st.text_input("Nome Azienda", "Tenuta Agricola d'Elite")
    ettari = st.number_input("Ettari Totali", 1, 1000, 50)
    so = st.slider("Sostanza Organica (%)", 0.5, 5.0, 1.5)
    pratica = st.selectbox("Protocollo Gestionale", ["Tradizionale", "Minima Lavorazione", "Agricoltura Rigenerativa"])

# --- DASHBOARD DINAMICA ---
insight = genera_insight(pratica, so)
st.info(f"**🤖 AI Insight:** {insight}")

c1, c2, c3 = st.columns(3)
# Calcoli scientifici simulati
co2_totale = ettari * (2.5 if pratica == "Agricoltura Rigenerativa" else 0.8) * (so/1.5)
valore_mercato = co2_totale * 55 # 55€ a tonnellata

with c1:
    st.metric("Carbon Rating", "AAA+" if so > 2.5 else "B", delta="Top 5% Zona" if so > 2.5 else "-12% Media")
with c2:
    st.metric("Sequestro Annuo", f"{round(co2_totale, 1)} tCO2e")
with c3:
    st.metric("Asset Valutazione", f"€ {round(valore_mercato, 2)}")

st.markdown("---")

# --- VISUALIZZAZIONE AVANZATA ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Simulazione Asset Carbonio (2026-2031)")
    proiezione = pd.DataFrame({
        'Anno': [2026, 2027, 2028, 2029, 2030, 2031],
        'Valore (€)': [valore_mercato * (1.15**i) for i in range(6)]
    })
    fig = px.area(proiezione, x='Anno', y='Valore (€)', title="Crescita del Valore dell'Asset Terreno",
                  color_discrete_sequence=['#10b981'])
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Composizione Fertilità")
    labels = ['Carbonio Umificato', 'Azoto Disponibile', 'Microrganismi', 'Minerali']
    values = [so*20, 15, 25, 40]
    fig_pie = px.pie(names=labels, values=values, hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- AZIONE FINALE ---
if st.button("🏆 GENERA DOSSIER INVESTIMENTO PDF"):
    st.balloons()
    st.success("Dossier preparato. Questo documento è pronto per essere presentato alla banca per l'accesso al credito agevolato.")
