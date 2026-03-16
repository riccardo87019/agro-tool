import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from fpdf import FPDF
import datetime

# --- 1. CONFIGURAZIONE PAGINA ELITE ---
st.set_page_config(
    page_title="AgroLog AI | Global Carbon Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS AVANZATO PER INTERFACCIA PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .main { background: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #4ade80; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #166534; color: white; border: none; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #15803d; border: 1px solid #4ade80; }
    h1, h2, h3 { color: #4ade80; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICA PERSISTENZA DATI (IL DATABASE) ---
if 'db_campi' not in st.session_state:
    st.session_state.db_campi = pd.DataFrame([
        {"Appezzamento": "Settore Nord", "Ettari": 10.0, "SO %": 1.5, "Argilla %": 25.0, "Limo %": 30.0, "Densità": 1.30, "Protocollo": "Rigenerativo Full"},
        {"Appezzamento": "Valle Vecchia", "Ettari": 5.0, "SO %": 2.1, "Argilla %": 18.0, "Limo %": 45.0, "Densità": 1.40, "Protocollo": "Intermedio"}
    ])

# --- 3. FUNZIONE PDF PROFESSIONALE (DOSSIER BANCARIO) ---
def generate_pdf(azienda, df, co2_tot, val_euro):
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(200, 20, "AGROLOG IA - CARBON ASSET REPORT", ln=True, align='C')
    # Info Cliente
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Azienda: {azienda}", ln=True)
    pdf.cell(0, 10, f"Data: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(10)
    # Sintesi
    pdf.set_fill_color(230, 245, 230)
    pdf.cell(0, 12, f"VALORE TOTALE ASSET: EUR {round(val_euro, 2)}", ln=True, fill=True)
    pdf.cell(0, 12, f"SEQUESTRO ANNUO: {round(co2_tot, 2)} t CO2e", ln=True)
    pdf.ln(10)
    # Tabella Campi
    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(200, 200, 200)
    headers = ["Campo", "Ha", "SO%", "Argilla%", "Limo%", "Densità", "CO2(t)"]
    widths = [45, 20, 20, 25, 25, 25, 30]
    for i in range(len(headers)):
        pdf.cell(widths[i], 10, headers[i], 1, 0, 'C', True)
    pdf.ln()
    pdf.set_font("Arial", "", 8)
    for _, r in df.iterrows():
        # Ricalcolo per PDF
        m = (30/100)*10000*r["Densità"]
        soc = m*(r["SO %"]/100)*0.58
        f_tess = 1+(r["Argilla %"]/100)+(r["Limo %"]/200)
        c_p = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(r["Protocollo"], 0.01)
        res = soc * c_p * f_tess * 3.67 * r["Ettari"]
        pdf.cell(widths[0], 10, str(r["Appezzamento"]), 1)
        pdf.cell(widths[1], 10, str(r["Ettari"]), 1)
        pdf.cell(widths[2], 10, f"{r['SO %']}%", 1)
        pdf.cell(widths[3], 10, f"{r['Argilla %']}%", 1)
        pdf.cell(widths[4], 10, f"{r['Limo %']}%", 1)
        pdf.cell(widths[5], 10, str(r["Densità"]), 1)
        pdf.cell(widths[6], 10, str(round(res, 2)), 1, 1)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SIDEBAR BRANDING & INPUT ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429435.png", width=100)
    st.title("AgroLog IA")
    st.markdown("### 👨‍🔬 Consulente Senior")
    st.markdown("**Dott. Agronomo [Tuo Nome]**")
    st.caption("Esperto Internazionale Carbon Farming")
    st.markdown("---")
    azienda_nome = st.text_input("Azienda Agricola", "Tenuta Elite")
    prezzo_co2 = st.number_input("Prezzo CO2 (€/t)", value=65.0)
    st.markdown("---")
    st.info("Algoritmo V8.0 Multi-Tessitura Attivo")

# --- 5. MAIN DASHBOARD ---
st.title(f"🌍 Global Carbon Intelligence: {azienda_nome}")
st.markdown("---")

# Sezione Input Multi-Campo
st.subheader("📑 Gestione Asset e Parametri Pedologici")
st.write("Inserisci i dati degli appezzamenti. Puoi aggiungere righe col tasto '+' in fondo alla tabella.")
df_input = st.data_editor(
    st.session_state.db_campi,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_principale"
)
st.session_state.db_campi = df_input

# --- 6. MOTORE DI CALCOLO SCIENTIFICO AVANZATO ---
total_co2 = 0
for _, row in df_input.iterrows():
    # Massa suolo (30cm) * Densità
    massa_suolo = 0.30 * 10000 * row["Densità"]
    # Carbonio Organico Totale (SOC)
    soc_stock = massa_suolo * (row["SO %"] / 100) * 0.58
    # Fattore stabilizzazione Tessitura (Argilla e Limo)
    f_tessitura = 1 + (row["Argilla %"]/100) + (row["Limo %"]/200)
    # Fattore Protocollo
    c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(row["Protocollo"], 0.01)
    # Calcolo Finale
    seq_annuo = soc_stock * c_prot * f_tessitura * 3.67 * row["Ettari"]
    total_co2 += seq_annuo

# --- 7. METRICHE CHIAVE ---
st.markdown("---")
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Sequestro Totale", f"{round(total_co2, 2)} t CO2/anno")
with m2:
    valore_asset = total_co2 * prezzo_co2
    st.metric("Valutazione Patrimonio", f"€ {round(valore_asset, 2)}")
with c_ha := m3:
    st.metric("Superficie Totale", f"{round(df_input['Ettari'].sum(), 2)} ha")

# --- 8. ANALISI VISIVA (HEATMAP & DONUT) ---
st.markdown("---")
c_left, c_right = st.columns([1, 1.2])

with c_left:
    st.subheader("📊 Performance Asset")
    df_plot = df_input.copy()
    # Calcolo rapido per grafico
    df_plot['CO2_val'] = df_plot.apply(lambda r: ((0.30*10000*r['Densità'])*(r['SO %']/100)*0.58 * (1+(r['Argilla %']/100)+(r['Limo %']/200)) * {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(r['Protocollo'],0.01) * 3.67 * r['Ettari']), axis=1)
    fig_pie = px.pie(df_plot, values='CO2_val', names='Appezzamento', hole=0.6, color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with c_right:
    st.subheader("🌋 Mappa Potenziale Carbonio")
    s_r, c_r = [1, 2, 3, 4, 5], [10, 25, 40, 60]
    z_d = [[x * (1 + y/100) for x in s_r] for y in c_r]
    fig_h = ff.create_annotated_heatmap(z=z_d, x=s_r, y=c_r, colorscale='Greens', showscale=True)
    fig_h.add_trace(go.Scatter(x=df_input['SO %'], y=df_input['Argilla %'], mode='markers+text', 
                               marker=dict(color='red', size=15, symbol='diamond'), 
                               text=df_input['Appezzamento'], textposition="top center", name="Campi"))
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', xaxis_title="Sostanza Organica %", yaxis_title="Argilla %")
    st.plotly_chart(fig_h, use_container_width=True)

# --- 9. ESPORTAZIONE E CHIUSURA ---
st.markdown("---")
if st.button("🧧 GENERA DOSSIER BANCARIO PDF"):
    pdf_bytes = generate_pdf(azienda_nome, df_input, total_co2, valore_asset)
    st.download_button(label="📥 Scarica Report Finale", data=pdf_bytes, file_name=f"AgroLog_Report_{azienda_nome}.pdf", mime="application/pdf")
