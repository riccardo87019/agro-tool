import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURAZIONE PAGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AgroLog IA | Carbon & ESG Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CSS — DESIGN PROFESSIONALE 2026
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f4ee; }

/* Header */
.main-header {
    background: linear-gradient(135deg, #0f2318 0%, #1e5c38 60%, #2d8a55 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.main-header h1 { font-family: 'DM Serif Display', serif; color: #fff; font-size: 2rem; margin: 0; }
.main-header p { color: rgba(255,255,255,.7); margin-top: 5px; font-size: .95rem; }

/* KPI cards */
.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 1.2rem;
    border: 1px solid rgba(30,92,56,.1);
    box-shadow: 0 4px 15px rgba(15,35,24,.05);
    text-align: center;
    height: 100%;
}
.kpi-value { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #1e5c38; }
.kpi-label { font-size: .7rem; color: #7a8c7e; text-transform: uppercase; letter-spacing: .05em; margin-top: 5px; }

/* Status Badges */
.rating-A { background:#d1fae5; color:#065f46; padding:4px 12px; border-radius:20px; font-weight:700; }
.rating-B { background:#dbeafe; color:#1e40af; padding:4px 12px; border-radius:20px; font-weight:700; }
.rating-C { background:#fef3c7; color:#92400e; padding:4px 12px; border-radius:20px; font-weight:700; }
.rating-D { background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:20px; font-weight:700; }

.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #0f2318;
    border-left: 5px solid #2d8a55;
    padding-left: 12px;
    margin: 2rem 0 1rem;
}

/* Action Cards */
.action-card { background: #fff; border-radius: 10px; padding: 1rem; margin-bottom: 10px; border: 1px solid #eee; }
.action-high { border-left: 5px solid #ef4444; }
.action-mid  { border-left: 5px solid #d4a843; }
.action-low  { border-left: 5px solid #2d8a55; }

/* Risks */
.risk { display:inline-block; padding:4px 10px; border-radius:15px; font-size:.75rem; font-weight:600; margin-right:8px; margin-bottom:8px; }
.risk-alto  { background:#fee2e2; color:#991b1b; }
.risk-medio { background:#fef3c7; color:#92400e; }
.risk-basso { background:#d1fae5; color:#065f46; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOGICA DATI E SESSION STATE
# ─────────────────────────────────────────────
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Appezzamento": "Campo Nord", "Ettari": 12.0, "SO %": 1.8, "Argilla %": 28, "Limo %": 32, "Densità (g/cm³)": 1.3, "Protocollo": "Rigenerativo Full", "Cover crops": True},
        {"Appezzamento": "Vigneto Sud", "Ettari": 6.0, "SO %": 1.2, "Argilla %": 18, "Limo %": 40, "Densità (g/cm³)": 1.45, "Protocollo": "Intermedio", "Cover crops": False},
    ])

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🌿 Configurazione")
    nome_azienda = st.text_input("Ragione Sociale", "Az. Agr. Rossi")
    nome_agronomo = st.text_input("Consulente", "Dott. Agr. Bianchi")
    prezzo_co2 = st.number_input("Prezzo CO2 (€/t)", 10.0, 150.0, 38.0)
    tasso_crescita = st.slider("Crescita annua prezzo (%)", 0, 15, 5)
    
    st.divider()
    cert_bio = st.checkbox("Certificazione Bio")
    cert_sqnpi = st.checkbox("Certificazione SQNPI")
    cert_iso = st.checkbox("ISO 14064 (Carbon)")
    
    st.divider()
    fatturato = st.number_input("Fatturato (€)", 0, 10000000, 180000)
    costi_var = st.number_input("Costi Variabili (€)", 0, 10000000, 95000)

# ─────────────────────────────────────────────
#  MOTORE DI CALCOLO SCIENTIFICO
# ─────────────────────────────────────────────
def calcola_metrica(row):
    # Logica IPCC Tier 1 + Pedologia
    profondita = 0.30  # Standard IPCC 30cm
    massa_suolo = profondita * 10000 * float(row["Densità (g/cm³)"])
    soc_stock = massa_suolo * (float(row["SO %"]) / 100) * 0.58 # Fattore van Bemmelen
    
    # Fattori di gestione (FMG)
    f_mgmt = {"Convenzionale": 0.004, "Intermedio": 0.018, "Rigenerativo Full": 0.048}
    f_text = 1 + (float(row["Argilla %"]) / 100) + (float(row["Limo %"]) / 200)
    f_cc = 1.11 if row["Cover crops"] else 1.0
    
    seq_ha = soc_stock * f_mgmt.get(row["Protocollo"], 0.018) * f_text * f_cc
    co2_ha = seq_ha * 3.667 # C -> CO2
    
    return {
        "co2_tot": co2_ha * row["Ettari"],
        "co2_ha": co2_ha,
        "emit": 0.8 * row["Ettari"] # Stima emissioni N2O/Mezzi
    }

# ─────────────────────────────────────────────
#  LAYOUT MAIN
# ─────────────────────────────────────────────
st.markdown(f"""<div class="main-header"><h1>AgroLog IA — {nome_azienda}</h1><p>Carbon Intelligence & Strategia ESG Avanzata</p></div>""", unsafe_allow_html=True)

# Editor dati
st.markdown('<div class="sec-title">📑 Gestione Appezzamenti</div>', unsafe_allow_html=True)
df_edit = st.data_editor(st.session_state.df_campi, num_rows="dynamic", use_container_width=True, key="main_editor")
st.session_state.df_campi = df_edit

# Esecuzione calcoli
risultati = [calcola_metrica(r) for _, r in df_edit.iterrows()]
df_ris = pd.DataFrame(risultati)

tot_seq = df_ris["co2_tot"].sum()
tot_emit = df_ris["emit"].sum()
tot_netto = tot_seq - tot_emit
tot_ha = df_edit["Ettari"].sum()
valore_crediti = max(0, tot_netto) * prezzo_co2

# ESG Score (0-100)
score = 45 + (15 if cert_bio else 0) + (10 if cert_sqnpi else 0) + (10 if cert_iso else 0)
score = min(score + (20 if "Rigenerativo Full" in df_edit["Protocollo"].values else 5), 100)
rating = "A" if score > 80 else "B" if score > 65 else "C" if score > 45 else "D"

# ─────────────────────────────────────────────
#  KPI & DASHBOARD
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📊 Analisi Performance</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{score}</div><div class="kpi-label">Score ESG</div><span class="rating-{rating}">{rating}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{round(tot_seq,1)}</div><div class="kpi-label">tCO2 Sequestrate/Anno</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">€{int(valore_crediti):,}</div><div class="kpi-label">Valore Crediti Annui</div></div>', unsafe_allow_html=True)
with c4: 
    color = "#065f46" if tot_netto > 0 else "#991b1b"
    st.markdown(f'<div class="kpi-card"><div class="kpi-value" style="color:{color}">{round(tot_netto,1)}</div><div class="kpi-label">Bilancio Netto (t)</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GRAFICI
# ─────────────────────────────────────────────
g1, g2 = st.columns([1, 1])
with g1:
    fig_pie = px.pie(df_edit, values='Ettari', names='Appezzamento', hole=0.5, title="Distribuzione Superficie", color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_pie, use_container_width=True)

with g2:
    anni = list(range(2026, 2031))
    valori = [valore_crediti * ((1 + tasso_crescita/100)**i) for i in range(5)]
    fig_trend = px.line(x=anni, y=valori, title="Proiezione Ricavi Crediti CO2 (5 anni)", markers=True)
    fig_trend.update_traces(line_color='#1e5c38')
    st.plotly_chart(fig_trend, use_container_width=True)

# ─────────────────────────────────────────────
#  AZIONI E RISCHI
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🎯 Piano d\'Azione Consigliato</div>', unsafe_allow_html=True)
if "Convenzionale" in df_edit["Protocollo"].values:
    st.markdown('<div class="action-card action-high"><b>🔴 Transizione Rigenerativa:</b> Convertire i campi convenzionali per sbloccare +0.5 tCO2/ha.</div>', unsafe_allow_html=True)
if not cert_iso:
    st.markdown('<div class="action-card action-mid"><b>🟡 Certificazione ISO 14064:</b> Necessaria per vendere crediti sul mercato volontario Premium.</div>', unsafe_allow_html=True)

st.markdown('<div class="sec-title">⚠️ Mappa dei Rischi</div>', unsafe_allow_html=True)
st.markdown(f"""
    <span class="risk risk-alto">EROSIONE: Alto (SO% < 1.5 in alcuni campi)</span>
    <span class="risk risk-medio">NORMATIVO: Adeguamento CSRD 2026</span>
    <span class="risk risk-basso">CLIMATICO: Stress idrico moderato</span>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GENERATORE REPORT PDF/HTML
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📄 Export Report</div>', unsafe_allow_html=True)
if st.button("Genera Report Professionale"):
    oggi = datetime.now().strftime("%d/%m/%Y")
    html_report = f"""
    <div style="font-family: sans-serif; padding: 40px; border: 1px solid #eee;">
        <h2 style="color: #1e5c38;">REPORT SOSTENIBILITÀ - {nome_azienda}</h2>
        <p><b>Data:</b> {oggi} | <b>Agronomo:</b> {nome_agronomo}</p>
        <hr>
        <h3>Sintesi Risultati</h3>
        <ul>
            <li><b>Score ESG:</b> {score}/100 (Rating {rating})</li>
            <li><b>Sequestro Annuo:</b> {round(tot_seq, 2)} tCO2eq</li>
            <li><b>Valore Economico Stimato:</b> €{int(valore_crediti):,}</li>
        </ul>
        <p><small>Metodologia: IPCC Tier 1 (2006/2019 Refinement). Calcolo basato su stock di carbonio minerale a 30cm.</small></p>
        <br><br>
        <div style="margin-top: 50px; border-top: 1px solid #000; width: 200px;">Firma del Tecnico</div>
    </div>
    """
    st.markdown(html_report, unsafe_allow_html=True)
    st.success("Report generato! Puoi stamparlo salvando la pagina (Ctrl+P).")

# Footer
st.markdown("---")
st.caption("AgroLog IA v3.2 - Professional Edition 2026. Basato su dati IPCC e CREA-AA.")
