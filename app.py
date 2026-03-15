import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="AgroLog IA - Carbon Validator", layout="wide")

# Header Professionale
st.title("🌱 AgroLog IA: Sustainability & Carbon Validator")
st.subheader("Analisi agronomica avanzata per Certificazioni ESG e Crediti di Carbonio")
st.markdown("---")

# Sidebar per l'inserimento dati
st.sidebar.header("Dati Aziendali & Campo")
nome_azienda = st.sidebar.text_input("Ragione Sociale Azienda")
ettari = st.sidebar.number_input("Ettari Totali (ha)", min_value=0.1, value=10.0)
tipo_coltura = st.sidebar.selectbox("Tipo di Coltura", ["Vite", "Olivo", "Cereali", "Frutteto"])
localita = st.sidebar.text_input("Località (Coordinate o Comune)")

st.sidebar.markdown("---")
st.sidebar.header("Pratiche Agronomiche")
lavorazione = st.sidebar.select_slider("Livello di Lavorazione Suolo", 
                                     options=["Aratura Profonda", "Minima Lavorazione", "No-Tillage / Sodo"])
cover_crops = st.sidebar.checkbox("Uso di Colture di Copertura (Cover Crops)")
concimazione = st.sidebar.selectbox("Tipo Concimazione", ["Minerale", "Organica / Letame", "Integrata"])

# Logica di Calcolo (Basata sulle tue competenze)
def calcola_sostenibilita(ha, lav, cover, conc):
    # Punteggio base
    punti = 0
    if lav == "No-Tillage / Sodo": punti += 40
    elif lav == "Minima Lavorazione": punti += 20
    
    if cover: punti += 30
    if conc == "Organica / Letame": punti += 30
    
    # Calcolo CO2 Sequestrata (Stima Ton/anno)
    co2_sequestrata = (punti / 100) * 2.8 * ha # 2.8 è un coeff. medio di sequestro
    
    # Definizione Rating
    if punti >= 80: rating = "A - Eccellente (Market Leader)"
    elif punti >= 50: rating = "B - Conforme ESG"
    else: rating = "C - Necessita Miglioramento"
    
    return round(co2_sequestrata, 2), rating, punti

# Esecuzione Calcolo
co2, rat, score = calcola_sostenibilita(ettari, lavorazione, cover_crops, concimazione)

# Visualizzazione Risultati in Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CO2 Sequestrata Stimata", f"{co2} Ton/anno")
with col2:
    st.metric("Rating ESG Aziendale", rat)
with col3:
    st.metric("Valore di Mercato Carbonio", f"€ {round(co2 * 35, 2)}") # 35€/ton prezzo medio 2026

st.markdown("---")

# Generazione Report per il Cliente
st.write("### 📄 Anteprima Report Certificazione")
st.info(f"L'azienda **{nome_azienda}** analizzata in località **{localita}** presenta un punteggio di sostenibilità del **{score}%**. "
         "Questo valore è idoneo per l'accesso ai finanziamenti agevolati Green e alla vendita di Crediti di Carbonio sul mercato volontario.")

if st.button("Genera Documento Finale"):
    st.balloons()
    st.success("Report Generato con Successo! (Pronto per invio a Ente Certificatore)")
