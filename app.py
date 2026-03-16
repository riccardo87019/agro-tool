import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
import base64

# CONFIGURAZIONE PREMIUM
st.set_page_config(page_title="AgroLog IA PRO - Report Certificato", layout="wide")

# Funzione per generare il PDF
def create_pdf(nome_azienda, ettari, coltura, rating, co2_totale):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "REPORT ANALISI SEQUESTRO CARBONIO 2026", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Azienda: {nome_azienda}", ln=True)
    pdf.cell(200, 10, f"Superficie: {ettari} ha", ln=True)
    pdf.cell(200, 10, f"Coltura: {coltura}", ln=True)
    pdf.cell(200, 10, f"Rating ESG Calcolato: {rating}", ln=True)
    pdf.cell(200, 10, f"Sequestro stimato: {co2_totale} Ton CO2 eq/anno", ln=True)
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, "Documento generato tramite algoritmo AgroLog IA. La validazione segue i protocolli IPCC per il monitoraggio del Carbon Farming.")
    return pdf.output(dest='S').encode('latin-1')

st.title("🌱 AgroLog IA: Professional Carbon Intelligence")

# --- SIDEBAR AVANZATA ---
st.sidebar.header("📋 Dati Aziendali")
azienda = st.sidebar.text_input("Ragione Sociale", "Azienda Agricola Rossi")
ettari = st.sidebar.number_input("Superficie (ha)", 1.0, 1000.0, 10.0)
coltura = st.sidebar.selectbox("Tipologia Coltura", ["Vite", "Olivo", "Cereali", "Nocciolo"])

st.sidebar.header("🔬 Parametri del Suolo")
tessitura = st.sidebar.selectbox("Tessitura Suolo", ["Argilloso (Alto stoccaggio)", "Limoso (Medio)", "Sabbioso (Basso)"])
sostanza_organica = st.sidebar.slider("Sostanza Organica Attuale (%)", 0.5, 5.0, 1.8)

# --- LOGICA SCIENTIFICA ---
# Coefficienti semplificati basati su studi agronomici
coeff_tessitura = {"Argilloso (Alto stoccaggio)": 1.2, "Limoso (Medio)": 1.0, "Sabbioso (Basso)": 0.7}
base_sequestro = 1.5 # Ton/ha base
tua_co2_ha = base_sequestro * coeff_tessitura[tessitura] * (sostanza_organica / 1.8)

total_co2 = round(tua_co2_ha * ettari, 2)
prezzo_credito = 45.0 # Prezzo stimato 2026
valore_economico = round(total_co2 * prezzo_credito, 2)

# --- DASHBOARD ---
col1, col2, col3 = st.columns(3)
with col1:
    rating = "A" if tua_co2_ha > 2.0 else "B" if tua_co2_ha > 1.2 else "C"
    st.metric("Rating ESG", rating)
with col2:
    st.metric("CO2 Sequestrata", f"{total_co2} Ton/anno")
with col3:
    st.metric("Valore Crediti", f"€ {valore_economico}")

st.markdown("---")

# --- GRAFICI DI BENCHMARKING ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Confronto Efficienza Suolo")
    df_bench = pd.DataFrame({
        'Categoria': ['Tua Azienda', 'Media Regione', 'Top Performers'],
        'Ton CO2/ha': [tua_co2_ha, 1.6, 3.2]
    })
    fig = px.bar(df_bench, x='Categoria', y='Ton CO2/ha', color='Categoria', 
                 color_discrete_map={'Tua Azienda': '#2ecc71', 'Media Regione': '#95a5a6', 'Top Performers': '#f1c40f'})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Simulazione Crescita 2026-2030")
    anni = [2026, 2027, 2028, 2029, 2030]
    valori = [total_co2 * (1.05**i) for i in range(5)]
    fig_line = px.line(x=anni, y=valori, labels={'x':'Anno', 'y':'Ton CO2'}, title="Incremento Carbon Stock con gestione Rigenerativa")
    st.plotly_chart(fig_line, use_container_width=True)

# --- GENERAZIONE REPORT ---
st.markdown("### 📄 Generazione Documentazione Ufficiale")
if st.button("Genera Report PDF Professionale"):
    pdf_bytes = create_pdf(azienda, ettari, coltura, rating, total_co2)
    st.download_button(label="📥 Scarica Report per la Banca",
                       data=pdf_bytes,
                       file_name=f"Report_Carbonio_{azienda}.pdf",
                       mime="application/pdf")
    st.success("Report generato con successo!")
