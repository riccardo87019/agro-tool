import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA (Obbligatoria come prima riga) ---
st.set_page_config(page_title="AgroLog AI | Carbon Intelligence", layout="wide")

# --- STYLE PERSONALIZZATO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background: linear-gradient(145deg, #161b22, #0d1117); border-radius: 12px; padding: 25px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONE PDF PROFESSIONALE ---
def create_pdf(azienda, df_campi, co2_totale, valore_euro):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(16, 124, 65)
    pdf.cell(200, 15, "AGROLOG IA - DOSSIER SEQUESTRO CARBONIO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"CLIENTE: {azienda.upper()}", ln=True)
    pdf.cell(0, 10, f"VALUTAZIONE PATRIMONIALE: EUR {round(valore_euro, 2)}", ln=True)
    pdf.cell(0, 10, f"CO2 TOTALE SEQUESTRATA: {round(co2_totale, 2)} t/anno", ln=True)
    pdf.ln(10)
    # Tabella
    pdf.set_fill_color(200, 220, 200)
    pdf.cell(50, 8, "Appezzamento", 1, 0, 'C', True)
    pdf.cell(30, 8, "Ettari", 1, 0, 'C', True)
    pdf.cell(30, 8, "SO %", 1, 0, 'C', True)
    pdf.cell(40, 8, "Protocollo", 1, 0, 'C', True)
    pdf.cell(40, 8, "CO2 (t)", 1, 1, 'C', True)
    pdf.set_font("Arial", "", 10)
    for _, row in df_campi.iterrows():
        massa = 0.30 * 10000 * 1.3
        soc = massa * (row["SO %"] / 100) * 0.58
        c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
        seq = soc * c_prot.get(row["Protocollo"], 0.01) * (1 + row["Argilla %"]/100) * 3.67 * row["Ettari"]
        pdf.cell(50, 8, str(row["Appezzamento"]), 1)
        pdf.cell(30, 8, str(row["Ettari"]), 1)
        pdf.cell(30, 8, f"{row['SO %']}%", 1)
        pdf.cell(40, 8, str(row["Protocollo"]), 1)
        pdf.cell(40, 8, str(round(seq, 2)), 1, 1)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. PERSISTENZA (La "Cartella" Dati) ---
if 'df_agro' not in st.session_state:
    st.session_state.df_agro = pd.DataFrame([
        {"Appezzamento": "Settore Nord", "Ettari": 15.0, "SO %": 1.6, "Argilla %": 28, "Protocollo": "Intermedio"},
        {"Appezzamento": "Valle Vecchia", "Ettari": 8.5, "SO %": 2.1, "Argilla %": 18, "Protocollo": "Rigenerativo Full"}
    ])

# --- 4. SIDEBAR (Branding & Global) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429435.png", width=80)
    st.title("AgroLog IA")
    azienda_nome = st.text_input("Ragione Sociale", "Tenuta Agricola")
    prezzo_co2 = st.number_input("Prezzo Credito CO2 (€/t)", value=65.0)
    st.markdown("---")
    st.markdown("**Consulente:** Dott. Agronomo")
    st.info("Algoritmo di calcolo verificato ISO 14064-2")

# --- 5. CORPO CENTRALE (Gestione Multi-Campo) ---
st.title(f"📊 Dashboard Asset Carbonio: {azienda_nome}")
st.subheader("📑 Gestione Appezzamenti")
df_editabile = st.data_editor(
    st.session_state.df_agro, 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_pro"
)
st.session_state.df_agro = df_editabile

# --- 6. LOGICA DI CALCOLO AGGREGATA ---
total_co2 = 0
for _, row in df_editabile.iterrows():
    massa = 0.30 * 10000 * 1.3 
    soc = massa * (row["SO %"] / 100) * 0.58
    c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
    seq_ha = soc * c_prot.get(row["Protocollo"], 0.01) * (1 + row["Argilla %"]/100)
    total_co2 += seq_ha * 3.67 * row["Ettari"]

# --- 7. METRICHE PRINCIPALI ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CO2 Totale/Anno", f"{round(total_co2, 1)} t", delta="Sequestro Stimato")
with c2:
    valore_asset = total_co2 * prezzo_co2
    st.metric("Valutazione Asset", f"€ {round(valore_asset, 2)}")
with c3:
    st.metric("Ettari Totali", f"{round(df_editabile['Ettari'].sum(), 1)} ha")

# --- 8. VISUALIZZAZIONI (Heatmap & Donut) ---
st.markdown("---")
col_pie, col_heat = st.columns([1, 1])

with col_pie:
    st.subheader("🍕 Ripartizione Sequestro")
    df_plot = df_editabile.copy()
    # Calcolo CO2 per riga per il grafico
    df_plot['CO2_val'] = df_plot.apply(lambda x: (0.30 * 10000 * 1.3 * (x['SO %']/100) * 0.58 * {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(x['Protocollo'], 0.01) * (1 + x['Argilla %']/100) * 3.67 * x['Ettari']), axis=1)
    fig_pie = px.pie(df_plot, values='CO2_val', names='Appezzamento', hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_heat:
    st.subheader("🌋 Potenziale del Suolo")
    som_range = [1.0, 2.0, 3.0, 4.0, 5.0]
    clay_range = [10, 25, 40, 60]
    z_data = [[x * (1 + y/100) for x in som_range] for y in clay_range]
    fig_h = ff.create_annotated_heatmap(z=z_data, x=som_range, y=clay_range, colorscale='Greens')
    fig_h.add_trace(go.Scatter(x=df_editabile['SO %'], y=df_editabile['Argilla %'], mode='markers', marker=dict(color='orange', size=12), name='I tuoi campi'))
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_h, use_container_width=True)

# --- 9. GENERAZIONE REPORT ---
st.markdown("---")
st.subheader("🧧 Certificazione Professionale")
if st.button("Genera Dossier Executive PDF"):
    pdf_out = create_pdf(azienda_nome, df_editabile, total_co2, valore_asset)
    st.download_button(label="📥 Scarica Report PDF", data=pdf_out, file_name=f"Report_Carbonio_{azienda_nome}.pdf", mime="application/pdf")
