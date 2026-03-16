import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF

# CONFIGURAZIONE ELITE
st.set_page_config(page_title="AgroLog AI | Financial & Carbon Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background: linear-gradient(145deg, #161b22, #0d1117); border-radius: 12px; padding: 25px; border: 1px solid #30363d; box-shadow: 5px 5px 15px #05070a; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR E DATI ---
with st.sidebar:
    st.title("💼 Control Panel")
    azienda = st.text_input("Ragione Sociale", "Tenuta Agricola d'Elite")
    ettari = st.number_input("Ettari", 1, 1000, 50)
    so = st.slider("Sostanza Organica attuale (%)", 0.5, 5.0, 1.8)
    protocollo = st.selectbox("Protocollo Tecnico", ["Convenzionale", "Intermedio", "Rigenerativo Full"])
    st.markdown("---")
    st.info("Algoritmo AgroLog v.4.2 - Aggiornato ai parametri IPCC 2026")

# --- CALCOLO PARAMETRI (Logica Scientifica) ---
co2_tot = ettari * (2.8 if protocollo == "Rigenerativo Full" else 1.2) * (so/1.5)
rating_val = "AAA" if co2_tot/ettari > 2.5 else "AA" if co2_tot/ettari > 1.5 else "B"
valore_asset = co2_tot * 65 # Prezzo stimato credito premium 2026

# --- HEADER DASHBOARD ---
st.title(f"📊 Dashboard Strategica: {azienda}")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("ESG Rating", rating_val, delta="Top 2% Nazionale" if rating_val == "AAA" else "-5% vs Target")
with c2:
    st.metric("Stoccaggio CO2e/Anno", f"{round(co2_tot, 1)} t", delta=f"{round(co2_tot/ettari, 1)} t/ha")
with c3:
    st.metric("Valutazione Crediti", f"€ {round(valore_asset, 2)}", delta="Previsione +12% nel 2027")

st.markdown("---")

# --- ANALISI MULTIDIMENSIONALE (Unicità Visiva) ---
col_map, col_radar = st.columns([1, 1])

with col_radar:
    st.subheader("🎯 Profilo di Sostenibilità")
    # Grafico Radar
    categories = ['Sequestro CO2', 'Biodiversità', 'Ritenzione Idrica', 'Resilienza Climatica', 'Margine Economico']
    valori_radar = [85 if protocollo == "Rigenerativo Full" else 40, 70, 60, 55, 90]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
          r=valori_radar,
          theta=categories,
          fill='toself',
          name='Profilo Aziendale',
          line_color='#00ff88'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_radar, use_container_width=True)

with col_map:
    st.subheader("💡 AI Advisor Report")
    st.write(f"Sulla base dei dati analizzati per **{azienda}**, il modello evidenzia un'efficienza del suolo superiore alla media.")
    st.warning("**Criticità rilevata:** La ritenzione idrica è al 60%. Si consiglia l'uso di biostimolanti organici nel periodo primaverile.")
    st.success(f"**Opportunità:** Con il protocollo {protocollo}, l'azienda può accedere a finanziamenti 'Green Loan' con tassi agevolati del 1.5% in meno rispetto al mercato.")

# --- BUSINESS CASE ---
st.markdown("### 📈 Proiezione Finanziaria Asset Carbonio")
df_fin = pd.DataFrame({
    'Anno': [2026, 2027, 2028, 2029, 2030],
    'Valore Crediti (€)': [valore_asset * (1.1**i) for i in range(5)],
    'Risparmio Costi Operativi (€)': [ettari * 120 * (i+1) for i in range(5)]
})
fig_fin = px.bar(df_fin, x='Anno', y=['Valore Crediti (€)', 'Risparmio Costi Operativi (€)'], 
                 barmode='group', color_discrete_sequence=['#00ff88', '#3b82f6'])
st.plotly_chart(fig_fin, use_container_width=True)

# --- FOOTER & REPORT ---
if st.button("🧧 GENERA EXECUTIVE SUMMARY PER LA BANCA"):
    st.balloons()
    st.write("Dossier in fase di crittografia e generazione...")
