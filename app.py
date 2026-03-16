import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from fpdf import FPDF

# --- 1. CONFIGURAZIONE PAGINA (Obbligatoria come prima riga) ---
st.set_page_config(page_title="AgroLog AI | Carbon Intelligence Professional", layout="wide")

# STYLE PERSONALIZZATO (Dark Mode Professionale)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background: linear-gradient(145deg, #161b22, #0d1117); border-radius: 12px; padding: 25px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONE PDF AVANZATA (Con tutti i parametri scientifici) ---
def create_pdf(azienda, df_campi, co2_totale, valore_euro):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Branding
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(16, 124, 65)
    pdf.cell(200, 15, "AGROLOG IA - DOSSIER TECNICO PATRIMONIALE", ln=True, align='C')
    
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 10, f"Documento di Valutazione Asset Carbonio per: {azienda}", ln=True, align='C')
    pdf.ln(10)
    
    # Sintesi Economica
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. RIEPILOGO ASSET", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"- Potenziale Sequestro Annuo: {round(co2_totale, 2)} Ton CO2e", ln=True)
    pdf.cell(0, 10, f"- Valutazione di Mercato Stimata: EUR {round(valore_euro, 2)}", ln=True)
    pdf.ln(5)

    # Tabella Dettagliata Appezzamenti
    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(200, 220, 200)
    # Intestazioni
    headers = ["Campo", "Ha", "SO%", "Argilla%", "Limo%", "Densità", "Protocollo", "CO2(t)"]
    widths = [35, 15, 15, 20, 20, 20, 35, 30]
    for i in range(len(headers)):
        pdf.cell(widths[i], 8, headers[i], 1, 0, 'C', True)
    pdf.ln()

    pdf.set_font("Arial", "", 8)
    for _, row in df_campi.iterrows():
        # Formula Scientifica per il PDF
        massa = (30/100) * 10000 * row["Densità"]
        soc = massa * (row["SO %"] / 100) * 0.58
        c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
        f_tessitura = 1 + (row["Argilla %"]/100) + (row["Limo %"]/200)
        seq = soc * c_prot.get(row["Protocollo"], 0.01) * f_tessitura * 3.67 * row["Ettari"]
        
        pdf.cell(widths[0], 8, str(row["Appezzamento"]), 1)
        pdf.cell(widths[1], 8, str(row["Ettari"]), 1)
        pdf.cell(widths[2], 8, f"{row['SO %']}%", 1)
        pdf.cell(widths[3], 8, f"{row['Argilla %']}%", 1)
        pdf.cell(widths[4], 8, f"{row['Limo %']}%", 1)
        pdf.cell(widths[5], 8, str(row["Densità"]), 1)
        pdf.cell(widths[6], 8, str(row["Protocollo"]), 1)
        pdf.cell(widths[7], 8, str(round(seq, 2)), 1, 1)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.multi_cell(0, 5, "Nota: Calcoli basati su modelli pedologici avanzati. Analisi conforme agli standard volontari di certificazione del carbonio.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. PERSISTENZA DATI (SESSION STATE) ---
if 'db_campi' not in st.session_state:
    st.session_state.db_campi = pd.DataFrame([
        {"Appezzamento": "Settore Nord", "Ettari": 10.0, "SO %": 1.5, "Argilla %": 25, "Limo %": 30, "Densità": 1.3, "Protocollo": "Rigenerativo Full"},
        {"Appezzamento": "Valle Vecchia", "Ettari": 5.0, "SO %": 2.1, "Argilla %": 18, "Limo %": 45, "Densità": 1.4, "Protocollo": "Intermedio"}
    ])

# --- 4. SIDEBAR (I TUOI DATI E BRANDING) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429435.png", width=80) 
    st.title("AgroLog IA")
    st.markdown("**Dott. [Tuo Nome e Cognome]**")
    st.caption("Dottore Agronomo - Esperto Carbon Farming")
    st.markdown("[Contattami su LinkedIn](https://linkedin.com/in/tuoprofilo)")
    st.markdown("📧 *Email: tua@email.it*")
    st.markdown("---")
    
    st.header("💹 Parametri Globali")
    azienda_nome = st.text_input("Ragione Sociale Azienda", "Tenuta Agricola")
    prezzo_co2 = st.number_input("Prezzo Credito CO2 (€/t)", value=65.0)
    st.info("Modello v7.0 - Motore Tessiturale Attivo")

# --- 5. DASHBOARD CENTRALE (MULTI-CAMPO) ---
st.title(f"📊 Dashboard Asset Carbonio: {azienda_nome}")
st.subheader("📑 Gestione Appezzamenti (Aggiungi righe per nuovi campi)")

# Editor interattivo con persistenza
df_editabile = st.data_editor(
    st.session_state.db_campi, 
    num_rows="dynamic", # <--- QUESTO PERMETTE DI INSERIRE PIÙ APPEZZAMENTI
    use_container_width=True,
    key="main_editor"
)
st.session_state.db_campi = df_editabile

# --- 6. MOTORE DI CALCOLO SCIENTIFICO ---
total_co2_aggregata = 0
for _, row in df_editabile.iterrows():
    # Calcolo Stock Carbonio (Massa Suolo * %SOC)
    massa_suolo_ha = (30 / 100) * 10000 * row["Densità"] 
    soc_stock = massa_suolo_ha * (row["SO %"] / 100) * 0.58
    
    # Stabilizzazione Tessiturale (Argilla + Limo)
    f_tessitura = 1 + (row["Argilla %"]/100) + (row["Limo %"]/200)
    
    # Coefficiente Protocollo
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

# --- 8. VISUALIZZAZIONI PROFESSIONALI ---
st.markdown("---")
col_pie, col_heat = st.columns([1, 1.2])

with col_pie:
    st.subheader("🎯 Rendimento dei Campi")
    df_plot = df_editabile.copy()
    # Ricalcolo per il grafico
    df_plot['CO2_val'] = df_plot.apply(lambda x: ((30/100)*10000*x['Densità']*(x['SO %']/100)*0.58 * {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(x['Protocollo'], 0.01) * (1 + x['Argilla %']/100 + x['Limo %']/200) * 3.67 * x['Ettari']), axis=1)
    fig_pie = px.pie(df_plot, values='CO2_val', names='Appezzamento', hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_heat:
    st.subheader("🌋 Mappa Potenziale Pedologico")
    som_range = [0.5, 1.5, 2.5, 3.5, 4.5, 5.0]
    clay_range = [5, 15, 25, 35, 45, 60]
    z_data = [[x * (1 + y/100) for x in som_range] for y in clay_range]
    fig_h = ff.create_annotated_heatmap(z=z_data, x=som_range, y=clay_range, colorscale='Greens', showscale=True)
    # Sovrapposizione dei campi dell'utente
    fig_h.add_trace(go.Scatter(x=df_editabile['SO %'], y=df_editabile['Argilla %'], mode='markers+text', 
                               marker=dict(color='red', size=14, symbol='x'), 
                               text=df_editabile['Appezzamento'], textposition="top center", name="Campi"))
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', xaxis_title="Sostanza Organica %", yaxis_title="Argilla %")
    st.plotly_chart(fig_h, use_container_width=True)

# --- 9. EXPORT DOSSIER PDF ---
st.markdown("---")
if st.button("🧧 Genera Dossier Professionale PDF"):
    pdf_out = create_pdf(azienda_nome, df_editabile, total_co2_aggregata, valore_totale)
    st.download_button(label="📥 Scarica Report per il Cliente", data=pdf_out, file_name=f"Report_Carbonio_{azienda_nome}.pdf", mime="application/pdf")
