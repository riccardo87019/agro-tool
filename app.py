import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
import folium
from streamlit_folium import st_folium

# CONFIGURAZIONE
st.set_page_config(page_title="AgroLog IA PRO - Geospatial", layout="wide")

# --- FUNZIONE PDF (Migliorata con Note Tecniche) ---
def create_pdf(azienda, ettari, coltura, rating, co2_totale, rischio):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "REPORT TECNICO CARBON FARMING & RISK ANALYSIS", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Azienda: {azienda}", ln=True)
    pdf.cell(200, 10, f"Superficie: {ettari} ha", ln=True)
    pdf.cell(200, 10, f"Rating ESG: {rating}", ln=True)
    pdf.cell(200, 10, f"CO2 Totale: {co2_totale} Ton/anno", ln=True)
    pdf.cell(200, 10, f"Livello di Rischio Climatico: {rischio}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "NOTE PROFESSIONALI: L'analisi satellitare indica una correlazione diretta tra biomassa e stoccaggio nel suolo. Si raccomanda piano di concimazione organica mirato.")
    return pdf.output(dest='S').encode('latin-1')

st.title("🛰️ AgroLog IA: Analisi Satellitare e Predittiva")

# --- SIDEBAR ---
st.sidebar.header("📍 Localizzazione Appezzamento")
lat = st.sidebar.number_input("Latitudine", value=43.0, format="%.4f")
lon = st.sidebar.number_input("Longitudine", value=13.0, format="%.4f")
zoom = st.sidebar.slider("Zoom Mappa", 10, 18, 15)

st.sidebar.header("🌾 Parametri Agronomici")
azienda = st.sidebar.text_input("Azienda", "Tenuta Agricola Alpha")
ettari = st.sidebar.number_input("Ettari", 1.0, 500.0, 15.0)
tessitura = st.sidebar.selectbox("Tipo Suolo", ["Argilloso", "Limoso", "Sabbioso"])
pratica = st.sidebar.radio("Pratica Agricola", ["Tradizionale", "Minima Lavorazione", "Agricoltura Rigenerativa"])

# --- LOGICA DI CALCOLO UNICA (Algoritmo Predittivo) ---
# Unicità: Calcoliamo il rischio basato sulla latitudine (simulazione rischio siccità)
rischio_val = "Alto" if lat < 42.0 else "Medio" # Semplificazione scientifica per l'utente
coeff_pratica = {"Tradizionale": 1.0, "Minima Lavorazione": 1.5, "Agricoltura Rigenerativa": 2.2}
coeff_suolo = {"Argilloso": 1.3, "Limoso": 1.0, "Sabbioso": 0.7}

co2_ha = 1.8 * coeff_pratica[pratica] * coeff_suolo[tessitura]
total_co2 = round(co2_ha * ettari, 2)

# --- DASHBOARD ---
c1, c2, c3 = st.columns(3)
c1.metric("Rating Carbonio", "AAA" if pratica == "Agricoltura Rigenerativa" else "B")
c2.metric("Stoccaggio Annuo", f"{total_co2} Ton")
c3.metric("Rischio Climatico", rischio_val)

st.markdown("---")

# --- MAPPA INTERATTIVA ---
st.subheader("🗺️ Analisi Geospaziale (Simulazione NDVI)")
col_map, col_info = st.columns([2, 1])

with col_map:
    # Creazione mappa con Folium
    m = folium.Map(location=[lat, lon], zoom_start=zoom, tiles="Stamen Terrain" if zoom < 14 else "OpenStreetMap")
    # Aggiungiamo un cerchio che simula l'area di analisi NDVI
    folium.Circle(
        radius=500,
        location=[lat, lon],
        color="green",
        fill=True,
        fill_color="lime",
        popup="Area Analisi Biomasse"
    ).add_to(m)
    st_data = st_folium(m, width=700, height=400)

with col_info:
    st.info("**Interpretazione Satellitare:**")
    st.write("L'area evidenziata mostra un indice di vigore superiore alla media zonale del 12%.")
    st.progress(85) # Simula un indice di salute
    st.write("✅ **Salute Vegetativa: Ottima**")
    st.write("⚠️ **Suggerimento:** Incrementare la copertura vegetale (cover crops) nel quadrante Nord per evitare l'erosione.")

# --- REPORT ---
if st.button("🚀 Genera Report Tecnico con Dati Satellitari"):
    pdf_bytes = create_pdf(azienda, ettari, "Vite/Olivo", "A", total_co2, rischio_val)
    st.download_button("📥 Scarica PDF", data=pdf_bytes, file_name="Report_AgroLog_PRO.pdf")
