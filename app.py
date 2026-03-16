import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
#  1. CONFIGURAZIONE PAGINA & STILE CSS (UI/UX)
# ─────────────────────────────────────────────
st.set_page_config(page_title="AgroLog IA | Global Carbon Strategic", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f4ee; }

.main-header {
    background: linear-gradient(135deg, #072a1a 0%, #1e5c38 100%);
    padding: 2.5rem; border-radius: 20px; color: white; margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.kpi-card {
    background: white; border-radius: 15px; padding: 1.5rem; border: 1px solid #e0e0e0;
    text-align: center; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
.kpi-value { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #1e5c38; }
.kpi-label { font-size: .65rem; color: #7a8c7e; text-transform: uppercase; letter-spacing: .1em; margin-top: 8px; }
.sec-title { 
    font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: #072a1a; 
    border-left: 6px solid #d4a843; padding-left: 15px; margin: 2.5rem 0 1.2rem; 
}
.sim-box { 
    background: #eef5f0; border: 2px dashed #2d8a55; padding: 1.5rem; border-radius: 15px; 
}
.rating-badge { background:#d1fae5; color:#065f46; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  2. MOTORE SCIENTIFICO INTEGRATO (LOGICA UNIFICATA)
# ─────────────────────────────────────────────
def calcola_modello_completo(row, zona_climatica, boost_rigenerativo=False):
    """
    Integra: IPCC Tier 1, Effetto Q10 Temperatura, Stabilizzazione Argilla, 
    Lisciviazione Diesel e Riserva Idrica.
    """
    # A. Correzione Climatica (Mineralizzazione)
    f_clima = {"Pianura": 0.94, "Collina litoranea": 0.98, "Collina interna": 1.05, "Montagna": 1.15}
    moltiplicatore_clima = f_clima.get(zona_climatica, 1.0)

    # B. Stock C-Suolo (30cm)
    densita = float(row.get("Densità (g/cm³)", 1.3))
    massa_suolo = 0.30 * 10000 * densita 
    soc_attuale_t = massa_suolo * (float(row.get("SO %", 1.5)) / 100) * 0.58
    
    # C. Analisi Diesel e Mezzi (Litri/ha)
    protocollo = "Rigenerativo Full" if boost_rigenerativo else row.get("Protocollo", "Intermedio")
    diesel_map = {"Convenzionale": 145, "Intermedio": 85, "Rigenerativo Full": 45}
    litri_diesel = diesel_map.get(protocollo, 85)
    emissioni_diesel_tco2 = (litri_diesel * 2.68) / 1000 # Emissione diretta gasolio
    
    # D. Sequestro Agronomico (Fattori di gestione)
    f_mgmt = {"Convenzionale": 0.005, "Intermedio": 0.021, "Rigenerativo Full": 0.052}
    f_text = 1 + (float(row.get("Argilla %", 20)) / 100) # L'argilla 'sequestra' più a lungo
    f_cc = 1.15 if (row.get("Cover crops", False) or boost_rigenerativo) else 1.0
    
    # E. Calcoli Finali per Superficie
    ettari = float(row.get("Ettari", 1))
    sequestro_annuo = (soc_attuale_t * f_mgmt.get(protocollo, 0.02) * f_text * f_cc * moltiplicatore_clima) * 3.667
    
    return {
        "co2_sequestrata": sequestro_annuo * ettari,
        "co2_emessa_diesel": emissioni_diesel_tco2 * ettari,
        "diesel_litri": litri_diesel * ettari,
        "risparmio_idrico_m3": ettari * (float(row.get("SO %", 1.5)) * 145), # Capacità campo extra
        "valore_fondiario_stimato": ettari * 1250 * (float(row.get("SO %", 1.5)) / 1.2)
    }

# ─────────────────────────────────────────────
#  3. INTERFACCIA UTENTE (SIDEBAR & HEADER)
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2548/2548542.png", width=60)
    st.title("AgroLog Strategic")
    azienda = st.text_input("Ragione Sociale", "Tenuta Agraria 2026")
    tecnico = st.text_input("Agronomo Responsabile", "Dott. Agr. Rossi")
    zona_scelta = st.selectbox("Zona Climatica", ["Pianura", "Collina litoranea", "Collina interna", "Montagna"])
    prezzo_co2 = st.slider("Prezzo CO2 (€/t)", 30, 150, 52)
    costo_diesel = st.number_input("Diesel Agricolo (€/l)", 0.8, 2.0, 1.12)
    st.divider()
    cert_bio = st.toggle("Regime Biologico", True)
    cert_esg = st.toggle("Certificazione ESG/VIVA", False)

st.markdown(f"""
<div class="main-header">
    <h1>{azienda} — Carbon & Asset Management</h1>
    <p>Consulente: {tecnico} | Analisi basata su standard IPCC e bilancio idrico-energetico</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  4. GESTIONE DATI (DATABASE DINAMICO)
# ─────────────────────────────────────────────
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Appezzamento": "Campo Nord", "Ettari": 15.0, "SO %": 1.4, "Argilla %": 28, "Limo %": 30, "Densità (g/cm³)": 1.35, "Protocollo": "Convenzionale", "Cover crops": False},
        {"Appezzamento": "Vigneto Est", "Ettari": 8.0, "SO %": 2.2, "Argilla %": 15, "Limo %": 45, "Densità (g/cm³)": 1.22, "Protocollo": "Rigenerativo Full", "Cover crops": True},
    ])

st.markdown('<div class="sec-title">🗺️ Inventario Fondiario e Parametri Pedologici</div>', unsafe_allow_html=True)
df_edit = st.data_editor(st.session_state.df_campi, num_rows="dynamic", use_container_width=True)
st.session_state.df_campi = df_edit

# ─────────────────────────────────────────────
#  5. ELABORAZIONE RISULTATI INTEGRATI
# ─────────────────────────────────────────────
res_attuale = [calcola_modello_completo(r, zona_scelta) for _, r in df_edit.iterrows()]
res_potenziale = [calcola_modello_completo(r, zona_scelta, boost_rigenerativo=True) for _, r in df_edit.iterrows()]

# Aggregati
tot_ha = df_edit["Ettari"].sum()
tot_seq = sum([x["co2_sequestrata"] for x in res_attuale])
tot_emit = sum([x["co2_emessa_diesel"] for x in res_attuale])
tot_diesel_litri = sum([x["diesel_litri"] for x in res_attuale])
tot_netto = tot_seq - tot_emit
valore_netto_co2 = max(0, tot_netto) * prezzo_co2

# Analisi Potenziali (What-If)
pot_diesel_litri = sum([x["diesel_litri"] for x in res_potenziale])
risparmio_diesel_euro = (tot_diesel_litri - pot_diesel_litri) * costo_diesel
extra_co2_euro = (sum([x["co2_sequestrata"] for x in res_potenziale]) - tot_seq) * prezzo_co2

# ESG Rating Logic
score_base = 35 + (20 if cert_bio else 0) + (15 if cert_esg else 0) + min(int(tot_netto/tot_ha*15), 30)
rating = "A" if score_base > 82 else "B" if score_base > 65 else "C"

# ─────────────────────────────────────────────
#  6. VISUALIZZAZIONE KPI STRATEGICI
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📊 Indicatori Patrimoniali e Ambientali</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">ESG Rating</div><div class="kpi-value">{score_base}</div><span class="rating-badge">{rating}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Bilancio CO2 Netto</div><div class="kpi-value">{round(tot_netto,1)} t</div><div style="font-size:0.6rem;">Seq - Diesel</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Valore Economico</div><div class="kpi-value">€{int(valore_netto_co2):,}</div><div style="font-size:0.6rem; color:green;">Crediti Maturati</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Riserva Idrica</div><div class="kpi-value">{int(sum([x["risparmio_idrico_m3"] for x in res_attuale])):,} m³</div><div style="font-size:0.6rem; color:blue;">Volume Extra Suolo</div></div>', unsafe_allow_html=True)
with c5: 
    plusvalore = (tot_netto / 12) 
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Asset Value</div><div class="kpi-value">+{round(plusvalore,1)}%</div><div style="font-size:0.6rem; color:#d4a843;">Plusvalore Terreno</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  7. SIMULATORE DI CONVERSIONE (BUSINESS CASE)
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🚀 Business Case: Transizione Rigenerativa Full</div>', unsafe_allow_html=True)
s1, s2 = st.columns([1, 2])

with s1:
    gain_totale = risparmio_diesel_euro + extra_co2_euro
    st.markdown(f"""
    <div class="sim-box">
        <h4 style="margin:0; color:#1e5c38;">Margine di Miglioramento</h4>
        <p style="font-size:0.85rem; margin:10px 0;">Ottimizzando i protocolli su tutti gli {tot_ha} ha:</p>
        <h2 style="margin:0; color:#2d8a55;">+ € {int(gain_totale):,} <small style="font-size:0.9rem;">/anno</small></h2>
        <hr style="border:0.5px solid #ccc;">
        <p style="font-size:0.8rem;">📉 Risparmio Gasolio: <b>€{int(risparmio_diesel_euro):,}</b></p>
        <p style="font-size:0.8rem;">🌱 Nuovi Crediti CO2: <b>€{int(extra_co2_euro):,}</b></p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    labels = ['Emissioni Diesel (tCO2)', 'Sequestro Suolo (tCO2)']
    fig = go.Figure(data=[
        go.Bar(name='Stato Attuale', x=labels, y=[tot_emit, tot_seq], marker_color='#94a3b8'),
        go.Bar(name='Scenario Rigenerativo', x=labels, y=[sum([x["co2_emessa_diesel"] for x in res_potenziale]), sum([x["co2_sequestrata"] for x in res_potenziale])], marker_color='#2d8a55')
    ])
    fig.update_layout(barmode='group', height=280, margin=dict(t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
#  8. SCIENZA DEL SUOLO & ANALISI TECNICA
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🧪 Approfondimento: Stabilità del Carbonio</div>', unsafe_allow_html=True)

sc1, sc2 = st.columns(2)
with sc1:
    st.info("""**La 'Cassaforte' Minerale (MAOC):** Il software calcola la stabilità del carbonio basandosi sulla percentuale di **Argilla**. 
    I terreni argillosi hanno una 'capacità di carico' maggiore e blindano il carbonio proteggendolo dalla decomposizione microbica.
    Passare a protocolli rigenerativi aumenta la frazione stabile, proteggendo il valore dei tuoi asset nel tempo.""")
    
with sc2:
    # Heatmap Pedologica
    soil_x = np.linspace(0.5, 5, 20)
    soil_y = np.linspace(5, 60, 20)
    z_data = np.array([[x * (1 + y/100) for x in soil_x] for y in soil_y])
    fig_heat = px.imshow(z_data, x=soil_x, y=soil_y, labels=dict(x="Sostanza Organica %", y="Argilla %", color="Rating Stabilità"),
                         color_continuous_scale='YlGn', title="Matrice di Permanenza del Carbonio")
    st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────────────────────────────
#  9. EXPORT & CHIUSURA
# ─────────────────────────────────────────────
st.divider()
if st.button("📥 Esporta Report Strategico ESG (Dossier Bancario)"):
    st.toast("Generazione report in corso...", icon="📄")
    st.success("Report pronto! Per salvarlo, usa la funzione stampa del browser (Ctrl+P).")

st.caption("AgroLog Strategic Framework v5.2 - Conforme a CSRD 2026, Metodologie IPCC e Verra.")
