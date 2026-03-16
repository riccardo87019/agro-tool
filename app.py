import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA (Deve essere la prima istruzione) ---
st.set_page_config(page_title="AgroLog AI | Executive", layout="wide")

# --- 2. FUNZIONE PDF ---
def create_pdf(azienda, df_campi, co2_totale, valore_euro):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"REPORT CARBONIO: {azienda}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Sequestro Totale: {round(co2_totale, 2)} t/CO2 anno", ln=True)
    pdf.cell(0, 10, f"Valore Asset: Euro {round(valore_euro, 2)}", ln=True)
    pdf.ln(10)
    # Intestazione Tabella
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 8, "Campo", 1)
    pdf.cell(30, 8, "Ettari", 1)
    pdf.cell(30, 8, "SO %", 1)
    pdf.cell(40, 8, "Protocollo", 1)
    pdf.cell(40, 8, "CO2 (t)", 1, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. PERSISTENZA DATI (La tua "Cartella") ---
if 'df_agro' not in st.session_state:
    st.session_state.df_agro = pd.DataFrame([
        {"Appezzamento": "Campo Nord", "Ettari": 10.0, "SO %": 1.5, "Argilla %": 25, "Protocollo": "Rigenerativo Full"},
        {"Appezzamento": "Vigneto", "Ettari": 5.0, "SO %": 1.2, "Argilla %": 15, "Protocollo": "Convenzionale"}
    ])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("AgroLog IA")
    azienda = st.text_input("Ragione Sociale", "Azienda Agricola")
    prezzo_co2 = st.number_input("Prezzo CO2 (€/t)", value=65.0)
    st.markdown("---")
    st.info("Algoritmo v5.2 - Persistenza Attiva")

# --- 5. CORPO CENTRALE (La Tabella) ---
st.subheader("📑 Gestione Asset Fondiari")
df_editabile = st.data_editor(
    st.session_state.df_agro, 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_v1"
)
st.session_state.df_agro = df_editabile # Salva i cambiamenti

# --- 6. CALCOLI SCIENTIFICI ---
total_co2 = 0
for _, row in df_editabile.iterrows():
    # Formula base semplificata per stabilità
    massa = 0.30 * 10000 * 1.3 
    soc = massa * (row["SO %"] / 100) * 0.58
    c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
    seq = soc * c_prot.get(row["Protocollo"], 0.01) * (1 + row["Argilla %"]/100)
    total_co2 += seq * 3.67 * row["Ettari"]

# --- 7. DASHBOARD ---
c1, c2 = st.columns(2)
c1.metric("CO2 Totale Sequestrata", f"{round(total_co2, 1)} t/anno")
c2.metric("Valore Asset", f"€ {round(total_co2 * prezzo_co2, 2)}")

# --- 8. HEATMAP ---
st.markdown("---")
st.subheader("🌋 Heatmap Potenziale")
fig_h = ff.create_annotated_heatmap(
    z=[[1, 2, 3], [4, 5, 6]], x=[1, 2, 3], y=[10, 20], colorscale='Greens'
)
st.plotly_chart(fig_h, use_container_width=True)

# --- 9. TASTO PDF ---
if st.button("🧧 Genera Dossier PDF"):
    pdf_out = create_pdf(azienda, df_editabile, total_co2, total_co2 * prezzo_co2)
    st.download_button("📥 Scarica Report", data=pdf_out, file_name="Report.pdf", mime="application/pdf")
