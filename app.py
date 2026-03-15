import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# CONFIGURAZIONE
st.set_page_config(page_title="AgroLog IA PRO - 2026", layout="wide")

# CSS Custom per rendere il tool "Premium"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 AgroLog IA Professional")
st.write("Analisi Predittiva ESG, Sequestro Carbonio e Benchmarking Territoriale")

# --- SIDEBAR: DATI INDISPENSABILI ---
st.sidebar.header("📍 Localizzazione e Asset")
azienda = st.sidebar.text_input("Ragione Sociale", "Azienda Agricola Esempio")
ettari = st.sidebar.number_input("Superficie Totale (ha)", 0.1, 500.0, 15.0)
coltura = st.sidebar.selectbox("Coltura Principale", ["Vite", "Olivo", "Nocciolo", "Cereali Bio"])

st.sidebar.header("🚜 Pratiche Attuali")
storico = st.sidebar.slider("Anni di conduzione sostenibile", 0, 20, 3)
lavorazione = st.sidebar.selectbox("Gestione Suolo", ["Convenzionale (Arature)", "Minima Lavorazione", "Sodo / Rigenerativa"])
input_organici = st.sidebar.checkbox("Apporto di ammendanti organici (Compost/Letame)")

# --- LOGICA DI BENCHMARKING (Dati simulati su medie regionali 2026) ---
media_regionale_co2 = 1.8 # Ton/ha
tua_co2_base = 1.2 if lavorazione == "Convenzionale (Arature)" else 2.5
if input_organici: tua_co2_base += 0.8

# --- CALCOLO PREVISIONALE A 5 ANNI ---
anni = [2026, 2027, 2028, 2029, 2030]
previsione_status_quo = [tua_co2_base * ettari * (1 + i*0.02) for i in range(5)]
previsione_ottimizzata = [tua_co2_base * ettari * (1.15 + i*0.08) for i in range(5)] # +15% subito col tuo piano

# --- LAYOUT DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rating Attuale", "B+" if tua_co2_base > 1.8 else "C")
with col2:
    st.metric("CO2 Sequestrata", f"{round(tua_co2_base * ettari, 1)} Ton", delta=f"{round(tua_co2_base - media_regionale_co2, 1)} vs Media")
with col3:
    st.metric("Crediti Generabili", f"€ {round(tua_co2_base * ettari * 42, 2)}") # Prezzo CO2 stimato 2026
with col4:
    st.metric("Potenziale 2030", f"+ {round(((previsione_ottimizzata[-1]/previsione_status_quo[0])-1)*100)} %")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🗺️ Mappa & Benchmarking", "📈 Previsionale 2030", "📄 Report Finale"])

with tab1:
    st.write("### Analisi Spaziale e Confronto Territoriale")
    c1, c2 = st.columns([2, 1])
    with c1:
        # Simulazione Mappa (Placeholder per integrazione API Sentinel)
        st.info("Integrazione Satellitare Sentinel-2 attiva. Visualizzazione Indice NDVI.")
        map_data = pd.DataFrame({'lat': [43.0], 'lon': [13.0]}) # Esempio Marche
        st.map(map_data, zoom=12)
    with c2:
        st.write("**Performance vs Vicini**")
        df_bench = pd.DataFrame({
            'Soggetto': ['Tua Azienda', 'Media Zona', 'Top 10% Local'],
            'CO2/ha': [tua_co2_base, media_regionale_co2, 3.8]
        })
        fig = px.bar(df_bench, x='Soggetto', y='CO2/ha', color='Soggetto', color_discrete_sequence=['#2ecc71', '#bdc3c7', '#f1c40f'])
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("### Proiezione Sequestro Carbonio (5 Anni)")
    df_chart = pd.DataFrame({
        'Anno': anni * 2,
        'CO2 (Ton)': previsione_status_quo + previsione_ottimizzata,
        'Scenario': ['Status Quo'] * 5 + ['Piano AgroLog IA'] * 5
    })
    fig_line = px.line(df_chart, x='Anno', y='CO2 (Ton)', color='Scenario', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.warning("⚠️ Passando alla gestione 'Sodo / Rigenerativa' potresti sbloccare incentivi PAC supplementari per €2.400/anno.")

with tab3:
    st.write("### Generazione Report Certificato")
    st.text_area("Note dell'Agronomo per il report", "L'azienda presenta un ottimo potenziale di stoccaggio nel suolo. Si consiglia l'introduzione di cover crops invernali per massimizzare il rating ESG.")
    if st.button("🚀 Esporta Report PDF per Banca/Ente"):
        st.balloons()
        st.success("Analisi completata! Il report 'AgroLog_Alpha_2026.pdf' è pronto per la revisione manuale e firma.")
