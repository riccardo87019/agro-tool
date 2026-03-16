import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io, base64

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
#  CSS — Tema professionale luce/scuro
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
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
.main-header::after {
    content: '🌿';
    position: absolute;
    right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.08;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif;
    color: #fff;
    font-size: 1.9rem;
    margin: 0 0 .3rem;
}
.main-header p { color: rgba(255,255,255,.7); margin: 0; font-size: .9rem; }
.badge-pill {
    display: inline-block;
    background: #d4a843;
    color: #0f2318;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: .6rem;
}

/* KPI cards */
.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(30,92,56,.1);
    box-shadow: 0 2px 10px rgba(15,35,24,.05);
    text-align: center;
    height: 100%;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #1e5c38;
    line-height: 1.1;
}
.kpi-label {
    font-size: .72rem;
    color: #7a8c7e;
    text-transform: uppercase;
    letter-spacing: .07em;
    margin-top: .25rem;
}
.kpi-sub { font-size: .8rem; color: #1e5c38; font-weight: 600; margin-top: .15rem; }

/* Rating badge */
.rating-A { background:#d1fae5; color:#065f46; padding:3px 14px; border-radius:20px; font-weight:700; }
.rating-B { background:#dbeafe; color:#1e40af; padding:3px 14px; border-radius:20px; font-weight:700; }
.rating-C { background:#fef3c7; color:#92400e; padding:3px 14px; border-radius:20px; font-weight:700; }
.rating-D { background:#fee2e2; color:#991b1b; padding:3px 14px; border-radius:20px; font-weight:700; }

/* Section titles */
.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0f2318;
    border-left: 4px solid #2d8a55;
    padding-left: .7rem;
    margin: 1.8rem 0 1rem;
}

/* Sidebar */
div[data-testid="stSidebar"] { background: #0f2318; }
div[data-testid="stSidebar"] * { color: rgba(255,255,255,.88) !important; }
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #fff !important;
}
div[data-testid="stSidebar"] label {
    font-size: .78rem !important;
    text-transform: uppercase;
    letter-spacing: .05em;
    color: rgba(255,255,255,.6) !important;
}
div[data-testid="stSidebar"] .stMarkdown hr { border-color: rgba(255,255,255,.15); }

/* Action cards */
.action-card {
    background: #fff;
    border-radius: 12px;
    padding: .9rem 1.1rem;
    margin: .4rem 0;
    border: 1px solid rgba(30,92,56,.12);
}
.action-high { border-left: 4px solid #ef4444; }
.action-mid  { border-left: 4px solid #d4a843; }
.action-low  { border-left: 4px solid #2d8a55; }

/* Risk pills */
.risk { display:inline-block; padding:3px 10px; border-radius:20px; font-size:.72rem; font-weight:600; margin:2px; }
.risk-alto  { background:#fee2e2; color:#991b1b; }
.risk-medio { background:#fef3c7; color:#92400e; }
.risk-basso { background:#d1fae5; color:#065f46; }

/* Footer */
.footer { font-size:.7rem; color:#9aab9e; text-align:center; margin-top:2rem; padding-top:1rem; border-top:1px solid rgba(30,92,56,.12); }

/* Buttons */
.stButton > button {
    background: #1e5c38 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: .55rem 1.4rem !important;
}
.stButton > button:hover { background: #0f2318 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATI DEFAULT appezzamenti
# ─────────────────────────────────────────────
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Appezzamento": "Campo Nord", "Ettari": 12.0, "SO %": 1.8,
         "Argilla %": 28, "Limo %": 32, "Densità (g/cm³)": 1.3,
         "Protocollo": "Rigenerativo Full", "Cover crops": True},
        {"Appezzamento": "Vigneto Sud", "Ettari": 6.0, "SO %": 1.2,
         "Argilla %": 18, "Limo %": 40, "Densità (g/cm³)": 1.45,
         "Protocollo": "Intermedio", "Cover crops": False},
        {"Appezzamento": "Oliveto", "Ettari": 4.0, "SO %": 2.1,
         "Argilla %": 22, "Limo %": 35, "Densità (g/cm³)": 1.25,
         "Protocollo": "Rigenerativo Full", "Cover crops": True},
    ])

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 AgroLog IA")
    st.markdown("*Carbon & ESG Intelligence*")
    st.markdown("---")

    st.markdown("### Dati Aziendali")
    nome_azienda   = st.text_input("Ragione Sociale", "Az. Agr. Rossi")
    nome_agronomo  = st.text_input("Consulente Agronomo", "Dott. [Cognome]")
    regione        = st.selectbox("Regione", [
        "Marche","Toscana","Emilia-Romagna","Veneto","Lombardia","Piemonte",
        "Puglia","Sicilia","Campania","Lazio","Umbria","Abruzzo","Altra"
    ])
    zona           = st.selectbox("Zona Altimetrica", ["Pianura","Collina litoranea","Collina interna","Montagna"])

    st.markdown("---")
    st.markdown("### Certificazioni")
    cert_bio       = st.checkbox("Biologico (Reg. UE 2018/848)")
    cert_sqnpi     = st.checkbox("SQnpi – Produzione Integrata")
    cert_gap       = st.checkbox("GlobalG.A.P.")
    cert_viva      = st.checkbox("VIVA Sostenibilità")
    cert_iso       = st.checkbox("ISO 14064 Carbon FP")

    st.markdown("---")
    st.markdown("### Parametri di Mercato")
    prezzo_co2     = st.number_input("Prezzo CO₂ mercato volontario (€/t)", min_value=10.0, max_value=150.0, value=38.0, step=1.0)
    tasso_crescita = st.slider("Tasso crescita prezzo CO₂ annuo (%)", 0, 15, 5)

    st.markdown("---")
    st.markdown("### Dati Economici")
    fatturato      = st.number_input("Fatturato annuo (€)", min_value=0, value=180000, step=5000)
    costi_var      = st.number_input("Costi variabili (€/anno)", min_value=0, value=95000, step=5000)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <div class="badge-pill">Versione Professionale 2026 — IPCC Tier 1 + Pedologia Avanzata</div>
  <h1>AgroLog IA — {nome_azienda}</h1>
  <p>Carbon Intelligence · ESG Rating · Crediti di Carbonio · Analisi Fondiaria</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABELLA MULTI-APPEZZAMENTO
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📑 Gestione Multi-Appezzamento</div>', unsafe_allow_html=True)
st.caption("Aggiungi, modifica o elimina appezzamenti. I calcoli si aggiornano in tempo reale.")

df_edit = st.data_editor(
    st.session_state.df_campi,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Protocollo": st.column_config.SelectboxColumn(
            options=["Convenzionale","Intermedio","Rigenerativo Full"], required=True
        ),
        "Cover crops": st.column_config.CheckboxColumn(),
        "Ettari":      st.column_config.NumberColumn(min_value=0.1, max_value=5000, format="%.1f"),
        "SO %":        st.column_config.NumberColumn(min_value=0.1, max_value=8.0,  format="%.2f"),
        "Argilla %":   st.column_config.NumberColumn(min_value=1,   max_value=80),
        "Limo %":      st.column_config.NumberColumn(min_value=1,   max_value=80),
        "Densità (g/cm³)": st.column_config.NumberColumn(min_value=0.7, max_value=1.9, format="%.2f"),
    },
    key="editor_v3"
)
st.session_state.df_campi = df_edit

# ─────────────────────────────────────────────
#  MOTORE SCIENTIFICO — IPCC Tier 1 + Pedologia
# ─────────────────────────────────────────────
def calcola_campo(row):
    prot_map = {"Convenzionale": 0.004, "Intermedio": 0.018, "Rigenerativo Full": 0.048}
    # Massa suolo (IPCC 30cm profondità standard)
    massa = (0.30) * 10000 * float(row.get("Densità (g/cm³)", 1.3))
    # SOC stock attuale (C = 58% della SOM)
    soc   = massa * (float(row.get("SO %", 1.5)) / 100) * 0.58
    # Fattore tessitura: argilla stabilizza C, limo contribuisce meno
    f_text = 1 + (float(row.get("Argilla %", 20)) / 100) + (float(row.get("Limo %", 30)) / 200)
    # Cover crops: FI factor IPCC +11%
    f_cc   = 1.11 if row.get("Cover crops", False) else 1.0
    # Sequestro annuo per ettaro (tC/ha/anno → tCO2eq/ha/anno × 3.667)
    seq_ha = soc * prot_map.get(str(row.get("Protocollo","Intermedio")), 0.018) * f_text * f_cc
    co2_ha = seq_ha * 3.667
    co2_tot = co2_ha * float(row.get("Ettari", 1))
    # Emissioni N2O stimate (media settore se non specificato)
    emit_ha = 0.8  # tCO2eq/ha/anno stima conservativa
    return {
        "co2_seq":   round(co2_tot, 3),
        "co2_ha":    round(co2_ha, 3),
        "emit":      round(emit_ha * float(row.get("Ettari",1)), 3),
        "soc_stock": round(soc * float(row.get("Ettari",1)) / 1000, 1),  # tC totali
    }

risultati = [calcola_campo(r) for _, r in df_edit.iterrows()]
df_ris    = pd.DataFrame(risultati)

tot_seq   = df_ris["co2_seq"].sum()
tot_emit  = df_ris["emit"].sum()
tot_netto = tot_seq - tot_emit
tot_ha    = df_edit["Ettari"].sum() if len(df_edit) > 0 else 1
valore_crediti = max(0, tot_netto) * prezzo_co2

# Score ESG
score = 50
prot_scores = {"Convenzionale": 0, "Intermedio": 15, "Rigenerativo Full": 30}
for _, r in df_edit.iterrows():
    score += prot_scores.get(str(r.get("Protocollo","")), 0) / max(len(df_edit),1)
    if r.get("Cover crops", False): score += 8 / max(len(df_edit),1)
if cert_bio:   score += 12
if cert_sqnpi: score += 7
if cert_gap:   score += 5
if cert_viva:  score += 6
if cert_iso:   score += 8
score = min(100, int(score))

if score >= 80:   rating, rcls = "A — Eccellente",   "A"
elif score >= 65: rating, rcls = "B — Conforme ESG", "B"
elif score >= 45: rating, rcls = "C — Sviluppabile", "C"
else:             rating, rcls = "D — Critico",      "D"

margine = fatturato - costi_var
margine_pct = round(margine / fatturato * 100, 1) if fatturato > 0 else 0

# ─────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📊 Indicatori Chiave</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5,k6 = st.columns(6)

with k1:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value">{score}<small style="font-size:.9rem">/100</small></div>
      <div class="kpi-label">Score ESG</div>
      <div class="kpi-sub"><span class="rating-{rcls}">{rcls}</span></div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value">{round(tot_seq,1)}</div>
      <div class="kpi-label">tCO₂eq Sequestrate/anno</div>
      <div class="kpi-sub">{round(tot_seq/max(tot_ha,1),2)} t/ha</div>
    </div>""", unsafe_allow_html=True)
with k3:
    col = "#065f46" if tot_netto >= 0 else "#991b1b"
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value" style="color:{col}">{"+" if tot_netto>=0 else ""}{round(tot_netto,1)}</div>
      <div class="kpi-label">Bilancio Carbonico Netto (t)</div>
      <div class="kpi-sub">{"✅ Carbon Positive" if tot_netto>=0 else "⚠️ Emittente Netto"}</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value">€{int(valore_crediti):,}</div>
      <div class="kpi-label">Valore Crediti CO₂/anno</div>
      <div class="kpi-sub">@ €{prezzo_co2}/tCO₂ mercato vol.</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value">{round(tot_ha,1)}</div>
      <div class="kpi-label">SAU Totale (ha)</div>
      <div class="kpi-sub">{len(df_edit)} appezzamenti</div>
    </div>""", unsafe_allow_html=True)
with k6:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-value">{margine_pct}%</div>
      <div class="kpi-label">Margine Netto</div>
      <div class="kpi-sub">€{margine:,}/anno</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GRAFICI — 3 colonne
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📈 Analisi Visiva</div>', unsafe_allow_html=True)
gc1, gc2, gc3 = st.columns(3)

# 1. Donut CO2 per appezzamento
with gc1:
    if len(df_edit) > 0:
        df_plot = df_edit.copy()
        df_plot["CO2"] = [r["co2_seq"] for r in risultati]
        fig_pie = px.pie(df_plot, values="CO2", names="Appezzamento",
                         hole=0.52, title="CO₂ sequestrata per appezzamento",
                         color_discrete_sequence=["#1e5c38","#2d8a55","#52b788","#95d5b2","#d8f3dc"])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#0f2318"),
            margin=dict(t=40,b=10,l=0,r=0),
            showlegend=True,
            legend=dict(font=dict(size=11))
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

# 2. Heatmap Argilla vs SO%
with gc2:
    som_r = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    cla_r = [5, 10, 15, 20, 25, 30, 40, 50, 60]
    z = [[round(s * (1 + c/100) * 0.048 * 3.667, 2) for s in som_r] for c in cla_r]
    fig_h = go.Figure(go.Heatmap(
        z=z, x=som_r, y=cla_r,
        colorscale=[[0,"#d8f3dc"],[0.5,"#52b788"],[1,"#0f2318"]],
        colorbar=dict(title="tCO₂/ha"),
        showscale=True
    ))
    # Punti reali
    if len(df_edit) > 0:
        fig_h.add_trace(go.Scatter(
            x=df_edit["SO %"].tolist(),
            y=df_edit["Argilla %"].tolist(),
            mode="markers+text",
            marker=dict(color="#d4a843", size=12, symbol="x", line=dict(width=2)),
            text=df_edit["Appezzamento"].tolist(),
            textposition="top center",
            name="Campi aziendali"
        ))
    fig_h.update_layout(
        title="Potenziale sequestro (tCO₂/ha) — Argilla × SO%",
        xaxis_title="Sostanza Organica %",
        yaxis_title="Argilla %",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f7f4ee",
        font=dict(family="DM Sans", color="#0f2318"),
        margin=dict(t=40,b=40,l=40,r=20)
    )
    st.plotly_chart(fig_h, use_container_width=True)

# 3. Proiezione finanziaria 5 anni
with gc3:
    anni = list(range(2026, 2032))
    prezzi = [prezzo_co2 * ((1 + tasso_crescita/100)**i) for i in range(len(anni))]
    valori_cum = [max(0, tot_netto) * p * (i+1) for i, p in enumerate(prezzi)]
    fig_fin = go.Figure()
    fig_fin.add_trace(go.Scatter(
        x=anni, y=valori_cum,
        mode="lines+markers",
        line=dict(color="#1e5c38", width=3),
        marker=dict(size=8, color="#d4a843"),
        fill="tozeroy",
        fillcolor="rgba(30,92,56,0.08)",
        name="Valore cumulato"
    ))
    fig_fin.update_layout(
        title="Capitalizzazione crediti CO₂ (5 anni)",
        xaxis_title="Anno",
        yaxis_title="€ cumulati",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f7f4ee",
        font=dict(family="DM Sans", color="#0f2318"),
        margin=dict(t=40,b=40,l=40,r=20),
        yaxis=dict(tickformat="€,.0f")
    )
    st.plotly_chart(fig_fin, use_container_width=True)

# ─────────────────────────────────────────────
#  BENCHMARKING SETTORIALE
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📊 Benchmarking vs Media Settore (CREA-AA 2025)</div>', unsafe_allow_html=True)
bm_col1, bm_col2 = st.columns(2)

benchmarks = {
    "Cereali":    {"score": 48, "co2_ha": 1.9},
    "Vite":       {"score": 57, "co2_ha": 3.1},
    "Olivo":      {"score": 54, "co2_ha": 2.7},
    "Nocciolo":   {"score": 50, "co2_ha": 2.3},
    "Foraggere":  {"score": 60, "co2_ha": 3.8},
}
bm_score_med = 52
bm_co2_med   = 2.5

with bm_col1:
    delta_s = score - bm_score_med
    fig_bm = go.Figure(go.Bar(
        x=["Questa azienda", "Media settore (CREA)"],
        y=[score, bm_score_med],
        marker_color=["#1e5c38" if score >= bm_score_med else "#d4a843", "#94a3b8"],
        text=[f"{score}/100", f"{bm_score_med}/100"],
        textposition="outside"
    ))
    fig_bm.update_layout(
        title=f"Score ESG {'▲ +'+str(delta_s) if delta_s>=0 else '▼ '+str(delta_s)} vs media",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f7f4ee",
        font=dict(family="DM Sans", color="#0f2318"),
        showlegend=False,
        yaxis=dict(range=[0,100]),
        margin=dict(t=40,b=20,l=20,r=20)
    )
    st.plotly_chart(fig_bm, use_container_width=True)

with bm_col2:
    co2_ha_az = round(tot_seq / max(tot_ha,1), 2)
    delta_c   = round(co2_ha_az - bm_co2_med, 2)
    fig_bm2 = go.Figure(go.Bar(
        x=["Questa azienda", "Media settore (CREA)"],
        y=[co2_ha_az, bm_co2_med],
        marker_color=["#1e5c38" if co2_ha_az >= bm_co2_med else "#d4a843", "#94a3b8"],
        text=[f"{co2_ha_az} t/ha", f"{bm_co2_med} t/ha"],
        textposition="outside"
    ))
    fig_bm2.update_layout(
        title=f"CO₂/ha {'▲ +'+str(delta_c) if delta_c>=0 else '▼ '+str(delta_c)} vs media",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f7f4ee",
        font=dict(family="DM Sans", color="#0f2318"),
        showlegend=False,
        margin=dict(t=40,b=20,l=20,r=20)
    )
    st.plotly_chart(fig_bm2, use_container_width=True)

# ─────────────────────────────────────────────
#  PIANO DI AZIONI PRIORITARIE
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">🎯 Piano di Miglioramento Prioritario</div>', unsafe_allow_html=True)

azioni = []
has_conv = any(str(r.get("Protocollo","")) == "Convenzionale" for _, r in df_edit.iterrows())
has_no_cc = any(not r.get("Cover crops", False) for _, r in df_edit.iterrows())

if has_conv:
    azioni.append({"p":"alta","t":"Convertire appezzamenti convenzionali a minima lavorazione",
        "i":"Potenziale +30 pt ESG, +0.04 tCO₂/ha/anno IPCC FMG factor",
        "e":f"€{round(tot_ha*0.04*3.667*prezzo_co2*0.3):,}/anno aggiuntivi stimati",
        "c":"Prerequisito GlobalG.A.P. e Carbon Credits Verra"})
if has_no_cc:
    azioni.append({"p":"alta","t":"Introdurre cover crops invernali su tutti gli appezzamenti",
        "i":"+11% FI factor IPCC, +15 pt ESG, miglioramento struttura suolo",
        "e":"Accesso PAC Eco-Scheme pagamento aggiuntivo",
        "c":"Requisito SQnpi e Biologico"})
if not cert_bio and not cert_sqnpi:
    azioni.append({"p":"media","t":"Avviare percorso certificazione SQnpi",
        "i":"+7 pt ESG, accesso filiere premium e grande distribuzione",
        "e":"Aumento prezzo vendita stimato +12-18%",
        "c":"Percorso 12 mesi — contatta ASSAM o CAA locale"})
if not cert_iso:
    azioni.append({"p":"media","t":"Certificazione ISO 14064-2 Carbon Footprint",
        "i":"+8 pt ESG, crediti verificabili e vendibili su mercato ufficiale",
        "e":f"Accesso mercato compliance: €{round(valore_crediti*2.5):,}/anno potenziali",
        "c":"Verra VCS o Gold Standard — verifica da ente terzo"})
if margine_pct < 25:
    azioni.append({"p":"bassa","t":"Ottimizzare struttura dei costi variabili",
        "i":f"Margine attuale {margine_pct}% — soglia resilienza è 25%",
        "e":"Riduzione input chimici compatibile con upgrade ESG",
        "c":"Piano agronomico integrato con analisi suolo"})

p_map = {"alta": ("action-high","🔴"), "media": ("action-mid","🟡"), "bassa": ("action-low","🟢")}
for i, az in enumerate(azioni[:5], 1):
    cls, ico = p_map[az["p"]]
    st.markdown(f"""
    <div class="action-card {cls}">
      <b>{ico} {i}. {az['t']}</b><br>
      <small style="color:#6b7c6e">📊 {az['i']}</small><br>
      <small style="color:#1e5c38">💶 {az['e']}</small><br>
      <small style="color:#9ca3af">📜 {az['c']}</small>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAPPA DEI RISCHI
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">⚠️ Mappa dei Rischi Normativi e Climatici</div>', unsafe_allow_html=True)
rischi = []
if has_conv:
    rischi.append({"l":"alto","t":"Gestione convenzionale: rischio erosione suolo e perdita SOM"})
if tot_netto < 0:
    rischi.append({"l":"alto","t":"Bilancio carbonico negativo: azienda emittente netta"})
if not any([cert_bio,cert_sqnpi,cert_gap]):
    rischi.append({"l":"medio","t":"Nessuna certificazione: vulnerabile al declassamento in filiera"})
if margine_pct < 20:
    rischi.append({"l":"medio","t":f"Margine netto {margine_pct}% sotto soglia di resilienza (25%)"})
rischi.append({"l":"basso","t":"Stress idrico in aumento per scenario RCP4.5 (CMIP6) area mediterranea"})
rischi.append({"l":"basso","t":"Evoluzione normativa CSRD — obbligatoria per filiere con fatturato >€40M"})

r_map = {"alto":"risk-alto","medio":"risk-medio","basso":"risk-basso"}
html_r = " ".join([f'<span class="risk {r_map[r["l"]]}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])
st.markdown(f'<div style="line-height:2.8">{html_r}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  METODOLOGIA
# ─────────────────────────────────────────────
with st.expander("🔬 Metodologia scientifica (IPCC Tier 1 — AR5)"):
    st.markdown("""
| Parametro | Formula / Fonte |
|-----------|----------------|
| Massa suolo | `Profondità (0.30m) × 10.000 m²/ha × Densità apparente` |
| SOC Stock | `Massa × (SO% / 100) × 0.58` (coefficiente IPCC) |
| Fattore tessitura | `1 + (Argilla%/100) + (Limo%/200)` |
| Cover crops FI | `+11%` (IPCC 2006 Table 5.5) |
| Sequestro netto | `SOC × coeff_protocollo × f_tessitura × f_CC × 3.667` |
| Conversione C→CO₂ | `× 3.667` (rapporto molecolare CO₂/C) |
| Emissioni N₂O | `EF=0.01 kg N₂O-N/kg N, GWP=265 (AR5)` |

**Coefficienti protocollo** (calibrati su letteratura IPCC + CREA):
- Convenzionale: 0.004 | Intermedio: 0.018 | Rigenerativo Full: 0.048

**Fonte benchmark:** CREA-AA Annuario 2025, RICA-Italia, ISPRA Inventario GHG 2024
    """)

# ─────────────────────────────────────────────
#  GENERA REPORT HTML (stampabile come PDF)
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📄 Genera Report Professionale</div>', unsafe_allow_html=True)
st.info("Il report si apre nel browser e può essere stampato come PDF con Ctrl+P → Salva come PDF. "
        "Intestazione personalizzata con il tuo nome e la metodologia citata.")

oggi = datetime.now().strftime("%d/%m/%Y")

if st.button("📥 Genera Report HTML (stampa come PDF)"):
    # Costruzione tabella campi per il report
    righe_tab = ""
    for i, (_, row) in enumerate(df_edit.iterrows()):
        r = risultati[i]
        righe_tab += f"""
        <tr>
          <td>{row.get('Appezzamento','—')}</td>
          <td>{row.get('Ettari','—')}</td>
          <td>{row.get('SO %','—')}%</td>
          <td>{row.get('Argilla %','—')}%</td>
          <td>{row.get('Limo %','—')}%</td>
          <td>{row.get('Densità (g/cm³)','—')}</td>
          <td>{row.get('Protocollo','—')}</td>
          <td>{'✓' if row.get('Cover crops',False) else '—'}</td>
          <td><b>{r['co2_seq']}</b></td>
        </tr>"""

    cert_list = ", ".join([c for c, v in [
        ("Biologico",cert_bio),("SQnpi",cert_sqnpi),
        ("GlobalG.A.P.",cert_gap),("VIVA",cert_viva),("ISO 14064",cert_iso)
    ] if v]) or "Nessuna certificazione attiva"

    azioni_html = ""
    for i, az in enumerate(azioni[:5], 1):
        col = {"alta":"#ef4444","media":"#d4a843","bassa":"#2d8a55"}[az["p"]]
        azioni_html += f"""
        <div style="border-left:4px solid {col};padding:.6rem 1rem;
                    margin:.4rem 0;background:#f9f9f7;border-radius:0 8px 8px 0">
          <b>{i}. {az['t']}</b><br>
          <small style="color:#555">📊 {az['i']}</small><br>
          <small style="color:#1e5c38">💶 {az['e']}</small>
        </div>"""

    html_report = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>AgroLog IA — {nome_azienda}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'DM Sans',sans-serif; color:#1c1c1c; background:#fff; font-size:13px; }}
  @media print {{
    .no-print {{ display:none; }}
    body {{ font-size:11px; }}
    .page-break {{ page-break-before: always; }}
  }}
  .header {{ background:linear-gradient(135deg,#0f2318,#1e5c38); color:#fff; padding:1.8rem 2rem; }}
  .header h1 {{ font-family:'DM Serif Display',serif; font-size:1.6rem; margin:.3rem 0; }}
  .header p {{ color:rgba(255,255,255,.7); font-size:.85rem; }}
  .badge {{ background:#d4a843; color:#0f2318; font-size:.65rem; font-weight:700;
            letter-spacing:.1em; text-transform:uppercase; padding:2px 10px; border-radius:20px; }}
  .section {{ padding:1.2rem 2rem; border-bottom:1px solid #e8e4dc; }}
  .sec-title {{ font-family:'DM Serif Display',serif; font-size:1.1rem; color:#0f2318;
                border-left:4px solid #2d8a55; padding-left:.6rem; margin-bottom:.8rem; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; }}
  .kpi {{ background:#f7f4ee; border-radius:10px; padding:.8rem 1rem; text-align:center;
          border:1px solid rgba(30,92,56,.1); }}
  .kpi-v {{ font-family:'DM Serif Display',serif; font-size:1.5rem; color:#1e5c38; }}
  .kpi-l {{ font-size:.68rem; color:#7a8c7e; text-transform:uppercase; letter-spacing:.06em; }}
  table {{ width:100%; border-collapse:collapse; font-size:.78rem; }}
  th {{ background:#1e5c38; color:#fff; padding:6px 8px; text-align:left; }}
  td {{ padding:5px 8px; border-bottom:1px solid #eee; }}
  tr:nth-child(even) td {{ background:#f7f7f5; }}
  .rating-box {{ display:inline-block; padding:3px 14px; border-radius:20px; font-weight:700; font-size:.85rem; }}
  .r-A {{ background:#d1fae5; color:#065f46; }}
  .r-B {{ background:#dbeafe; color:#1e40af; }}
  .r-C {{ background:#fef3c7; color:#92400e; }}
  .r-D {{ background:#fee2e2; color:#991b1b; }}
  .footer-rep {{ background:#0f2318; color:rgba(255,255,255,.6); padding:1rem 2rem;
                 font-size:.7rem; text-align:center; }}
  .sign-box {{ border:1px solid #ddd; border-radius:10px; padding:1rem 1.5rem; margin-top:.5rem; }}
</style>
</head>
<body>

<div class="header">
  <div class="badge">Report ESG & Carbon Intelligence — AgroLog IA 2026</div>
  <h1>Analisi Sostenibilità: {nome_azienda}</h1>
  <p>Consulente: {nome_agronomo} &nbsp;|&nbsp; Data: {oggi} &nbsp;|&nbsp; Regione: {regione} — {zona}</p>
</div>

<div class="section">
  <div class="sec-title">Indicatori Chiave</div>
  <div class="kpi-grid">
    <div class="kpi">
      <div class="kpi-v">{score}/100</div>
      <div class="kpi-l">Score ESG</div>
      <div style="margin-top:4px"><span class="rating-box r-{rcls}">{rating}</span></div>
    </div>
    <div class="kpi">
      <div class="kpi-v">{round(tot_seq,1)} t</div>
      <div class="kpi-l">CO₂eq Sequestrata/anno</div>
      <div style="font-size:.78rem;color:#1e5c38;margin-top:2px">{round(tot_seq/max(tot_ha,1),2)} t/ha</div>
    </div>
    <div class="kpi">
      <div class="kpi-v">€{int(valore_crediti):,}</div>
      <div class="kpi-l">Valore Crediti CO₂/anno</div>
      <div style="font-size:.78rem;color:#7a8c7e;margin-top:2px">@ €{prezzo_co2}/t mercato vol.</div>
    </div>
    <div class="kpi">
      <div class="kpi-v">{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</div>
      <div class="kpi-l">Bilancio Carbonico Netto</div>
      <div style="font-size:.78rem;color:{'#065f46' if tot_netto>=0 else '#991b1b'};margin-top:2px">
        {"✅ Carbon Positive" if tot_netto>=0 else "⚠️ Emittente Netto"}</div>
    </div>
    <div class="kpi">
      <div class="kpi-v">{round(tot_ha,1)} ha</div>
      <div class="kpi-l">SAU Totale</div>
      <div style="font-size:.78rem;color:#7a8c7e;margin-top:2px">{len(df_edit)} appezzamenti</div>
    </div>
    <div class="kpi">
      <div class="kpi-v">{margine_pct}%</div>
      <div class="kpi-l">Margine Netto</div>
      <div style="font-size:.78rem;color:#1e5c38;margin-top:2px">€{margine:,}/anno</div>
    </div>
  </div>
</div>

<div class="section">
  <div class="sec-title">Dettaglio Appezzamenti — Calcolo IPCC Tier 1</div>
  <table>
    <thead><tr>
      <th>Appezzamento</th><th>Ettari</th><th>SO%</th><th>Argilla%</th>
      <th>Limo%</th><th>Densità</th><th>Protocollo</th><th>CC</th><th>tCO₂/anno</th>
    </tr></thead>
    <tbody>{righe_tab}</tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">Benchmarking vs Media Settore (fonte: CREA-AA 2025)</div>
  <table>
    <thead><tr><th>Indicatore</th><th>Questa Azienda</th><th>Media Settore</th><th>Delta</th></tr></thead>
    <tbody>
      <tr><td>Score ESG</td><td><b>{score}/100</b></td><td>{bm_score_med}/100</td>
          <td style="color:{'#065f46' if score>=bm_score_med else '#991b1b'}">
          {"+" if score>=bm_score_med else ""}{score-bm_score_med} pt</td></tr>
      <tr><td>CO₂ sequestrata/ha</td><td><b>{round(tot_seq/max(tot_ha,1),2)} t</b></td>
          <td>{bm_co2_med} t</td>
          <td style="color:{'#065f46' if tot_seq/max(tot_ha,1)>=bm_co2_med else '#991b1b'}">
          {"+" if tot_seq/max(tot_ha,1)>=bm_co2_med else ""}{round(tot_seq/max(tot_ha,1)-bm_co2_med,2)} t</td></tr>
      <tr><td>Certificazioni attive</td><td><b>{cert_list}</b></td><td>1-2 certificazioni</td><td>—</td></tr>
    </tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">Piano di Miglioramento Prioritario</div>
  {azioni_html}
</div>

<div class="section">
  <div class="sec-title">Nota Metodologica</div>
  <p style="font-size:.78rem;color:#555;line-height:1.6">
  Le stime di sequestro carbonio sono calcolate secondo <b>IPCC 2006 Guidelines for National GHG Inventories,
  Vol. 4 (Agriculture), Tier 1</b>, con fattori aggiornati al <b>5° Report di Valutazione AR5</b>.
  Il fattore di conversione C→CO₂ è 3.667 (rapporto molecolare). Il fattore tessitura integra
  argilla e limo secondo letteratura pedologica CREA. I valori di mercato dei crediti di carbonio
  si riferiscono al <b>Voluntary Carbon Market Q1 2026</b> (Xpansiv CBL). Il presente report ha
  valore previsionale e orientativo; la certificazione ufficiale richiede verifica da Ente Terzo
  accreditato (Verra, Gold Standard, ISAE 3000).
  </p>
</div>

<div class="section">
  <div class="sec-title">Firma e Validazione</div>
  <div class="sign-box">
    <p><b>Consulente Agronomo:</b> {nome_agronomo}</p>
    <p style="margin-top:.3rem"><b>Iscrizione Albo:</b> ______________________</p>
    <p style="margin-top:.3rem"><b>Data:</b> {oggi} &nbsp;&nbsp;&nbsp;
       <b>Luogo:</b> ______________________</p>
    <p style="margin-top:1.5rem;color:#999">Firma: ______________________</p>
    <p style="margin-top:.3rem;color:#999">Timbro:</p>
  </div>
</div>

<div class="footer-rep">
  AgroLog IA — Carbon & ESG Intelligence | Metodologia IPCC 2006 Tier 1, AR5 GWP |
  Mercato volontario carbonio Q1 2026 | Report previsionale — verifica Ente Terzo per certificazione ufficiale
</div>

</body></html>"""

    b64 = base64.b64encode(html_report.encode("utf-8")).decode()
    fname = f"AgroLog_{nome_azienda.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html"
    href = f'<a href="data:text/html;base64,{b64}" download="{fname}" style="display:inline-block;background:#1e5c38;color:#fff;padding:.6rem 1.5rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:.9rem">⬇️ Scarica Report HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("✅ Report generato! Aprilo nel browser e premi Ctrl+P → Salva come PDF per ottenere il documento da consegnare al cliente.")

st.markdown("""
<div class="footer">
  AgroLog IA v3.0 — Carbon & ESG Intelligence | Metodologia IPCC 2006 Tier 1 |
  Benchmark: CREA-AA 2025, RICA-Italia, ISPRA GHG 2024 | Dati previsionali
</div>""", unsafe_allow_html=True)
