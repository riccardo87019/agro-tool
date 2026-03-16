import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AgroLog AI | Carbon Intelligence 2026", layout="wide")

# STYLE PERSONALIZZATO (Dark Mode & Professional)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background: linear-gradient(145deg, #161b22, #0d1117); border-radius: 12px; padding: 25px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONE PDF COMPLETA (TUTTI I DATI) ---
def create_pdf(azienda, df_campi, co2_totale, valore_euro):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(16, 124, 65)
    pdf.cell(200, 15, "AGROLOG IA - REPORT TECNICO INTEGRATO", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"AZIENDA: {azienda.upper()}", ln=True)
    pdf.cell(0, 10, f"VALUTAZIONE PATRIMONIALE: EUR {round(valore_euro, 2)}", ln=True)
    pdf.cell(0, 10, f"CAPITALE CARBONIO: {round(co2_totale, 2)} t/CO2e anno", ln=True)
    pdf.ln(5)

    # Tabella Analitica
    pdf.set_fill_color(200, 220, 200)
    pdf.set_font("Arial", "B", 7)
    cols = ["Appezzamento", "Ettari", "SO %", "Argilla %", "Limo %", "Densità", "Protocollo", "CO2 (t)"]
    widths = [35, 15, 15, 20, 20, 20, 35, 30]
    
    for i in range(len(cols)):
        pdf.cell(widths[i], 8, cols[i], 1, 0, 'C', True)
    pdf.ln()

    pdf.set_font("Arial", "", 7)
    for _, row in df_campi.iterrows():
        # Formula Scientifica Reale (Densità + Argilla + Limo)
        massa = (30 / 100) * 10000 * row["Densità"]
        soc = massa * (row["SO %"] / 100) * 0.58
        c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
        # Il Limo contribuisce alla stabilizzazione ma meno dell'argilla
        f_tessitura = 1 + (row["Argilla %"]/100) + (row["Limo %"]/200)
        seq = soc * c_prot.get(row["Protocollo"], 0.01) * f_tessitura * 3.67 * row["Ettari"]
        
        pdf.cell(35, 8, str(row["Appezzamento"]), 1)
        pdf.cell(15, 8, str(row["Ettari"]), 1)
        pdf.cell(15, 8, f"{row['SO %']}%", 1)
        pdf.cell(20, 8, f"{row['Argilla %']}%", 1)
        pdf.cell(20, 8, f"{row['Limo %']}%", 1)
        pdf.cell(20, 8, str(row["Densità"]), 1)
        pdf.cell(35, 8, str(row["Protocollo"]), 1)
        pdf.cell(30, 8, str(round(seq, 2)), 1, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. PERSISTENZA DATI (TESSITURA COMPLETA) ---
if 'df_agro_full' not in st.session_state:
    st.session_state.df_agro_full = pd.DataFrame([
        {"Appezzamento": "Campo 1", "Ettari": 10.0, "SO %": 1.5, "Argilla %": 25, "Limo %": 30, "Densità": 1.3, "Protocollo": "Rigenerativo Full"},
        {"Appezzamento": "Campo 2", "Ettari": 5.0, "SO %": 2.0, "Argilla %": 15, "Limo %": 45, "Densità": 1.4, "Protocollo": "Intermedio"}
    ])

# --- 4. SIDEBAR (Branding & Global Params) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429435.png", width=80)
    st.title("AgroLog IA")
    azienda_nome = st.text_input("Ragione Sociale", "Tenuta Agricola Elite")
    st.markdown("---")
    st.header("💹 Mercato Crediti")
    prezzo_co2 = st.number_input("Prezzo (€/t)", value=65.0)
    st.markdown("---")
    st.markdown("**Consulente:** Dott. Agronomo")
    st.caption("Esperto Carbon Farming & Certificazioni ESG")

# --- 5. DASHBOARD CENTRALE ---
st.title(f"📊 Sistema Integrato Carbon Intelligence: {azienda_nome}")

# TABELLA MULTI-CAMPO (La Cartella)
st.subheader("📑 Gestione Asset e Tessitura")
df_editabile = st.data_editor(
    st.session_state.df_agro_full, 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_full_v1"
)
st.session_state.df_agro_full = df_editabile

# --- 6. MOTORE DI CALCOLO SCIENTIFICO ---
total_co2_aggregata = 0
for _, row in df_editabile.iterrows():
    # Calcolo Stock Carbonio Reale (SOC Stock = Massa * %SOC)
    massa_suolo_ha = (30 / 100) * 10000 * row["Densità"] 
    soc_stock = massa_suolo_ha * (row["SO %"] / 100) * 0.58
    
    # Fattore di stabilizzazione (Tessitura: Argilla e Limo)
    f_tessitura = 1 + (row["Argilla %"]/100) + (row["Limo %"]/200)
    
    # Protocollo Gestionale
    c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
    seq_annuo_ha = soc_stock * c_prot.get(row["Protocollo"], 0.01) * f_tessitura
    
    total_co2_aggregata += seq_annuo_ha * 3.67 * row["Ettari"]

# --- 7. METRICHE ESG ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CO2 Totale Sequestrata", f"{round(total_co2_aggregata, 1)} t/anno")
with c2:
    valore_totale = total_co2_aggregata * prezzo_co2
    st.metric("Valore Annuo Asset", f"€ {round(valore_totale, 2)}")
with c3:
    st.metric("Superficie Totale", f"{round(df_editabile['Ettari'].sum(), 1)} ha")

# --- 8. VISUALIZZAZIONI ---
st.markdown("---")
col_chart, col_heat = st.columns([1, 1.3])

with col_chart:
    st.subheader("🎯 Rendimento Asset")
    df_plot = df_editabile.copy()
    # Ricalcolo per grafico
    df_plot['CO2_val'] = df_plot.apply(lambda x: ((30/100)*10000*x['Densità']*(x['SO %']/100)*0.58 * {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(x['Protocollo'], 0.01) * (1 + x['Argilla %']/100 + x['Limo %']/200) * 3.67 * x['Ettari']), axis=1)
    fig_pie = px.pie(df_plot, values='CO2_val', names='Appezzamento', hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_heat:
    st.subheader("🌋 Heatmap Potenziale (Argilla vs SO%)")
    # Generazione Heatmap dinamica
    som_range = [0.5, 1.5, 2.5, 3.5, 4.5, 5.0]
    clay_range = [5, 15, 25, 35, 45, 60]
    z_data = [[x * (1 + y/100) for x in som_range] for y in clay_range]
    fig_h = ff.create_annotated_heatmap(z=z_data, x=som_range, y=clay_range, colorscale='Greens', showscale=True)
    # Sovrapposizione campi reali
    fig_h.add_trace(go.Scatter(x=df_editabile['SO %'], y=df_editabile['Argilla %'], mode='markers+text', 
                               marker=dict(color='red', size=14, symbol='x'), 
                               text=df_editabile['Appezzamento'], textposition="top center", name="Campi"))
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', xaxis_title="Sostanza Organica %", yaxis_title="Argilla %")
    st.plotly_chart(fig_h, use_container_width=True)

# --- 9. EXPORT & DOSSIER ---
st.markdown("---")
if st.button("🧧 Genera Dossier Certificabile PDF"):
    pdf_out = create_pdf(azienda_nome, df_editabile, total_co2_aggregata, valore_totale)
    st.download_button(label="📥 Scarica Report per la Banca", data=pdf_out, file_name=f"AgroLog_Report_{azienda_nome}.pdf", mime="application/pdf")
