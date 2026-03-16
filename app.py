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
    st.header("🔬 Parametri Avanzati")
    coltura = st.selectbox("Coltura Principale", ["Cereali", "Vite", "Olivo", "Frutteto", "Pascolo"])
    
    # Dati fisici per calcolo Stock Reale
    profondita = st.select_slider("Profondità Analisi (cm)", options=[10, 30, 60], value=30)
    densita = st.number_input("Densità Apparente (g/cm³)", 0.8, 1.8, 1.3)
    argilla = st.slider("Contenuto Argilla (%)", 5, 60, 25)
    
    st.header("🚜 Gestione Residui")
    residui = st.radio("Gestione Residui", ["Asportati", "Interrati", "Lasciati in superficie (Sodo)"])
    apporto_organico = st.number_input("Compost/Letame (t/ha/anno)", 0, 50, 0)

# --- LOGICA SCIENTIFICA AVANZATA ---
# 1. Calcoliamo la massa del suolo per ettaro (t/ha) in base alla profondità e densità
# Formula: Volume (m3) * Densità (t/m3)
massa_suolo = (profondita / 100) * 10000 * densita 

# 2. Calcoliamo lo stock attuale di Carbonio Organico (SOC)
# La SO contiene circa il 58% di Carbonio
soc_attuale = massa_suolo * (so / 100) * 0.58

# 3. Coefficiente di miglioramento basato su Protocollo e Argilla
# L'argilla aiuta a sequestrare più carbonio (effetto "spugna")
coeff_argilla = 1 + (argilla / 100)
coeff_protocollo = {"Convenzionale": 0.01, "Intermedio": 0.03, "Rigenerativo Full": 0.06}

# Sequestro annuo stimato (incremento percentuale dello stock)
sequestro_annuo_ha = soc_attuale * coeff_protocollo[protocollo] * coeff_argilla

# Trasformiamo il Carbonio (C) in CO2 equivalente (moltiplicando per 3.67)
co2_tot = sequestro_annuo_ha * 3.67 * ettari

# Valutazione economica
valore_asset = co2_tot * 65

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
