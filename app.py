import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests, json, base64, math

# ══════════════════════════════════════════════════════════════
#  CONFIGURAZIONE
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgroLog IA | Carbon & ESG Strategic Intelligence",
    page_icon="🌿", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#f5f2eb;}

.hero{background:linear-gradient(135deg,#061912 0%,#0f3d22 45%,#1a6b3a 100%);
  padding:2.2rem 2.5rem;border-radius:18px;margin-bottom:1.8rem;
  box-shadow:0 8px 32px rgba(6,25,18,.18);}
.hero h1{font-family:'DM Serif Display',serif;color:#fff;font-size:2rem;margin:.3rem 0;}
.hero p{color:rgba(255,255,255,.65);font-size:.88rem;margin:0;}
.hero-badge{background:#c9963a;color:#061912;font-size:.65rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;border-radius:20px;
  margin-bottom:.6rem;display:inline-block;}

.kpi{background:#fff;border-radius:14px;padding:1.1rem 1.3rem;
  border:1px solid rgba(15,61,34,.1);box-shadow:0 2px 10px rgba(6,25,18,.05);
  text-align:center;height:100%;}
.kpi-v{font-family:'DM Serif Display',serif;font-size:1.75rem;color:#0f3d22;line-height:1.1;}
.kpi-l{font-size:.65rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.08em;margin-top:.3rem;}
.kpi-s{font-size:.78rem;color:#1a6b3a;font-weight:600;margin-top:.15rem;}

.sec{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#061912;
  border-left:5px solid #1a6b3a;padding-left:.7rem;margin:2rem 0 1rem;}

.action{background:#fff;border-radius:11px;padding:.85rem 1.1rem;margin:.35rem 0;
  border:1px solid rgba(15,61,34,.1);}
.act-h{border-left:4px solid #ef4444;}
.act-m{border-left:4px solid #c9963a;}
.act-l{border-left:4px solid #1a6b3a;}

.risk{display:inline-block;padding:3px 11px;border-radius:20px;font-size:.7rem;font-weight:600;margin:2px;}
.r-alto{background:#fee2e2;color:#991b1b;}
.r-medio{background:#fef3c7;color:#92400e;}
.r-basso{background:#d1fae5;color:#065f46;}

.weather-box{background:linear-gradient(135deg,#0a3d62,#1a6b3a);
  border-radius:14px;padding:1.2rem 1.5rem;color:#fff;margin-bottom:1rem;}
.weather-box h3{margin:0 0 .5rem;font-family:'DM Serif Display',serif;font-size:1.1rem;}

.scenario-card{border-radius:12px;padding:1rem 1.2rem;border:2px dashed;}
.s-base{background:#f0fdf4;border-color:#1a6b3a;}
.s-opt{background:#fefce8;border-color:#c9963a;}
.s-best{background:#eff6ff;border-color:#3b82f6;}

div[data-testid="stSidebar"]{background:#061912;}
div[data-testid="stSidebar"] *{color:rgba(255,255,255,.85)!important;}
div[data-testid="stSidebar"] h2,div[data-testid="stSidebar"] h3{
  font-family:'DM Serif Display',serif!important;color:#fff!important;}
div[data-testid="stSidebar"] label{
  font-size:.75rem!important;text-transform:uppercase;
  letter-spacing:.05em;color:rgba(255,255,255,.55)!important;}
div[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.12)!important;}

.stButton>button{background:#0f3d22!important;color:#fff!important;
  border:none!important;border-radius:8px!important;font-weight:600!important;}
.stButton>button:hover{background:#061912!important;}

.footer{font-size:.68rem;color:#9aab9e;text-align:center;margin-top:2rem;
  padding-top:1rem;border-top:1px solid rgba(15,61,34,.12);}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COSTANTI SCIENTIFICHE
# ══════════════════════════════════════════════════════════════
COORDS_REGIONI = {
    "Marche":         (43.62, 13.51), "Toscana":        (43.46, 11.10),
    "Emilia-Romagna": (44.50, 11.34), "Veneto":         (45.44, 11.88),
    "Lombardia":      (45.46,  9.19), "Piemonte":       (45.07,  7.68),
    "Puglia":         (41.12, 16.87), "Sicilia":        (37.60, 14.02),
    "Campania":       (40.83, 14.25), "Lazio":          (41.90, 12.49),
    "Umbria":         (43.11, 12.39), "Abruzzo":        (42.35, 13.39),
    "Calabria":       (38.90, 16.59), "Sardegna":       (40.12,  9.01),
    "Altra":          (42.50, 12.50),
}
SOC_REF = {"Pianura":47.8,"Collina litoranea":39.3,"Collina interna":37.1,"Montagna":31.5}
F_CLIMA  = {"Pianura":0.93,"Collina litoranea":0.97,"Collina interna":1.04,"Montagna":1.16}
PROTOCOLLI = {
    "Convenzionale":     {"fmg":0.82,"diesel":145,"n_kg_ha":110,"co2_coeff":0.004},
    "Intermedio":        {"fmg":1.00,"diesel": 85,"n_kg_ha": 75,"co2_coeff":0.021},
    "Rigenerativo Full": {"fmg":1.15,"diesel": 42,"n_kg_ha": 35,"co2_coeff":0.052},
}
COLTURE_KC = {
    "Cereali":1.15,"Vite (DOC/IGT)":0.70,"Olivo":0.65,"Nocciolo":0.80,
    "Frutteto":1.10,"Orticole":1.20,"Foraggere":1.00,"Misto":0.90,
}
EF_N2O   = 0.01   # kg N2O-N per kg N (IPCC)
GWP_N2O  = 265    # AR5
GWP_CO2  = 1
DIESEL_KG_CO2 = 2.68
PREZZO_ACQUA  = 0.45  # €/m³ irrigazione

# ══════════════════════════════════════════════════════════════
#  DATI DEFAULT
# ══════════════════════════════════════════════════════════════
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Appezzamento":"Campo Nord","Ettari":12.0,"SO %":1.8,"Argilla %":28,
         "Limo %":32,"Densità":1.30,"Protocollo":"Convenzionale","Cover crops":False,
         "Coltura":"Cereali","Irrigazione m³/ha":800},
        {"Appezzamento":"Vigneto Sud","Ettari":6.0,"SO %":1.4,"Argilla %":18,
         "Limo %":40,"Densità":1.42,"Protocollo":"Intermedio","Cover crops":False,
         "Coltura":"Vite (DOC/IGT)","Irrigazione m³/ha":300},
        {"Appezzamento":"Oliveto","Ettari":4.5,"SO %":2.1,"Argilla %":24,
         "Limo %":35,"Densità":1.25,"Protocollo":"Rigenerativo Full","Cover crops":True,
         "Coltura":"Olivo","Irrigazione m³/ha":0},
    ])

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌿 AgroLog IA")
    st.markdown("*Carbon & ESG Strategic Intelligence*")
    st.markdown("---")
    st.markdown("### Anagrafica")
    nome_az    = st.text_input("Ragione Sociale", "Az. Agr. Rossi")
    agronomo   = st.text_input("Dottore Agronomo", "Dott. [Cognome]")
    regione    = st.selectbox("Regione", list(COORDS_REGIONI.keys()))
    zona       = st.selectbox("Zona Altimetrica", list(SOC_REF.keys()))

    st.markdown("---")
    st.markdown("### Certificazioni Attive")
    cert_bio   = st.checkbox("Biologico (Reg. UE 2018/848)")
    cert_sqnpi = st.checkbox("SQnpi")
    cert_gap   = st.checkbox("GlobalG.A.P.")
    cert_viva  = st.checkbox("VIVA Sostenibilità")
    cert_iso   = st.checkbox("ISO 14064")
    cert_csrd  = st.checkbox("CSRD / ESRS")

    st.markdown("---")
    st.markdown("### Mercato & Finanza")
    prezzo_co2      = st.number_input("Prezzo CO₂ (€/t)", 10.0, 200.0, 38.0, 1.0)
    crescita_co2    = st.slider("Crescita prezzo CO₂/anno (%)", 0, 20, 7)
    costo_diesel    = st.number_input("Gasolio agricolo (€/L)", 0.7, 2.5, 1.15, 0.05)
    fatturato       = st.number_input("Fatturato (€/anno)", 0, 5000000, 200000, 5000)
    costi_var       = st.number_input("Costi variabili (€/anno)", 0, 5000000, 105000, 5000)
    costo_acqua     = st.number_input("Costo irrigazione (€/m³)", 0.1, 2.0, 0.45, 0.05)

    st.markdown("---")
    st.markdown("### Investimento Tecnologico")
    inv_sensori     = st.checkbox("Sensori IoT suolo (Costo: €3.500)")
    inv_drip        = st.checkbox("Drip irrigation (Costo: €6.000/ha)")
    inv_precision   = st.checkbox("Precision farming GPS (Costo: €8.000)")
    inv_biochar     = st.checkbox("Applicazione Biochar (Costo: €1.200/ha)")

# ══════════════════════════════════════════════════════════════
#  METEO LIVE — Open-Meteo (gratuito, no API key)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_meteo(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast"
               f"?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
               f"et0_fao_evapotranspiration,wind_speed_10m_max,soil_moisture_0_to_7cm"
               f"&timezone=Europe/Rome&forecast_days=7")
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

@st.cache_data(ttl=86400)
def get_meteo_storico(lat, lon):
    """Ultimi 30 giorni per calcolare ET0 media e stress idrico"""
    try:
        from datetime import date, timedelta
        end = date.today().strftime("%Y-%m-%d")
        start = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        url = (f"https://archive-api.open-meteo.com/v1/archive"
               f"?latitude={lat}&longitude={lon}"
               f"&start_date={start}&end_date={end}"
               f"&daily=precipitation_sum,et0_fao_evapotranspiration,temperature_2m_mean"
               f"&timezone=Europe/Rome")
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

lat, lon = COORDS_REGIONI.get(regione, (42.5, 12.5))
meteo_data    = get_meteo(lat, lon)
meteo_storico = get_meteo_storico(lat, lon)

# Estrai dati meteo
def parse_meteo(md, ms):
    out = {"temp_max":22,"temp_min":10,"pioggia_7g":15,"et0_media":3.5,
           "vento_max":25,"umidita_suolo":0.25,"precipitazioni_30g":45,
           "et0_30g":85,"temp_media_30g":14}
    if md and "daily" in md:
        d = md["daily"]
        out["temp_max"]      = round(np.mean(d.get("temperature_2m_max",[22])),1)
        out["temp_min"]      = round(np.mean(d.get("temperature_2m_min",[10])),1)
        out["pioggia_7g"]    = round(sum(d.get("precipitation_sum",[0]*7)),1)
        et0_list = [x for x in d.get("et0_fao_evapotranspiration",[3.5]*7) if x is not None]
        out["et0_media"]     = round(np.mean(et0_list) if et0_list else 3.5, 2)
        out["vento_max"]     = round(max(d.get("wind_speed_10m_max",[25])),1)
        sm_list = [x for x in d.get("soil_moisture_0_to_7cm",[0.25]*7) if x is not None]
        out["umidita_suolo"] = round(np.mean(sm_list) if sm_list else 0.25, 3)
    if ms and "daily" in ms:
        d = ms["daily"]
        p = [x for x in d.get("precipitation_sum",[]) if x is not None]
        e = [x for x in d.get("et0_fao_evapotranspiration",[]) if x is not None]
        t = [x for x in d.get("temperature_2m_mean",[]) if x is not None]
        if p: out["precipitazioni_30g"] = round(sum(p),1)
        if e: out["et0_30g"]            = round(sum(e),1)
        if t: out["temp_media_30g"]     = round(np.mean(t),1)
    return out

meteo = parse_meteo(meteo_data, meteo_storico)

# Indice stress idrico (0=no stress, 1=stress totale)
deficit_idrico = max(0, meteo["et0_30g"] - meteo["precipitazioni_30g"])
stress_idrico  = min(1.0, deficit_idrico / 80)  # 80mm = soglia critica

# ══════════════════════════════════════════════════════════════
#  MOTORE SCIENTIFICO UNIFICATO
# ══════════════════════════════════════════════════════════════
def calcola_campo(row, zona, meteo, scenario_boost=False):
    prot = "Rigenerativo Full" if scenario_boost else str(row.get("Protocollo","Intermedio"))
    p    = PROTOCOLLI.get(prot, PROTOCOLLI["Intermedio"])
    ha   = float(row.get("Ettari", 1))

    # 1. CARBONIO — IPCC Tier 1 + pedologia avanzata
    densita = float(row.get("Densità", 1.3))
    so_pct  = float(row.get("SO %", 1.5))
    arg_pct = float(row.get("Argilla %", 20))
    lim_pct = float(row.get("Limo %", 30))
    massa   = 0.30 * 10000 * densita
    soc     = massa * (so_pct / 100) * 0.58                          # tC/ha
    f_text  = 1 + (arg_pct/100) + (lim_pct/200)                      # stabilizzazione minerale
    f_cc    = 1.15 if (row.get("Cover crops", False) or scenario_boost) else 1.0
    f_clim  = F_CLIMA.get(zona, 1.0)
    soc_ref = SOC_REF.get(zona, 40.0)
    f_mg    = p["fmg"]
    seq_ha  = soc * p["co2_coeff"] * f_text * f_cc * f_clim * f_mg
    co2_seq = seq_ha * 3.667 * ha                                     # tCO2eq/anno

    # 2. EMISSIONI dirette
    n_kg     = p["n_kg_ha"] * ha
    n2o_co2  = n_kg * EF_N2O * (44/28) * GWP_N2O / 1000             # tCO2eq
    diesel_l = p["diesel"] * ha
    diesel_c = diesel_l * DIESEL_KG_CO2 / 1000                       # tCO2eq
    co2_emit = n2o_co2 + diesel_c

    # 3. ACQUA — FAO Penman-Monteith semplificato
    coltura  = str(row.get("Coltura","Cereali"))
    kc       = COLTURE_KC.get(coltura, 1.0)
    et0_ann  = meteo["et0_media"] * 365                               # mm/anno stimato
    etc_ann  = et0_ann * kc                                           # mm/anno fabbisogno
    pioggia_eff = meteo["precipitazioni_30g"] * 12 * 0.85            # mm/anno pioggia efficace
    fabbisogno_irr = max(0, etc_ann - pioggia_eff) * 10 * ha         # m³/anno
    irr_attuale    = float(row.get("Irrigazione m³/ha", 0)) * ha
    spreco_acqua   = max(0, irr_attuale - fabbisogno_irr)

    # SOM aumenta ritenzione idrica: ogni +0.1% SO → +1.5 mm/m profondità
    capacita_extra = (so_pct - 1.0) * 1.5 * (0.30 / 0.10) * 10 * ha # m³ extra
    if scenario_boost:
        so_target      = min(so_pct * 1.15, 5.0)
        capacita_extra_pot = (so_target - 1.0) * 1.5 * 3 * 10 * ha
        risparmio_acqua = (capacita_extra_pot - capacita_extra) * 0.7
    else:
        risparmio_acqua = 0

    # Stress idrico: riduce produttività
    riduz_produt   = stress_idrico * 0.18  # max -18% resa

    # 4. COSTI gasolio + fertilizzanti
    costo_diesel_ha  = diesel_l * costo_diesel
    costo_n_ha       = n_kg * 0.85  # €/kg N medio 2026
    costo_irr        = irr_attuale * costo_acqua

    # 5. VALORE FONDIARIO — incremento per SOC
    plusvalore_ha    = (so_pct / 1.2 - 1) * 0.12 * 15000  # €/ha rispetto a media
    valore_fondo     = ha * (15000 + plusvalore_ha)

    return {
        "co2_seq":          round(co2_seq, 3),
        "co2_emit":         round(co2_emit, 3),
        "co2_netto":        round(co2_seq - co2_emit, 3),
        "n2o":              round(n2o_co2, 3),
        "diesel_co2":       round(diesel_c, 3),
        "diesel_l":         round(diesel_l, 0),
        "fabbisogno_irr":   round(fabbisogno_irr, 0),
        "irr_attuale":      round(irr_attuale, 0),
        "spreco_acqua":     round(spreco_acqua, 0),
        "capacita_extra":   round(capacita_extra, 0),
        "risparmio_acqua":  round(risparmio_acqua, 0),
        "riduz_produt_pct": round(riduz_produt * 100, 1),
        "costo_diesel_tot": round(costo_diesel_ha, 0),
        "costo_n_tot":      round(costo_n_ha, 0),
        "costo_irr":        round(costo_irr, 0),
        "valore_fondo":     round(valore_fondo, 0),
        "seq_ha":           round(seq_ha * 3.667, 3),
    }

# ══════════════════════════════════════════════════════════════
#  TABELLA APPEZZAMENTI
# ══════════════════════════════════════════════════════════════
df_edit = st.session_state.df_campi

st.markdown(f"""
<div class="hero">
  <div class="hero-badge">Platform Pro 2026 · IPCC Tier 1 · Meteo Live · FAO Water · ROI Engine</div>
  <h1>🌿 {nome_az} — Carbon & ESG Intelligence</h1>
  <p>Consulente: {agronomo} &nbsp;·&nbsp; {regione} / {zona} &nbsp;·&nbsp; {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
</div>
""", unsafe_allow_html=True)

# ── METEO LIVE ────────────────────────────────────────────────
st.markdown('<div class="sec">🌦️ Meteo Live & Stress Idrico</div>', unsafe_allow_html=True)
mc1,mc2,mc3,mc4,mc5,mc6 = st.columns(6)
meteo_kpis = [
    (f"{meteo['temp_max']}°C / {meteo['temp_min']}°C","Temp. Max/Min","7 giorni"),
    (f"{meteo['pioggia_7g']} mm","Pioggia prevista","prossimi 7gg"),
    (f"{meteo['et0_media']} mm/g","ET₀ FAO","evapotraspirazione"),
    (f"{meteo['precipitazioni_30g']} mm","Pioggia storica","ultimi 30gg"),
    (f"{meteo['et0_30g']} mm","ET₀ storica","ultimi 30gg"),
    (f"{round(stress_idrico*100,0):.0f}%","Stress Idrico","indice attuale"),
]
for col, (v, l, s) in zip([mc1,mc2,mc3,mc4,mc5,mc6], meteo_kpis):
    col_color = "#991b1b" if "Stress" in l and stress_idrico > 0.5 else "#1a6b3a"
    with col:
        st.markdown(f"""<div class="kpi">
          <div class="kpi-v" style="font-size:1.35rem;color:{col_color}">{v}</div>
          <div class="kpi-l">{l}</div>
          <div class="kpi-s" style="color:#7a8c7e">{s}</div>
        </div>""", unsafe_allow_html=True)

if stress_idrico > 0.4:
    st.warning(f"⚠️ **Stress idrico elevato ({round(stress_idrico*100)}%)** — deficit idrico stimato di {round(deficit_idrico,0)} mm negli ultimi 30 giorni. Rischio riduzione resa fino a {round(stress_idrico*18,1)}%. Valutare irrigazione di soccorso.")
elif stress_idrico > 0.2:
    st.info(f"ℹ️ Stress idrico moderato ({round(stress_idrico*100)}%) — monitorare umidità suolo nelle prossime 2 settimane.")
else:
    st.success(f"✅ Bilancio idrico equilibrato — precipitazioni adeguate al fabbisogno colturale.")

# ── TABELLA MULTI-APPEZZAMENTO ────────────────────────────────
st.markdown('<div class="sec">📑 Inventario Fondiario</div>', unsafe_allow_html=True)
st.caption("Modifica i dati — tutti i calcoli si aggiornano in tempo reale.")

df_edit = st.data_editor(
    st.session_state.df_campi, num_rows="dynamic", use_container_width=True,
    column_config={
        "Protocollo":  st.column_config.SelectboxColumn(
            options=["Convenzionale","Intermedio","Rigenerativo Full"], required=True),
        "Cover crops": st.column_config.CheckboxColumn(),
        "Coltura":     st.column_config.SelectboxColumn(
            options=list(COLTURE_KC.keys()), required=True),
        "Ettari":             st.column_config.NumberColumn(min_value=0.1,max_value=5000,format="%.1f"),
        "SO %":               st.column_config.NumberColumn(min_value=0.1,max_value=8.0,format="%.2f"),
        "Argilla %":          st.column_config.NumberColumn(min_value=1,max_value=80),
        "Limo %":             st.column_config.NumberColumn(min_value=1,max_value=80),
        "Densità":            st.column_config.NumberColumn(min_value=0.7,max_value=1.9,format="%.2f"),
        "Irrigazione m³/ha":  st.column_config.NumberColumn(min_value=0,max_value=10000),
    }, key="editor_v4"
)
st.session_state.df_campi = df_edit

# ══════════════════════════════════════════════════════════════
#  CALCOLO AGGREGATO
# ══════════════════════════════════════════════════════════════
res_att  = [calcola_campo(r, zona, meteo, False) for _, r in df_edit.iterrows()]
res_pot  = [calcola_campo(r, zona, meteo, True)  for _, r in df_edit.iterrows()]

tot_ha        = float(df_edit["Ettari"].sum()) if len(df_edit)>0 else 1
tot_seq       = sum(r["co2_seq"]   for r in res_att)
tot_emit      = sum(r["co2_emit"]  for r in res_att)
tot_netto     = tot_seq - tot_emit
tot_diesel_l  = sum(r["diesel_l"]  for r in res_att)
tot_costo_die = sum(r["costo_diesel_tot"] for r in res_att)
tot_costo_n   = sum(r["costo_n_tot"]      for r in res_att)
tot_irr_att   = sum(r["irr_attuale"]      for r in res_att)
tot_fabb_irr  = sum(r["fabbisogno_irr"]   for r in res_att)
tot_spreco_h2o= sum(r["spreco_acqua"]     for r in res_att)
tot_cap_extra = sum(r["capacita_extra"]   for r in res_att)
tot_costo_irr = sum(r["costo_irr"]        for r in res_att)
tot_valore_f  = sum(r["valore_fondo"]     for r in res_att)
valore_crediti= max(0, tot_netto) * prezzo_co2
margine       = fatturato - costi_var
margine_pct   = round(margine/fatturato*100,1) if fatturato > 0 else 0

# Scenario ottimistico
pot_seq   = sum(r["co2_seq"]          for r in res_pot)
pot_emit  = sum(r["co2_emit"]         for r in res_pot)
pot_netto = pot_seq - pot_emit
pot_diesel= sum(r["diesel_l"]         for r in res_pot)
pot_risp_h= sum(r["risparmio_acqua"]  for r in res_pot)
pot_cred  = max(0, pot_netto) * prezzo_co2
risp_diesel_eur = (tot_diesel_l - pot_diesel) * costo_diesel
risp_h2o_eur    = pot_risp_h * costo_acqua
extra_cred_eur  = pot_cred - valore_crediti
guadagno_tot    = risp_diesel_eur + risp_h2o_eur + extra_cred_eur

# Score ESG completo
score = 30
if tot_netto/max(tot_ha,1) > 1.5: score += 20
elif tot_netto/max(tot_ha,1) > 0:  score += 10
if cert_bio:   score += 14
if cert_sqnpi: score += 8
if cert_gap:   score += 7
if cert_viva:  score += 8
if cert_iso:   score += 10
if cert_csrd:  score += 8
cc_pct = sum(1 for _,r in df_edit.iterrows() if r.get("Cover crops",False)) / max(len(df_edit),1)
score += int(cc_pct * 12)
if tot_spreco_h2o < tot_fabb_irr * 0.1: score += 8
if inv_sensori:   score += 4
if inv_drip:      score += 5
if inv_precision: score += 4
if inv_biochar:   score += 6
score = min(100, score)

if score >= 80:   rating,rcls = "A — Eccellente",  "A"
elif score >= 65: rating,rcls = "B — Conforme ESG","B"
elif score >= 48: rating,rcls = "C — Sviluppabile","C"
else:             rating,rcls = "D — Critico",     "D"

# Costo investimento tecnologico
tot_ha_int = int(tot_ha)
costo_inv  = (3500 if inv_sensori else 0) + (6000*tot_ha_int if inv_drip else 0) + \
             (8000 if inv_precision else 0) + (1200*tot_ha_int if inv_biochar else 0)
payback_inv= round(costo_inv / max(guadagno_tot,1), 1) if costo_inv > 0 else 0

# ══════════════════════════════════════════════════════════════
#  KPI PRINCIPALI
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📊 Indicatori Strategici</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5,k6,k7 = st.columns(7)

kpi_data = [
    (f"{score}/100", "Score ESG", f'<span style="background:{"#d1fae5" if rcls=="A" else "#dbeafe" if rcls=="B" else "#fef3c7" if rcls=="C" else "#fee2e2"};color:{"#065f46" if rcls=="A" else "#1e40af" if rcls=="B" else "#92400e" if rcls=="C" else "#991b1b"};padding:2px 10px;border-radius:20px;font-weight:700;font-size:.75rem">{rcls}</span>'),
    (f"{round(tot_seq,1)} t","CO₂ Sequestrata/anno",f"{round(tot_seq/max(tot_ha,1),2)} t/ha"),
    (f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t',"Bilancio Carbonico Netto","✅ Positive" if tot_netto>=0 else "⚠️ Emittente"),
    (f"€{int(valore_crediti):,}","Valore Crediti CO₂/anno",f"@ €{prezzo_co2}/t"),
    (f"{int(tot_fabb_irr):,} m³","Fabbisogno Idrico/anno",f"Spreco: {int(tot_spreco_h2o):,} m³"),
    (f"€{int(tot_valore_f):,}","Valore Fondo Stimato",f"{int(tot_ha)} ha capitalizzati"),
    (f"{margine_pct}%","Margine Netto",f"€{margine:,}/anno"),
]
for col, (v,l,s) in zip([k1,k2,k3,k4,k5,k6,k7], kpi_data):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s">{s}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  GRAFICI — riga 1
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📈 Analisi Multi-Dimensionale</div>', unsafe_allow_html=True)
g1,g2,g3 = st.columns(3)

GREEN = ["#061912","#0f3d22","#1a6b3a","#2d8a55","#52b788","#95d5b2","#d8f3dc"]

with g1:
    df_p = df_edit.copy()
    df_p["CO2"] = [r["co2_seq"] for r in res_att]
    df_p["Emissioni"] = [r["co2_emit"] for r in res_att]
    df_p["Netto"] = [r["co2_netto"] for r in res_att]
    fig = px.bar(df_p, x="Appezzamento", y=["CO2","Emissioni"],
                 barmode="group",
                 color_discrete_map={"CO2":"#1a6b3a","Emissioni":"#ef4444"},
                 title="CO₂ sequestrata vs emessa per campo")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#fafaf7",
                      font=dict(family="DM Sans",color="#061912"),
                      margin=dict(t=40,b=10,l=0,r=0),
                      legend=dict(orientation="h",y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

with g2:
    som_x = np.linspace(0.5, 5.0, 25)
    arg_y = np.linspace(5, 60, 25)
    z = np.array([[s * (1+a/100) * PROTOCOLLI["Rigenerativo Full"]["co2_coeff"] * 3.667
                   for s in som_x] for a in arg_y])
    fig_h = go.Figure(go.Heatmap(
        z=z, x=som_x, y=arg_y,
        colorscale=[[0,"#d8f3dc"],[0.5,"#1a6b3a"],[1,"#061912"]],
        colorbar=dict(title="tCO₂/ha")
    ))
    if len(df_edit) > 0:
        fig_h.add_trace(go.Scatter(
            x=df_edit["SO %"].tolist(), y=df_edit["Argilla %"].tolist(),
            mode="markers+text", marker=dict(color="#c9963a",size=13,symbol="x",line=dict(width=2)),
            text=df_edit["Appezzamento"].tolist(), textposition="top center", name="Campi"
        ))
    fig_h.update_layout(title="Potenziale sequestro — Argilla × SO%",
                        xaxis_title="Sostanza Organica %", yaxis_title="Argilla %",
                        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#fafaf7",
                        font=dict(family="DM Sans",color="#061912"),
                        margin=dict(t=40,b=40,l=40,r=20))
    st.plotly_chart(fig_h, use_container_width=True)

with g3:
    # Radar ESG completo
    cats = ["Carbonio","Acqua","Biodiversità","Certificazioni","Economia","Tecnologia"]
    carb_s = min(100, int(tot_netto/max(tot_ha,1)*30 + 50))
    acq_s  = max(0, 100 - int(tot_spreco_h2o/max(tot_fabb_irr+1,1)*100))
    bio_s  = int(cc_pct * 70 + 30)
    cert_s = min(100, (14*cert_bio+8*cert_sqnpi+7*cert_gap+8*cert_viva+10*cert_iso+8*cert_csrd))
    eco_s  = min(100, max(0, int(margine_pct * 3)))
    tec_s  = min(100, (inv_sensori*25 + inv_drip*30 + inv_precision*25 + inv_biochar*20))
    vals   = [carb_s, acq_s, bio_s, cert_s, eco_s, tec_s]

    fig_r = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself",
        line=dict(color="#1a6b3a",width=2.5),
        fillcolor="rgba(26,107,58,0.2)"
    ))
    fig_r.update_layout(
        polar=dict(radialaxis=dict(visible=True,range=[0,100],
                   tickfont=dict(size=9), gridcolor="rgba(15,61,34,.15)"),
                   angularaxis=dict(tickfont=dict(size=11))),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans",color="#061912"),
        title="Radar ESG Multidimensionale", margin=dict(t=50,b=10,l=10,r=10)
    )
    st.plotly_chart(fig_r, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  ACQUA — Analisi dettagliata
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">💧 Gestione Idrica Avanzata</div>', unsafe_allow_html=True)
wa1, wa2, wa3 = st.columns(3)

with wa1:
    df_w = df_edit.copy()
    df_w["Fabbisogno (m³)"] = [r["fabbisogno_irr"] for r in res_att]
    df_w["Irrigazione att."] = [r["irr_attuale"] for r in res_att]
    df_w["Capacità SOM extra"] = [r["capacita_extra"] for r in res_att]
    fig_w = px.bar(df_w, x="Appezzamento",
                   y=["Fabbisogno (m³)","Irrigazione att.","Capacità SOM extra"],
                   barmode="group", title="Bilancio idrico per campo (m³/anno)",
                   color_discrete_sequence=["#0a3d62","#3b82f6","#1a6b3a"])
    fig_w.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#fafaf7",
                        font=dict(family="DM Sans",color="#061912"),
                        margin=dict(t=40,b=10,l=0,r=0),
                        legend=dict(orientation="h",y=-0.25,font=dict(size=9)))
    st.plotly_chart(fig_w, use_container_width=True)

with wa2:
    mesi = ["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
    et0_mese  = [1.2,1.5,2.5,3.8,5.2,6.8,7.5,7.0,5.0,3.2,1.8,1.0]
    piog_mese = [55,50,60,58,52,30,18,22,50,70,80,65]
    kc_medio  = np.mean(list(COLTURE_KC.values()))
    etc_mese  = [e*kc_medio for e in et0_mese]
    deficit   = [max(0,e-p) for e,p in zip(etc_mese,piog_mese)]
    fig_mm = go.Figure()
    fig_mm.add_bar(x=mesi,y=piog_mese,name="Pioggia (mm)",marker_color="#3b82f6",opacity=0.7)
    fig_mm.add_scatter(x=mesi,y=etc_mese,name="ETc colture (mm)",
                       line=dict(color="#ef4444",width=2.5),mode="lines+markers")
    fig_mm.update_layout(title="Stagionalità idrica (profilo annuo)",
                         paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#fafaf7",
                         font=dict(family="DM Sans",color="#061912"),
                         legend=dict(orientation="h",y=-0.2),
                         margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig_mm, use_container_width=True)

with wa3:
    st.markdown(f"""
    <div style="background:#fff;border-radius:14px;padding:1.2rem 1.4rem;
         border:1px solid rgba(15,61,34,.1);height:100%">
      <div style="font-family:'DM Serif Display',serif;font-size:1rem;
           color:#061912;margin-bottom:.8rem">💧 Sintesi Idrica Aziendale</div>
      <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Fabbisogno stimato</td>
            <td style="text-align:right;font-weight:600">{int(tot_fabb_irr):,} m³/anno</td></tr>
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Irrigazione attuale</td>
            <td style="text-align:right;font-weight:600">{int(tot_irr_att):,} m³/anno</td></tr>
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Spreco stimato</td>
            <td style="text-align:right;font-weight:600;color:#ef4444">{int(tot_spreco_h2o):,} m³/anno</td></tr>
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Costo irrigazione</td>
            <td style="text-align:right;font-weight:600">€{int(tot_costo_irr):,}/anno</td></tr>
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Ritenzione SOM extra</td>
            <td style="text-align:right;font-weight:600;color:#1a6b3a">{int(tot_cap_extra):,} m³</td></tr>
        <tr style="border-bottom:1px solid #eee"><td style="padding:5px 0;color:#7a8c7e">Stress idrico attuale</td>
            <td style="text-align:right;font-weight:600;color:{'#ef4444' if stress_idrico>0.4 else '#c9963a' if stress_idrico>0.2 else '#1a6b3a'}">{round(stress_idrico*100)}%</td></tr>
        <tr><td style="padding:5px 0;color:#7a8c7e">Risparmio potenziale (rig.)</td>
            <td style="text-align:right;font-weight:600;color:#1a6b3a">€{int(risp_h2o_eur):,}/anno</td></tr>
      </table>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SCENARI — Business Case
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🚀 Scenari Economici & ROI Sostenibilità</div>', unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.markdown(f"""
    <div class="scenario-card s-base">
      <div style="font-weight:600;color:#1a6b3a;margin-bottom:.5rem">📍 Scenario Base — Stato Attuale</div>
      <div style="font-size:.82rem;line-height:1.8">
        CO₂ netta: <b>{round(tot_netto,1)} t/anno</b><br>
        Valore crediti: <b>€{int(valore_crediti):,}/anno</b><br>
        Costo gasolio: <b>€{int(tot_costo_die):,}/anno</b><br>
        Costo fertilizzanti N: <b>€{int(tot_costo_n):,}/anno</b><br>
        Costo irrigazione: <b>€{int(tot_costo_irr):,}/anno</b><br>
        Margine netto: <b>€{margine:,}/anno ({margine_pct}%)</b>
      </div>
    </div>""", unsafe_allow_html=True)

with sc2:
    st.markdown(f"""
    <div class="scenario-card s-opt">
      <div style="font-weight:600;color:#92400e;margin-bottom:.5rem">⚡ Scenario Ottimizzato — Rigenerativo Full</div>
      <div style="font-size:.82rem;line-height:1.8">
        CO₂ netta: <b>{round(pot_netto,1)} t/anno</b><br>
        Valore crediti: <b>€{int(pot_cred):,}/anno</b><br>
        Risparmio gasolio: <b>€{int(risp_diesel_eur):,}/anno</b><br>
        Risparmio acqua: <b>€{int(risp_h2o_eur):,}/anno</b><br>
        Nuovi crediti CO₂: <b>€{int(extra_cred_eur):,}/anno</b><br>
        <b style="color:#92400e;font-size:.9rem">Guadagno totale: +€{int(guadagno_tot):,}/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

with sc3:
    roi_txt = f"Payback: {payback_inv} anni" if costo_inv > 0 else "Nessun investimento selezionato"
    st.markdown(f"""
    <div class="scenario-card s-best">
      <div style="font-weight:600;color:#1e40af;margin-bottom:.5rem">🔬 Scenario Tech — Investimento Tecnologico</div>
      <div style="font-size:.82rem;line-height:1.8">
        Investimento totale: <b>€{int(costo_inv):,}</b><br>
        {'Sensori IoT suolo: €3.500<br>' if inv_sensori else ''}
        {'Drip irrigation: €'+str(6000*tot_ha_int)+'/ha<br>' if inv_drip else ''}
        {'Precision farming: €8.000<br>' if inv_precision else ''}
        {'Biochar: €'+str(1200*tot_ha_int)+'/ha<br>' if inv_biochar else ''}
        Ritorno stimato: <b>€{int(guadagno_tot):,}/anno</b><br>
        <b style="color:#1e40af;font-size:.9rem">{roi_txt}</b>
      </div>
    </div>""", unsafe_allow_html=True)

# ── Proiezione 5 anni ────────────────────────────────────────
anni = list(range(2026, 2032))
val_base = [max(0,tot_netto) * prezzo_co2 * (i+1) for i in range(6)]
val_pot  = [max(0,pot_netto) * prezzo_co2 * ((1+crescita_co2/100)**i) * (i+1) for i in range(6)]
val_tech = [max(0,pot_netto) * prezzo_co2 * ((1+crescita_co2/100)**i) * (i+1)
            + guadagno_tot*(i+1) - costo_inv for i in range(6)]

fig_proj = go.Figure()
fig_proj.add_scatter(x=anni, y=val_base, name="Base (attuale)",
                     line=dict(color="#94a3b8",width=2,dash="dot"), mode="lines+markers")
fig_proj.add_scatter(x=anni, y=val_pot,  name="Rigenerativo",
                     line=dict(color="#1a6b3a",width=3), mode="lines+markers",
                     fill="tonexty", fillcolor="rgba(26,107,58,0.06)")
fig_proj.add_scatter(x=anni, y=val_tech, name="Tech+Rigenerativo",
                     line=dict(color="#c9963a",width=3), mode="lines+markers",
                     fill="tonexty", fillcolor="rgba(201,150,58,0.06)")
fig_proj.update_layout(
    title="Capitalizzazione Crediti CO₂ — 3 Scenari (€ cumulati)",
    xaxis_title="Anno", yaxis_title="€ cumulati",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafaf7",
    font=dict(family="DM Sans",color="#061912"),
    legend=dict(orientation="h",y=-0.15),
    yaxis=dict(tickformat="€,.0f"),
    margin=dict(t=50,b=30,l=60,r=20)
)
st.plotly_chart(fig_proj, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  CERTIFICAZIONI — Gap Analysis
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📜 Gap Analysis Certificazioni</div>', unsafe_allow_html=True)
certs_info = [
    ("Biologico (Reg. UE 2018/848)", cert_bio,  14, "12-24 mesi conversione", "+15-25% prezzo vendita",   "Tutti i comparti"),
    ("SQnpi – Produzione Integrata",  cert_sqnpi, 8, "6-12 mesi",             "+8-15% accesso GDO",       "Cereali, orticole, frutteto"),
    ("GlobalG.A.P.",                  cert_gap,   7, "6 mesi",                "Accesso export e retail",   "Tutte le colture"),
    ("VIVA Sostenibilità",            cert_viva,  8, "12 mesi",               "+10% premio vitivinicolo",  "Solo vite"),
    ("ISO 14064-2 Carbon FP",         cert_iso,  10, "6-9 mesi",              "Crediti vendibili €42/t",  "Tutte le colture"),
    ("CSRD / ESRS reporting",         cert_csrd,  8, "12-18 mesi",            "Accesso catene >€40M",     "Aziende >10 ha"),
]
c_cols = st.columns(3)
for i,(nome,attiva,punti,tempo,valore,chi) in enumerate(certs_info):
    with c_cols[i%3]:
        bg  = "#f0fdf4" if attiva else "#fafaf7"
        brd = "#1a6b3a" if attiva else "rgba(15,61,34,.15)"
        ico = "✅" if attiva else "○"
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {brd};border-radius:11px;
             padding:.8rem 1rem;margin:.3rem 0">
          <div style="font-weight:600;font-size:.85rem">{ico} {nome}</div>
          <div style="font-size:.72rem;color:#7a8c7e;margin-top:3px">
            ESG: +{punti}pt &nbsp;|&nbsp; Tempo: {tempo}<br>
            💶 {valore}<br>
            👥 {chi}
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  AZIONI PRIORITARIE
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🎯 Piano d\'Azione Prioritario</div>', unsafe_allow_html=True)
azioni = []
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    azioni.append({"p":"alta","t":"Convertire appezzamenti convenzionali → Minima lavorazione",
        "i":f"IPCC FMG +0.18, +{round(tot_ha*0.025*3.667,1)} tCO₂/anno stimati",
        "e":f"€{round(tot_ha*0.025*3.667*prezzo_co2):,}/anno nuovi crediti",
        "c":"Prerequisito GlobalG.A.P. e ISO 14064"})
if tot_spreco_h2o > 500:
    azioni.append({"p":"alta","t":"Eliminare spreco idrico con drip irrigation",
        "i":f"Spreco attuale: {int(tot_spreco_h2o):,} m³/anno su {int(tot_ha)} ha",
        "e":f"€{int(tot_spreco_h2o*costo_acqua):,}/anno risparmio immediato",
        "c":"PAC Eco-Scheme misura irrigazione efficiente"})
if not cert_bio and not cert_sqnpi:
    azioni.append({"p":"alta","t":"Avviare certificazione SQnpi",
        "i":"Gateway per tutta la filiera GDO e export EU",
        "e":"Aumento prezzo vendita +12-18% stimato",
        "c":"Percorso 6-12 mesi — contatta CAA locale"})
if not cert_iso:
    azioni.append({"p":"media","t":"Certificazione ISO 14064 per crediti vendibili",
        "i":f"Bilancio netto attuale: {round(tot_netto,1)} tCO₂/anno",
        "e":f"€{round(max(0,tot_netto)*42):,}/anno su mercato ufficiale @ €42/t",
        "c":"Verra VCS o Gold Standard — verifica ente terzo"})
if not inv_sensori and tot_ha > 10:
    azioni.append({"p":"media","t":"Installare sensori IoT umidità suolo",
        "i":"Ottimizzazione irrigazione -25-35% consumi idrici",
        "e":f"ROI stimato in {round(3500/max(risp_h2o_eur+1,1),1)} anni",
        "c":"Integrazione con sistema previsione meteo Open-Meteo"})
if stress_idrico > 0.3:
    azioni.append({"p":"alta","t":"Gestione stress idrico — urgente",
        "i":f"Stress attuale {round(stress_idrico*100)}%, rischio resa -{round(stress_idrico*18,1)}%",
        "e":f"Perdita stimata: €{round(fatturato*stress_idrico*0.15):,} se non gestito",
        "c":"Irrigazione di soccorso + cover crops per ritenzione"})

p_map = {"alta":("act-h","🔴"),"media":("act-m","🟡"),"bassa":("act-l","🟢")}
for i,az in enumerate(azioni[:6],1):
    cls,ico = p_map[az["p"]]
    st.markdown(f"""
    <div class="action {cls}">
      <b>{ico} {i}. {az['t']}</b><br>
      <small style="color:#7a8c7e">📊 {az['i']}</small>&nbsp;&nbsp;
      <small style="color:#1a6b3a">💶 {az['e']}</small>&nbsp;&nbsp;
      <small style="color:#9ca3af">📜 {az['c']}</small>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  RISCHI
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">⚠️ Mappa dei Rischi</div>', unsafe_allow_html=True)
rischi = []
if stress_idrico > 0.4:
    rischi.append({"l":"alto","t":f"Stress idrico critico ({round(stress_idrico*100)}%) — rischio produttivo immediato"})
if tot_netto < 0:
    rischi.append({"l":"alto","t":"Bilancio carbonico negativo — azienda emittente netta"})
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    rischi.append({"l":"alto","t":"Gestione convenzionale: perdita SOM stimata >0.5% in 5 anni"})
if not any([cert_bio,cert_sqnpi,cert_gap]):
    rischi.append({"l":"medio","t":"Zero certificazioni: esclusione da filiere premium e crediti ufficiali"})
if margine_pct < 20:
    rischi.append({"l":"medio","t":f"Margine {margine_pct}% sotto soglia resilienza (25%)"})
rischi.append({"l":"medio","t":"CSRD 2026: filiere >€40M richiederanno rating ESG fornitori entro 2027"})
rischi.append({"l":"basso","t":"Volatilità mercato volontario CO₂: range €25-65/t nel 2026"})
rischi.append({"l":"basso","t":"Scenario RCP4.5: +1.2°C temperatura media entro 2035 — area mediterranea"})

rmap = {"alto":"r-alto","medio":"r-medio","basso":"r-basso"}
html_r = " ".join([f'<span class="risk {rmap[r["l"]]}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])
st.markdown(f'<div style="line-height:2.8">{html_r}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  METODOLOGIA
# ══════════════════════════════════════════════════════════════
with st.expander("🔬 Metodologia scientifica completa"):
    st.markdown("""
| Modulo | Formula / Standard |
|--------|-------------------|
| **Carbon — IPCC Tier 1** | `SOC × coeff_prot × f_tessitura × f_CC × f_clima × FMG × 3.667` |
| **SOC Stock** | `0.30m × 10.000m²/ha × Densità × (SO%/100) × 0.58` |
| **Fattore tessitura** | `1 + (Argilla%/100) + (Limo%/200)` — MAOC stabilizzazione minerale |
| **Cover crops FI** | `+15%` (IPCC 2006 Table 5.5 — Fi=1.15) |
| **FMG factor** | Conv=0.82 / Interm=1.00 / Rig=1.15 (IPCC Tier 1) |
| **Fattore clima** | Pianura=0.93 / Collina l.=0.97 / Collina i.=1.04 / Montagna=1.16 |
| **Emissioni N₂O** | `N × 0.01 × (44/28) × 265` (GWP AR5, EF IPCC) |
| **Emissioni gasolio** | `litri × 2.68 kgCO₂/L` (DEFRA 2024) |
| **Acqua — FAO PM** | `ET₀ (Open-Meteo live) × Kc coltura × area − pioggia efficace (×0.85)` |
| **Ritenzione SOM** | `(SO%-1.0) × 1.5mm/m × 3m profondità × area` (Rawls et al.) |
| **Stress idrico** | `deficit = ET₀_30g − pioggia_30g; stress = deficit/80mm` |
| **Valore fondiario** | `ha × 15.000€ × (1 + delta_SO% × 0.12)` (CREA-AA 2025) |
| **Prezzo CO₂** | Xpansiv CBL Voluntary Carbon Market Q1 2026 |
| **Benchmark** | CREA-AA Annuario 2025, RICA-Italia, ISPRA GHG 2024 |
| **Meteo live** | Open-Meteo API (ECMWF + DWD ICON, 1km risoluzione, no API key) |
    """)

# ══════════════════════════════════════════════════════════════
#  REPORT HTML
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📄 Genera Report Professionale</div>', unsafe_allow_html=True)

if st.button("📥 Genera Report HTML — Stampa come PDF (Ctrl+P)"):
    righe = ""
    for i,(_, row) in enumerate(df_edit.iterrows()):
        r = res_att[i]
        righe += f"""<tr>
          <td>{row.get('Appezzamento','')}</td><td>{row.get('Ettari','')}</td>
          <td>{row.get('Coltura','')}</td><td>{row.get('Protocollo','')}</td>
          <td>{row.get('SO %','')}%</td><td>{row.get('Argilla %','')}%</td>
          <td>{'✓' if row.get('Cover crops',False) else '—'}</td>
          <td><b>{r['co2_seq']}</b></td><td>{r['co2_emit']}</td>
          <td><b>{r['co2_netto']}</b></td><td>{int(r['fabbisogno_irr']):,}</td>
        </tr>"""

    cert_att = ", ".join([c for c,v in [("Bio",cert_bio),("SQnpi",cert_sqnpi),
        ("GlobalG.A.P.",cert_gap),("VIVA",cert_viva),("ISO 14064",cert_iso),
        ("CSRD",cert_csrd)] if v]) or "Nessuna"

    az_html = "".join([f"""
    <div style="border-left:4px solid {'#ef4444' if a['p']=='alta' else '#c9963a' if a['p']=='media' else '#1a6b3a'};
         padding:.5rem 1rem;margin:.35rem 0;background:#f9f9f7;border-radius:0 8px 8px 0">
      <b>{a['t']}</b><br>
      <small style="color:#555">📊 {a['i']}</small>&nbsp;
      <small style="color:#1a6b3a">💶 {a['e']}</small>
    </div>""" for a in azioni[:6]])

    html = f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<title>AgroLog IA — {nome_az}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',sans-serif;color:#1c1c1c;background:#fff;font-size:12.5px;}}
@media print{{.noprint{{display:none}};body{{font-size:11px}}}}
.hdr{{background:linear-gradient(135deg,#061912,#1a6b3a);color:#fff;padding:1.8rem 2.2rem}}
.hdr h1{{font-family:'DM Serif Display',serif;font-size:1.55rem;margin:.3rem 0}}
.hdr p{{color:rgba(255,255,255,.65);font-size:.82rem}}
.badge{{background:#c9963a;color:#061912;font-size:.62rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;padding:2px 10px;border-radius:20px}}
.sec{{padding:1rem 2rem;border-bottom:1px solid #e8e4dc}}
.st{{font-family:'DM Serif Display',serif;font-size:1.05rem;color:#061912;
  border-left:4px solid #1a6b3a;padding-left:.6rem;margin-bottom:.7rem}}
.kg{{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin:.5rem 0}}
.k{{background:#f5f2eb;border-radius:9px;padding:.7rem 1rem;text-align:center;
  border:1px solid rgba(15,61,34,.1)}}
.kv{{font-family:'DM Serif Display',serif;font-size:1.35rem;color:#0f3d22}}
.kl{{font-size:.62rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.06em}}
table{{width:100%;border-collapse:collapse;font-size:.78rem}}
th{{background:#0f3d22;color:#fff;padding:6px 8px;text-align:left;font-weight:500}}
td{{padding:5px 8px;border-bottom:1px solid #eee}}
tr:nth-child(even) td{{background:#f7f5f0}}
.ftr{{background:#061912;color:rgba(255,255,255,.5);padding:.8rem 2rem;
  font-size:.65rem;text-align:center}}
.sign{{border:1px solid #ddd;border-radius:10px;padding:1rem 1.5rem;margin:.5rem 0}}
.meteo{{background:linear-gradient(90deg,#0a3d62,#0f3d22);color:#fff;
  border-radius:10px;padding:.8rem 1.2rem;margin:.5rem 0;font-size:.82rem}}
</style></head><body>
<div class="hdr">
  <div class="badge">AgroLog IA — Carbon & ESG Strategic Intelligence 2026</div>
  <h1>{nome_az}</h1>
  <p>Consulente: {agronomo} &nbsp;·&nbsp; {regione} / {zona} &nbsp;·&nbsp; {datetime.now().strftime('%d/%m/%Y %H:%M')} &nbsp;·&nbsp; IPCC Tier 1 + FAO Water + Meteo Live</p>
</div>
<div class="sec"><div class="st">Indicatori Chiave</div>
<div class="kg">
  <div class="k"><div class="kv">{score}/100</div><div class="kl">Score ESG — {rcls}</div></div>
  <div class="k"><div class="kv">{round(tot_seq,1)} t</div><div class="kl">CO₂ Sequestrata/anno</div></div>
  <div class="k"><div class="kv">€{int(valore_crediti):,}</div><div class="kl">Valore Crediti CO₂</div></div>
  <div class="k"><div class="kv">{round(tot_netto,1)} t</div><div class="kl">Bilancio Carbonico Netto</div></div>
  <div class="k"><div class="kv">{int(tot_fabb_irr):,} m³</div><div class="kl">Fabbisogno Idrico/anno</div></div>
  <div class="k"><div class="kv">€{int(tot_valore_f):,}</div><div class="kl">Valore Fondo Stimato</div></div>
  <div class="k"><div class="kv">{margine_pct}%</div><div class="kl">Margine Netto</div></div>
  <div class="k"><div class="kv">{round(stress_idrico*100):.0f}%</div><div class="kl">Stress Idrico Attuale</div></div>
</div></div>
<div class="sec"><div class="st">Condizioni Meteo — {regione} (Open-Meteo live)</div>
<div class="meteo">
  🌡️ Temp. 7gg: {meteo['temp_max']}°/{meteo['temp_min']}°C &nbsp;|&nbsp;
  🌧️ Pioggia 7gg: {meteo['pioggia_7g']} mm &nbsp;|&nbsp;
  💧 ET₀: {meteo['et0_media']} mm/g &nbsp;|&nbsp;
  📊 Pioggia 30gg: {meteo['precipitazioni_30g']} mm &nbsp;|&nbsp;
  ⚡ Deficit idrico: {round(deficit_idrico,0)} mm &nbsp;|&nbsp;
  🔥 Stress: {round(stress_idrico*100):.0f}%
</div></div>
<div class="sec"><div class="st">Dettaglio Appezzamenti</div>
<table><thead><tr><th>Campo</th><th>ha</th><th>Coltura</th><th>Protocollo</th><th>SO%</th>
<th>Arg%</th><th>CC</th><th>CO₂ Seq (t)</th><th>CO₂ Emit (t)</th>
<th>Netto (t)</th><th>Fabb.Irr (m³)</th></tr></thead><tbody>{righe}</tbody></table></div>
<div class="sec"><div class="st">Scenari Economici</div>
<table><thead><tr><th>Voce</th><th>Scenario Base</th><th>Rigenerativo</th><th>Delta</th></tr></thead>
<tbody>
<tr><td>CO₂ netta (t/anno)</td><td>{round(tot_netto,1)}</td><td>{round(pot_netto,1)}</td>
    <td style="color:#1a6b3a">+{round(pot_netto-tot_netto,1)}</td></tr>
<tr><td>Valore crediti CO₂</td><td>€{int(valore_crediti):,}</td><td>€{int(pot_cred):,}</td>
    <td style="color:#1a6b3a">+€{int(extra_cred_eur):,}</td></tr>
<tr><td>Risparmio gasolio</td><td>—</td><td>€{int(risp_diesel_eur):,}</td>
    <td style="color:#1a6b3a">+€{int(risp_diesel_eur):,}</td></tr>
<tr><td>Risparmio acqua</td><td>—</td><td>€{int(risp_h2o_eur):,}</td>
    <td style="color:#1a6b3a">+€{int(risp_h2o_eur):,}</td></tr>
<tr style="background:#f0fdf4"><td><b>Guadagno totale annuo</b></td><td>—</td>
    <td colspan="2"><b style="color:#1a6b3a">+€{int(guadagno_tot):,}/anno</b></td></tr>
</tbody></table></div>
<div class="sec"><div class="st">Piano Azioni Prioritarie</div>{az_html}</div>
<div class="sec"><div class="st">Certificazioni</div>
<p style="font-size:.82rem;color:#555">Attive: <b>{cert_att}</b></p></div>
<div class="sec"><div class="st">Nota Metodologica</div>
<p style="font-size:.78rem;color:#555;line-height:1.6">
Calcoli carbonio: <b>IPCC 2006 Guidelines Vol.4 Tier 1, AR5 GWP</b>. Acqua: <b>FAO Penman-Monteith</b>,
Kc colturali FAO-56. Meteo live: <b>Open-Meteo API</b> (ECMWF + DWD ICON, risoluzione 1km).
Stress idrico: deficit ET₀−pioggia 30gg (soglia critica 80mm). Valore fondiario: <b>CREA-AA 2025</b>.
Prezzi CO₂: Xpansiv CBL Voluntary Carbon Market Q1 2026. Report previsionale — certificazione ufficiale
richiede verifica Ente Terzo accreditato (Verra, Gold Standard, ISAE 3000).
</p></div>
<div class="sec"><div class="st">Firma e Validazione</div>
<div class="sign">
  <p><b>Dottore Agronomo:</b> {agronomo} &nbsp;&nbsp; <b>Albo:</b> ______________________</p>
  <p style="margin-top:.4rem"><b>Data:</b> {datetime.now().strftime('%d/%m/%Y')} &nbsp;&nbsp;
     <b>Luogo:</b> ______________________</p>
  <p style="margin-top:1.5rem;color:#bbb">Firma: ______________________ &nbsp;&nbsp; Timbro:</p>
</div></div>
<div class="ftr">AgroLog IA v4.0 — Carbon & ESG Strategic Intelligence | IPCC 2006 Tier 1 · FAO-PM Water · Open-Meteo Live · CREA-AA 2025 | Report previsionale</div>
</body></html>"""

    b64 = base64.b64encode(html.encode("utf-8")).decode()
    fn  = f"AgroLog_{nome_az.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html"
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="{fn}" '
        f'style="display:inline-block;background:#0f3d22;color:#fff;padding:.6rem 1.5rem;'
        f'border-radius:8px;text-decoration:none;font-weight:600">⬇️ Scarica Report HTML</a>',
        unsafe_allow_html=True)
    st.success("✅ Apri il file nel browser → Ctrl+P → Salva come PDF → consegna al cliente.")

st.markdown("""
<div class="footer">
  AgroLog IA v4.0 — Carbon & ESG Strategic Intelligence |
  IPCC 2006 Tier 1 · FAO Penman-Monteith · Open-Meteo Live (ECMWF+DWD) ·
  CREA-AA 2025 · ISPRA GHG 2024 · Xpansiv CBL Q1 2026 |
  Dati previsionali — verifica Ente Terzo per certificazione ufficiale
</div>""", unsafe_allow_html=True)
