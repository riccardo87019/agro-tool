import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests, base64

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgroLog IA | Carbon & ESG Intelligence",
    page_icon="🌿", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
html,body,[class*="css"]{font-family:'Lexend',sans-serif;}
.stApp{background:#f4f1ea;}

.hero{background:linear-gradient(135deg,#061912 0%,#0f3520 40%,#1a6b3a 100%);
  padding:2.5rem 3rem;border-radius:22px;margin-bottom:2rem;
  box-shadow:0 12px 40px rgba(6,25,18,.22);border-bottom:4px solid #c9963a;}
.hero h1{font-family:'DM Serif Display',serif;color:#fff;font-size:2.1rem;margin:.3rem 0 .1rem;}
.hero p{color:rgba(255,255,255,.62);font-size:.88rem;margin:0;}
.hero-badge{background:#c9963a;color:#061912;font-size:.62rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;
  border-radius:20px;margin-bottom:.6rem;display:inline-block;}

.kpi{background:#fff;border-radius:18px;padding:1.3rem 1.1rem;
  border:1px solid rgba(15,53,32,.1);box-shadow:0 4px 14px rgba(6,25,18,.06);
  text-align:center;transition:transform .25s;}
.kpi:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(6,25,18,.1);}
.kpi-v{font-size:1.85rem;font-weight:700;color:#0f3520;line-height:1.1;}
.kpi-l{font-size:.62rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.09em;margin-top:.3rem;}
.kpi-s{font-size:.78rem;color:#1a6b3a;font-weight:600;margin-top:.15rem;}

.sec{font-family:'DM Serif Display',serif;font-size:1.25rem;color:#061912;
  border-left:5px solid #c9963a;padding-left:.75rem;margin:2.2rem 0 1rem;}

.action{background:#fff;border-radius:13px;padding:.9rem 1.15rem;margin:.4rem 0;
  border:1px solid rgba(15,53,32,.1);transition:box-shadow .2s;}
.action:hover{box-shadow:0 4px 14px rgba(6,25,18,.08);}
.act-h{border-left:4px solid #ef4444;}
.act-m{border-left:4px solid #c9963a;}
.act-l{border-left:4px solid #1a6b3a;}

.risk{display:inline-block;padding:3px 11px;border-radius:20px;
  font-size:.7rem;font-weight:600;margin:2px;}
.r-alto{background:#fee2e2;color:#991b1b;}
.r-medio{background:#fef3c7;color:#92400e;}
.r-basso{background:#d1fae5;color:#065f46;}

.cert-box{border-radius:11px;padding:.8rem 1rem;margin:.3rem 0;
  border:1px solid rgba(15,53,32,.12);}
.cert-on{background:#f0fdf4;border-color:#1a6b3a;}
.cert-off{background:#fafaf9;}

.sc-card{border-radius:14px;padding:1.2rem 1.4rem;margin:.4rem 0;}
.sc-base{background:#f0fdf4;border:2px dashed #1a6b3a;}
.sc-opt{background:#fffbeb;border:2px dashed #c9963a;}
.sc-tech{background:#eff6ff;border:2px dashed #3b82f6;}

div[data-testid="stSidebar"]{background:#061912;}
div[data-testid="stSidebar"] *{color:rgba(255,255,255,.85)!important;}
div[data-testid="stSidebar"] h2,div[data-testid="stSidebar"] h3{
  font-family:'DM Serif Display',serif!important;color:#fff!important;}
div[data-testid="stSidebar"] label{
  font-size:.72rem!important;text-transform:uppercase;
  letter-spacing:.05em;color:rgba(255,255,255,.5)!important;}

.stButton>button{background:#0f3520!important;color:#fff!important;
  border:none!important;border-radius:10px!important;
  font-weight:600!important;font-size:.92rem!important;
  padding:.65rem 1.8rem!important;}
.stButton>button:hover{background:#061912!important;}

.report-btn>button{background:#c9963a!important;}

.footer{font-size:.67rem;color:#9aab9e;text-align:center;margin-top:2.5rem;
  padding-top:1rem;border-top:1px solid rgba(15,53,32,.12);}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COSTANTI
# ══════════════════════════════════════════════════════════════
COORDS = {
    "Marche":(43.62,13.51),"Toscana":(43.46,11.10),"Emilia-Romagna":(44.50,11.34),
    "Veneto":(45.44,11.88),"Lombardia":(45.46,9.19),"Piemonte":(45.07,7.68),
    "Puglia":(41.12,16.87),"Sicilia":(37.60,14.02),"Campania":(40.83,14.25),
    "Lazio":(41.90,12.49),"Umbria":(43.11,12.39),"Abruzzo":(42.35,13.39),
    "Calabria":(38.90,16.59),"Sardegna":(40.12,9.01),"Altra":(42.50,12.50),
}
SOC_REF  = {"Pianura":47.8,"Collina litoranea":39.3,"Collina interna":37.1,"Montagna":31.5}
F_CLIMA  = {"Pianura":0.93,"Collina litoranea":0.97,"Collina interna":1.04,"Montagna":1.16}
PROT = {
    "Convenzionale":    {"fmg":0.82,"diesel":155,"n_ha":115,"co2c":0.005},
    "Intermedio":       {"fmg":1.00,"diesel": 82,"n_ha": 72,"co2c":0.022},
    "Rigenerativo Full":{"fmg":1.15,"diesel": 40,"n_ha": 32,"co2c":0.055},
}
KC = {"Cereali":1.15,"Vite (DOC/IGT)":0.70,"Olivo":0.65,"Nocciolo":0.80,
      "Frutteto":1.10,"Orticole":1.20,"Foraggere":1.00,"Misto":0.90}

# ══════════════════════════════════════════════════════════════
#  DATI DEFAULT
# ══════════════════════════════════════════════════════════════
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Campo":"Nord A1","Ettari":14.0,"SO %":1.6,"Argilla %":26,"Limo %":30,
         "Densità":1.32,"Protocollo":"Convenzionale","Cover crops":False,
         "Coltura":"Cereali","Irrigazione m³/ha":750},
        {"Campo":"Vigneto Est","Ettari":7.0,"SO %":1.3,"Argilla %":17,"Limo %":42,
         "Densità":1.44,"Protocollo":"Intermedio","Cover crops":False,
         "Coltura":"Vite (DOC/IGT)","Irrigazione m³/ha":280},
        {"Campo":"Oliveto Sud","Ettari":5.0,"SO %":2.2,"Argilla %":23,"Limo %":36,
         "Densità":1.24,"Protocollo":"Rigenerativo Full","Cover crops":True,
         "Coltura":"Olivo","Irrigazione m³/ha":0},
    ])

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌿 AgroLog IA")
    st.caption("Carbon & ESG Strategic Intelligence")
    st.markdown("---")
    st.markdown("### Azienda")
    nome_az   = st.text_input("Ragione Sociale", "Az. Agr. Rossi")
    agronomo  = st.text_input("Dottore Agronomo", "Dott. [Cognome]")
    regione   = st.selectbox("Regione", list(COORDS.keys()))
    zona      = st.selectbox("Zona Altimetrica", list(SOC_REF.keys()))
    tel       = st.text_input("Telefono / Email", "")

    st.markdown("---")
    st.markdown("### Certificazioni")
    cert_bio  = st.checkbox("Biologico (Reg. UE 2018/848)")
    cert_sqnpi= st.checkbox("SQnpi")
    cert_gap  = st.checkbox("GlobalG.A.P.")
    cert_viva = st.checkbox("VIVA Sostenibilità")
    cert_iso  = st.checkbox("ISO 14064")
    cert_csrd = st.checkbox("CSRD / ESRS")

    st.markdown("---")
    st.markdown("### Mercato & Finanza")
    prezzo_co2   = st.number_input("Prezzo CO₂ (€/t)", 10.0, 200.0, 42.0, 1.0)
    crescita_co2 = st.slider("Crescita prezzo CO₂/anno (%)", 0, 20, 7)
    costo_diesel = st.number_input("Gasolio (€/L)", 0.7, 2.5, 1.18, 0.05)
    costo_acqua  = st.number_input("Irrigazione (€/m³)", 0.1, 2.0, 0.48, 0.05)
    fatturato    = st.number_input("Fatturato (€/anno)", 0, 5000000, 220000, 5000)
    costi_var    = st.number_input("Costi variabili (€/anno)", 0, 5000000, 115000, 5000)

    st.markdown("---")
    st.markdown("### Tecnologia")
    inv_iot      = st.checkbox("Sensori IoT suolo (€3.500)")
    inv_drip     = st.checkbox("Micro-irrigazione (€6.000/ha)")
    inv_gps      = st.checkbox("Precision farming GPS (€8.000)")
    inv_biochar  = st.checkbox("Biochar (€1.200/ha)")

# ══════════════════════════════════════════════════════════════
#  METEO LIVE — Open-Meteo (gratis, no API key)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_meteo_live(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
               f"et0_fao_evapotranspiration,wind_speed_10m_max"
               f"&timezone=Europe/Rome&forecast_days=7")
        d = requests.get(url, timeout=7).json().get("daily", {})
        return {
            "tmax": round(np.mean([x for x in d.get("temperature_2m_max",[22]) if x]),1),
            "tmin": round(np.mean([x for x in d.get("temperature_2m_min",[10]) if x]),1),
            "pioggia_7g": round(sum([x for x in d.get("precipitation_sum",[0]*7) if x]),1),
            "et0": round(np.mean([x for x in d.get("et0_fao_evapotranspiration",[3.5]) if x]),2),
            "vento": round(max([x for x in d.get("wind_speed_10m_max",[20]) if x]),1),
        }
    except:
        return {"tmax":22,"tmin":10,"pioggia_7g":12,"et0":3.8,"vento":22}

@st.cache_data(ttl=86400)
def get_meteo_storico(lat, lon):
    try:
        from datetime import date, timedelta
        e = date.today().strftime("%Y-%m-%d")
        s = (date.today()-timedelta(days=30)).strftime("%Y-%m-%d")
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
               f"&start_date={s}&end_date={e}"
               f"&daily=precipitation_sum,et0_fao_evapotranspiration,temperature_2m_mean"
               f"&timezone=Europe/Rome")
        d = requests.get(url, timeout=10).json().get("daily", {})
        p = [x for x in d.get("precipitation_sum",[]) if x is not None]
        e2= [x for x in d.get("et0_fao_evapotranspiration",[]) if x is not None]
        t = [x for x in d.get("temperature_2m_mean",[]) if x is not None]
        return {
            "pioggia_30g": round(sum(p),1) if p else 42,
            "et0_30g":     round(sum(e2),1) if e2 else 88,
            "temp_30g":    round(np.mean(t),1) if t else 15,
        }
    except:
        return {"pioggia_30g":42,"et0_30g":88,"temp_30g":15}

lat, lon = COORDS.get(regione, (42.5,12.5))
M  = get_meteo_live(lat, lon)
MS = get_meteo_storico(lat, lon)
deficit_idrico = max(0, MS["et0_30g"] - MS["pioggia_30g"])
stress_idx     = min(1.0, deficit_idrico / 80)

# ══════════════════════════════════════════════════════════════
#  MOTORE SCIENTIFICO
# ══════════════════════════════════════════════════════════════
def calcola(row, boost=False):
    prot = "Rigenerativo Full" if boost else str(row.get("Protocollo","Intermedio"))
    p    = PROT.get(prot, PROT["Intermedio"])
    ha   = float(row.get("Ettari",1))
    so   = float(row.get("SO %",1.5))
    arg  = float(row.get("Argilla %",20))
    lim  = float(row.get("Limo %",30))
    den  = float(row.get("Densità",1.3))
    cc   = row.get("Cover crops", False) or boost
    col  = str(row.get("Coltura","Cereali"))
    irr  = float(row.get("Irrigazione m³/ha",0))

    # --- CARBON (IPCC Tier 1) ---
    massa   = 0.30 * 10000 * den
    soc     = massa * (so/100) * 0.58
    f_text  = 1 + (arg/100) + (lim/200)
    f_cc    = 1.15 if cc else 1.0
    f_clim  = F_CLIMA.get(zona, 1.0)
    seq_ha  = soc * p["co2c"] * f_text * f_cc * f_clim * p["fmg"]
    co2_seq = seq_ha * 3.667 * ha

    n_kg    = p["n_ha"] * ha
    n2o     = n_kg * 0.01 * (44/28) * 265 / 1000
    diesel  = p["diesel"] * ha
    die_co2 = diesel * 2.68 / 1000
    co2_emit= n2o + die_co2

    # --- ACQUA (FAO PM) ---
    kc        = KC.get(col, 1.0)
    et0_ann   = M["et0"] * 365
    etc_ann   = et0_ann * kc
    pioggia_e = MS["pioggia_30g"] * 12 * 0.85
    fabb_irr  = max(0, etc_ann - pioggia_e) * 10 * ha
    irr_tot   = irr * ha
    spreco    = max(0, irr_tot - fabb_irr)
    ret_h2o   = (so - 1.0) * 1.5 * 3 * 10 * ha

    # --- COSTI ---
    c_diesel  = diesel * costo_diesel
    c_n       = n_kg * 0.85
    c_irr     = irr_tot * costo_acqua
    valore_f  = ha * (15000 + (so/1.2 - 1) * 0.12 * 15000)

    return {
        "co2_seq":    round(co2_seq,3),
        "co2_emit":   round(co2_emit,3),
        "co2_netto":  round(co2_seq-co2_emit,3),
        "n2o":        round(n2o,3),
        "diesel_co2": round(die_co2,3),
        "diesel_l":   round(diesel,0),
        "fabb_irr":   round(fabb_irr,0),
        "irr_tot":    round(irr_tot,0),
        "spreco":     round(spreco,0),
        "ret_h2o":    round(ret_h2o,0),
        "c_diesel":   round(c_diesel,0),
        "c_n":        round(c_n,0),
        "c_irr":      round(c_irr,0),
        "valore_f":   round(valore_f,0),
        "seq_ha":     round(seq_ha*3.667,3),
    }

# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">AgroLog IA · Platform Pro 2026 · IPCC·FAO·Meteo Live</div>
  <h1>🌿 {nome_az}</h1>
  <p>Consulente: {agronomo} · {regione} / {zona} · {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  METEO LIVE BANNER
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🌦️ Meteo & Stress Idrico Live</div>', unsafe_allow_html=True)
w1,w2,w3,w4,w5,w6 = st.columns(6)
wdata = [
    (f"{M['tmax']}° / {M['tmin']}°C","Temp. 7gg","Min/Max"),
    (f"{M['pioggia_7g']} mm","Pioggia prevista","prossimi 7 giorni"),
    (f"{M['et0']} mm/g","ET₀ FAO","evapotraspirazione"),
    (f"{MS['pioggia_30g']} mm","Pioggia storica","ultimi 30 giorni"),
    (f"{MS['et0_30g']} mm","ET₀ storica","ultimi 30 giorni"),
    (f"{round(stress_idx*100):.0f}%","Stress Idrico","indice corrente"),
]
stress_col = "#991b1b" if stress_idx>.5 else "#92400e" if stress_idx>.25 else "#1a6b3a"
for col,(v,l,s),clr in zip([w1,w2,w3,w4,w5,w6],wdata,
    ["#0f3520","#0f3520","#0f3520","#0f3520","#0f3520",stress_col]):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v" style="font-size:1.3rem;color:{clr}">{v}</div>'
                    f'<div class="kpi-l">{l}</div><div class="kpi-s" style="color:#9aab9e">{s}</div></div>',
                    unsafe_allow_html=True)

if stress_idx > .4:
    st.warning(f"⚠️ **Stress idrico critico {round(stress_idx*100)}%** — deficit {round(deficit_idrico)} mm. Rischio resa -{round(stress_idx*18,1)}%.")
elif stress_idx > .2:
    st.info(f"ℹ️ Stress idrico moderato {round(stress_idx*100)}% — monitorare nelle prossime 2 settimane.")
else:
    st.success("✅ Bilancio idrico equilibrato — condizioni favorevoli.")

# ══════════════════════════════════════════════════════════════
#  TABELLA APPEZZAMENTI
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📑 Inventario Fondiario</div>', unsafe_allow_html=True)
st.caption("Inserisci i dati reali dell'azienda — il report si aggiorna in tempo reale.")

df_edit = st.data_editor(
    st.session_state.df_campi, num_rows="dynamic", use_container_width=True,
    column_config={
        "Protocollo": st.column_config.SelectboxColumn(
            options=["Convenzionale","Intermedio","Rigenerativo Full"], required=True),
        "Cover crops":        st.column_config.CheckboxColumn(),
        "Coltura":            st.column_config.SelectboxColumn(options=list(KC.keys()), required=True),
        "Ettari":             st.column_config.NumberColumn(min_value=0.1, max_value=5000, format="%.1f"),
        "SO %":               st.column_config.NumberColumn(min_value=0.1, max_value=8.0,  format="%.2f"),
        "Argilla %":          st.column_config.NumberColumn(min_value=1,   max_value=80),
        "Limo %":             st.column_config.NumberColumn(min_value=1,   max_value=80),
        "Densità":            st.column_config.NumberColumn(min_value=0.7, max_value=1.9,  format="%.2f"),
        "Irrigazione m³/ha":  st.column_config.NumberColumn(min_value=0,   max_value=10000),
    }, key="editor_v5"
)
st.session_state.df_campi = df_edit

# ══════════════════════════════════════════════════════════════
#  CALCOLI
# ══════════════════════════════════════════════════════════════
if len(df_edit) == 0:
    st.warning("Aggiungi almeno un appezzamento nella tabella sopra.")
    st.stop()

res_att = [calcola(r, False) for _, r in df_edit.iterrows()]
res_pot = [calcola(r, True)  for _, r in df_edit.iterrows()]

tot_ha       = float(df_edit["Ettari"].sum())
tot_seq      = sum(r["co2_seq"]  for r in res_att)
tot_emit     = sum(r["co2_emit"] for r in res_att)
tot_netto    = tot_seq - tot_emit
tot_diesel_l = sum(r["diesel_l"] for r in res_att)
tot_irr      = sum(r["irr_tot"]  for r in res_att)
tot_fabb     = sum(r["fabb_irr"] for r in res_att)
tot_spreco   = sum(r["spreco"]   for r in res_att)
tot_ret_h2o  = sum(r["ret_h2o"]  for r in res_att)
tot_c_diesel = sum(r["c_diesel"] for r in res_att)
tot_c_n      = sum(r["c_n"]      for r in res_att)
tot_c_irr    = sum(r["c_irr"]    for r in res_att)
tot_valore_f = sum(r["valore_f"] for r in res_att)
val_crediti  = max(0, tot_netto) * prezzo_co2
margine      = fatturato - costi_var
marg_pct     = round(margine/fatturato*100,1) if fatturato>0 else 0

pot_netto    = sum(r["co2_netto"] for r in res_pot)
pot_diesel_l = sum(r["diesel_l"]  for r in res_pot)
pot_cred     = max(0, pot_netto) * prezzo_co2
risp_die_eur = (tot_diesel_l - pot_diesel_l) * costo_diesel
risp_h2o_eur = sum(r["spreco"] for r in res_pot) * 0  # già ottimizzato
risp_h2o_eur = tot_spreco * costo_acqua
extra_cred   = pot_cred - val_crediti
guadagno     = risp_die_eur + risp_h2o_eur + extra_cred

tot_ha_i = max(1, int(tot_ha))
costo_inv = ((3500 if inv_iot else 0) + (6000*tot_ha_i if inv_drip else 0) +
             (8000 if inv_gps else 0) + (1200*tot_ha_i if inv_biochar else 0))
payback   = round(costo_inv/max(guadagno,1),1) if costo_inv>0 else 0

# Score ESG
score = 28
score += min(25, int(max(0, tot_netto/max(tot_ha,1)) * 12))
if cert_bio:   score += 14
if cert_sqnpi: score += 8
if cert_gap:   score += 7
if cert_viva:  score += 8
if cert_iso:   score += 10
if cert_csrd:  score += 8
cc_r = sum(1 for _,r in df_edit.iterrows() if r.get("Cover crops",False))/max(len(df_edit),1)
score += int(cc_r*12)
if tot_spreco < tot_fabb*0.1: score += 7
if inv_iot:    score += 4
if inv_drip:   score += 5
if inv_gps:    score += 4
if inv_biochar:score += 6
score = min(100, score)

if score>=80:   rating,rcls,rcol = "A — Eccellente",  "A","#065f46"
elif score>=65: rating,rcls,rcol = "B — Conforme ESG","B","#1e40af"
elif score>=48: rating,rcls,rcol = "C — Sviluppabile","C","#92400e"
else:           rating,rcls,rcol = "D — Critico",     "D","#991b1b"

rbg = {"A":"#d1fae5","B":"#dbeafe","C":"#fef3c7","D":"#fee2e2"}[rcls]

# ══════════════════════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📊 Indicatori Strategici</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5,k6,k7 = st.columns(7)
kpis = [
    (f"{score}/100","Score ESG",f'<span style="background:{rbg};color:{rcol};padding:2px 10px;border-radius:20px;font-weight:700;font-size:.72rem">{rcls}</span>'),
    (f"{round(tot_seq,1)} t","CO₂ Sequestrata/anno",f"{round(tot_seq/max(tot_ha,1),2)} t/ha"),
    (f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t',"Bilancio Carbonico","✅ Carbon +" if tot_netto>=0 else "⚠️ Emittente"),
    (f"€{int(val_crediti):,}","Valore Crediti CO₂",f"@ €{prezzo_co2}/tCO₂"),
    (f"{int(tot_fabb):,} m³","Fabbisogno Idrico",f"Spreco {int(tot_spreco):,} m³"),
    (f"€{int(tot_valore_f):,}","Valore Fondo Stimato",f"{int(tot_ha)} ha · CREA-AA"),
    (f"{marg_pct}%","Margine Netto",f"€{margine:,}/anno"),
]
for col,(v,l,s) in zip([k1,k2,k3,k4,k5,k6,k7], kpis):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s">{s}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  GRAFICI
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📈 Analisi Visiva Multi-Dimensionale</div>', unsafe_allow_html=True)
g1,g2,g3 = st.columns(3)
PLT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
           font=dict(family="Lexend", color="#061912"),
           margin=dict(t=44,b=24,l=24,r=12))

with g1:
    df_p = df_edit.copy()
    df_p["Seq"] = [r["co2_seq"]  for r in res_att]
    df_p["Emit"]= [r["co2_emit"] for r in res_att]
    fig = go.Figure()
    fig.add_bar(x=df_p["Campo"],y=df_p["Seq"], name="Seq CO₂",marker_color="#1a6b3a")
    fig.add_bar(x=df_p["Campo"],y=df_p["Emit"],name="Emissioni",marker_color="#ef4444")
    fig.update_layout(**PLT, title="CO₂ per campo (t/anno)", barmode="group",
                      legend=dict(orientation="h",y=-0.25,font=dict(size=10)))
    st.plotly_chart(fig, use_container_width=True)

with g2:
    cats = ["Carbonio","Acqua","Biodiversità","Certificazioni","Economia","Tecnologia"]
    c_s = min(100,int(tot_netto/max(tot_ha,1)*12+50))
    a_s = max(0,100-int(tot_spreco/max(tot_fabb+1,1)*100))
    b_s = int(cc_r*70+30)
    ce_s= min(100,(14*cert_bio+8*cert_sqnpi+7*cert_gap+8*cert_viva+10*cert_iso+8*cert_csrd))
    e_s = min(100,max(0,int(marg_pct*3)))
    t_s = min(100,(inv_iot*25+inv_drip*30+inv_gps*25+inv_biochar*20))
    vals= [c_s,a_s,b_s,ce_s,e_s,t_s]
    fig_r = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself",
        line=dict(color="#1a6b3a",width=2.5),
        fillcolor="rgba(26,107,58,0.18)"
    ))
    fig_r.update_layout(**PLT, title="Radar ESG 6 Dimensioni",
        polar=dict(radialaxis=dict(visible=True,range=[0,100],
                   tickfont=dict(size=9),gridcolor="rgba(15,53,32,.12)"),
                   angularaxis=dict(tickfont=dict(size=10))),
        margin=dict(t=50,b=10,l=10,r=10))
    st.plotly_chart(fig_r, use_container_width=True)

with g3:
    anni = list(range(2026,2032))
    v_base = [max(0,tot_netto)*prezzo_co2*(i+1) for i in range(6)]
    v_pot  = [max(0,pot_netto)*prezzo_co2*((1+crescita_co2/100)**i)*(i+1) for i in range(6)]
    v_tech = [max(0,pot_netto)*prezzo_co2*((1+crescita_co2/100)**i)*(i+1)+guadagno*(i+1)-costo_inv for i in range(6)]
    fig_p = go.Figure()
    fig_p.add_scatter(x=anni,y=v_base,name="Base",line=dict(color="#94a3b8",width=2,dash="dot"),mode="lines+markers")
    fig_p.add_scatter(x=anni,y=v_pot, name="Rigenerativo",line=dict(color="#1a6b3a",width=3),mode="lines+markers",
                      fill="tonexty",fillcolor="rgba(26,107,58,0.07)")
    fig_p.add_scatter(x=anni,y=v_tech,name="Tech+Rigenerat.",line=dict(color="#c9963a",width=3),mode="lines+markers",
                      fill="tonexty",fillcolor="rgba(201,150,58,0.07)")
    fig_p.update_layout(**PLT,title="Capitalizzazione CO₂ — 3 scenari",
                        yaxis=dict(tickformat="€,.0f"),
                        legend=dict(orientation="h",y=-0.25,font=dict(size=10)))
    st.plotly_chart(fig_p, use_container_width=True)

# Heatmap + Bilancio idrico
g4,g5 = st.columns(2)
with g4:
    som_x = np.linspace(0.5,5,22); arg_y = np.linspace(5,60,22)
    z = np.array([[s*(1+a/100)*PROT["Rigenerativo Full"]["co2c"]*3.667 for s in som_x] for a in arg_y])
    fig_h = go.Figure(go.Heatmap(z=z,x=som_x,y=arg_y,
        colorscale=[[0,"#d8f3dc"],[0.5,"#1a6b3a"],[1,"#061912"]],
        colorbar=dict(title="tCO₂/ha")))
    if len(df_edit)>0:
        fig_h.add_trace(go.Scatter(x=df_edit["SO %"].tolist(),y=df_edit["Argilla %"].tolist(),
            mode="markers+text",marker=dict(color="#c9963a",size=13,symbol="x",line=dict(width=2)),
            text=df_edit["Campo"].tolist(),textposition="top center",name="Campi"))
    fig_h.update_layout(**PLT,title="Potenziale sequestro — Argilla × SO%",
        xaxis_title="SO%",yaxis_title="Argilla%")
    st.plotly_chart(fig_h, use_container_width=True)

with g5:
    df_w = df_edit.copy()
    df_w["Fabb."] = [r["fabb_irr"] for r in res_att]
    df_w["Att."]  = [r["irr_tot"]  for r in res_att]
    df_w["Ret."]  = [r["ret_h2o"]  for r in res_att]
    fig_w = px.bar(df_w,x="Campo",y=["Fabb.","Att.","Ret."],barmode="group",
        title="Bilancio idrico per campo (m³/anno)",
        color_discrete_sequence=["#0a3d62","#3b82f6","#1a6b3a"])
    fig_w.update_layout(**PLT,legend=dict(orientation="h",y=-0.25,font=dict(size=10)))
    st.plotly_chart(fig_w, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  SCENARI ECONOMICI
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🚀 Business Case & ROI Sostenibilità</div>', unsafe_allow_html=True)
s1,s2,s3 = st.columns(3)
with s1:
    st.markdown(f"""<div class="sc-card sc-base">
      <b style="color:#1a6b3a">📍 Stato Attuale</b>
      <div style="font-size:.82rem;line-height:2;margin-top:.5rem">
        CO₂ netta: <b>{round(tot_netto,1)} t/anno</b><br>
        Crediti CO₂: <b>€{int(val_crediti):,}/anno</b><br>
        Costo gasolio: <b>€{int(tot_c_diesel):,}/anno</b><br>
        Costo fertilizzanti: <b>€{int(tot_c_n):,}/anno</b><br>
        Costo irrigazione: <b>€{int(tot_c_irr):,}/anno</b><br>
        Margine: <b>€{margine:,} ({marg_pct}%)</b>
      </div></div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div class="sc-card sc-opt">
      <b style="color:#92400e">⚡ Rigenerativo Full</b>
      <div style="font-size:.82rem;line-height:2;margin-top:.5rem">
        CO₂ netta: <b>{round(pot_netto,1)} t/anno</b><br>
        Crediti CO₂: <b>€{int(pot_cred):,}/anno</b><br>
        Risparmio gasolio: <b>€{int(risp_die_eur):,}/anno</b><br>
        Risparmio acqua: <b>€{int(risp_h2o_eur):,}/anno</b><br>
        Nuovi crediti: <b>€{int(extra_cred):,}/anno</b><br>
        <b style="color:#92400e">+€{int(guadagno):,}/anno totale</b>
      </div></div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""<div class="sc-card sc-tech">
      <b style="color:#1e40af">🔬 Investimento Tecnologico</b>
      <div style="font-size:.82rem;line-height:2;margin-top:.5rem">
        Investimento: <b>€{int(costo_inv):,}</b><br>
        {'IoT sensori: €3.500<br>' if inv_iot else ''}
        {'Drip irrigation: €'+f"{6000*tot_ha_i:,}"+'<br>' if inv_drip else ''}
        {'Precision GPS: €8.000<br>' if inv_gps else ''}
        {'Biochar: €'+f"{1200*tot_ha_i:,}"+'<br>' if inv_biochar else ''}
        Ritorno annuo: <b>€{int(guadagno):,}</b><br>
        <b style="color:#1e40af">Payback: {payback} anni</b>
      </div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CERTIFICAZIONI GAP ANALYSIS
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📜 Gap Analysis Certificazioni</div>', unsafe_allow_html=True)
certs = [
    ("Biologico (Reg. UE 2018/848)",cert_bio, "+14 pt ESG","12-24 mesi","Prezzo +15-25%"),
    ("SQnpi – Produzione Integrata", cert_sqnpi,"+8 pt ESG", "6-12 mesi", "Accesso GDO +12%"),
    ("GlobalG.A.P.",                 cert_gap,  "+7 pt ESG", "6 mesi",    "Export EU/USA"),
    ("VIVA Sostenibilità",           cert_viva, "+8 pt ESG", "12 mesi",   "Premio vitivinicolo +10%"),
    ("ISO 14064 Carbon FP",          cert_iso,  "+10 pt ESG","6-9 mesi",  f"Crediti @ €42/t"),
    ("CSRD / ESRS",                  cert_csrd, "+8 pt ESG", "12-18 mesi","Filiere >€40M fatturato"),
]
c1c,c2c,c3c = st.columns(3)
for i,(nome,att,punti,tempo,val) in enumerate(certs):
    with [c1c,c2c,c3c][i%3]:
        cls = "cert-on" if att else "cert-off"
        ico = "✅" if att else "○"
        st.markdown(f"""<div class="cert-box {cls}">
          <b style="font-size:.84rem">{ico} {nome}</b><br>
          <span style="font-size:.7rem;color:#7a8c7e">{punti} · {tempo}<br>💶 {val}</span>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  AZIONI PRIORITARIE
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🎯 Piano d\'Azione Prioritario</div>', unsafe_allow_html=True)
azioni = []
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    azioni.append({"p":"alta","t":"Convertire appezzamenti convenzionali → Minima lavorazione",
        "i":f"IPCC FMG +0.18 · +{round(tot_ha*0.025*3.667,1)} tCO₂/anno",
        "e":f"€{round(tot_ha*0.025*3.667*prezzo_co2):,}/anno nuovi crediti",
        "c":"Prerequisito GlobalG.A.P. e ISO 14064"})
if tot_spreco > 500:
    azioni.append({"p":"alta","t":"Eliminare spreco irriguo — drip irrigation",
        "i":f"Spreco attuale {int(tot_spreco):,} m³/anno",
        "e":f"€{int(tot_spreco*costo_acqua):,}/anno risparmio",
        "c":"PAC Eco-Scheme misura idrica"})
if stress_idx > .3:
    azioni.append({"p":"alta","t":f"Gestione stress idrico urgente ({round(stress_idx*100)}%)",
        "i":f"Deficit {round(deficit_idrico)} mm · rischio resa -{round(stress_idx*18,1)}%",
        "e":f"Perdita stimata €{round(fatturato*stress_idx*.15):,} se non gestito",
        "c":"Irrigazione di soccorso + cover crops"})
if not cert_bio and not cert_sqnpi:
    azioni.append({"p":"alta","t":"Avviare certificazione SQnpi",
        "i":"Gateway filiera GDO e export UE",
        "e":"Prezzo vendita +12-18%",
        "c":"6-12 mesi · CAA locale"})
if not cert_iso:
    azioni.append({"p":"media","t":"Certificazione ISO 14064 per vendita crediti",
        "i":f"Bilancio netto {round(tot_netto,1)} tCO₂/anno certificabile",
        "e":f"€{round(max(0,tot_netto)*42):,}/anno su mercato ufficiale",
        "c":"Verra VCS · Gold Standard"})
if marg_pct < 22:
    azioni.append({"p":"media","t":"Ottimizzare struttura costi variabili",
        "i":f"Margine {marg_pct}% sotto soglia resilienza (25%)",
        "e":"Riduzione input chimici compatibile con upgrade ESG",
        "c":"Piano agronomico integrato"})

pm = {"alta":("act-h","🔴"),"media":("act-m","🟡"),"bassa":("act-l","🟢")}
for i,az in enumerate(azioni[:6],1):
    cls,ico = pm[az["p"]]
    st.markdown(f"""<div class="action {cls}">
      <b>{ico} {i}. {az['t']}</b><br>
      <small style="color:#7a8c7e">📊 {az['i']}</small>&nbsp;&nbsp;
      <small style="color:#1a6b3a">💶 {az['e']}</small>&nbsp;&nbsp;
      <small style="color:#9ca3af">📜 {az['c']}</small>
    </div>""", unsafe_allow_html=True)

# RISCHI
st.markdown('<div class="sec">⚠️ Mappa dei Rischi</div>', unsafe_allow_html=True)
rischi=[]
if stress_idx>.4: rischi.append({"l":"alto","t":f"Stress idrico critico {round(stress_idx*100)}% — rischio produttivo immediato"})
if tot_netto<0:   rischi.append({"l":"alto","t":"Bilancio carbonico negativo — azienda emittente netta"})
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    rischi.append({"l":"alto","t":"Lavorazione convenzionale: perdita SOM >0.5% in 5 anni stimata"})
if not any([cert_bio,cert_sqnpi,cert_gap]): rischi.append({"l":"medio","t":"Zero certificazioni: esclusione filiere premium e crediti ufficiali"})
if marg_pct<20: rischi.append({"l":"medio","t":f"Margine {marg_pct}% sotto soglia resilienza"})
rischi.append({"l":"medio","t":"CSRD 2026: filiere >€40M richiederanno ESG rating fornitori entro 2027"})
rischi.append({"l":"basso","t":"Volatilità mercato CO₂ volontario: range €25-65/t nel 2026"})
rischi.append({"l":"basso","t":"Scenario RCP4.5: +1.2°C area mediterranea entro 2035"})
rm = {"alto":"r-alto","medio":"r-medio","basso":"r-basso"}
st.markdown('<div style="line-height:2.8">'+" ".join([f'<span class="risk {rm[r["l"]]}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])+"</div>", unsafe_allow_html=True)

# METODOLOGIA
with st.expander("🔬 Metodologia Scientifica Completa"):
    st.markdown("""
| Modulo | Formula / Standard |
|--------|-------------------|
| **Carbon IPCC Tier 1** | `SOC × coeff × f_text × f_CC × f_clima × FMG × 3.667` |
| **SOC Stock** | `0.30m × 10.000m²/ha × Densità × (SO%/100) × 0.58` |
| **Fattore tessitura** | `1 + (Argilla/100) + (Limo/200)` — MAOC minerale |
| **FMG** | Conv=0.82 / Int=1.00 / Rig=1.15 (IPCC Table 5.5) |
| **Clima** | Pianura 0.93 · Collina l. 0.97 · Collina i. 1.04 · Montana 1.16 |
| **N₂O** | `N × 0.01 × (44/28) × 265` — GWP AR5 |
| **Gasolio** | `L × 2.68 kgCO₂/L` — DEFRA 2024 |
| **Acqua FAO-PM** | `ET₀ live × Kc coltura × ha − pioggia efficace (×0.85)` |
| **Ritenzione SOM** | `(SO%−1) × 1.5mm/m × 3m × 10 × ha` — Rawls et al. |
| **Valore fondiario** | `ha × 15.000€ × (1 + delta_SO × 0.12)` — CREA-AA 2025 |
| **Meteo live** | Open-Meteo API · ECMWF + DWD ICON · 1km risoluzione |
| **Benchmark** | CREA-AA 2025 · RICA-Italia · ISPRA GHG 2024 |
    """)

# ══════════════════════════════════════════════════════════════
#  GENERA REPORT HTML COMPLETO
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📄 Report Professionale</div>', unsafe_allow_html=True)
st.info("Clicca per generare il dossier completo. Aprilo nel browser → **Ctrl+P → Salva come PDF** → consegna al cliente, alla banca, all'ente certificatore.")

if st.button("🖨️ Genera Dossier ESG Completo"):
    oggi = datetime.now().strftime("%d/%m/%Y")

    # tabella campi
    righe_tab = ""
    for i,(_,row) in enumerate(df_edit.iterrows()):
        r = res_att[i]
        righe_tab += f"""<tr>
          <td><b>{row.get('Campo','')}</b></td>
          <td>{row.get('Ettari','')} ha</td>
          <td>{row.get('Coltura','')}</td>
          <td>{row.get('Protocollo','')}</td>
          <td>{row.get('SO %','')}%</td>
          <td>{row.get('Argilla %','')}% / {row.get('Limo %','')}%</td>
          <td>{row.get('Densità','')} g/cm³</td>
          <td>{'✓' if row.get('Cover crops',False) else '—'}</td>
          <td>{int(row.get('Irrigazione m³/ha',0)):,} m³/ha</td>
          <td><b style="color:#1a6b3a">{r['co2_seq']}</b></td>
          <td style="color:#ef4444">{r['co2_emit']}</td>
          <td><b>{"+" if r['co2_netto']>=0 else ""}{r['co2_netto']}</b></td>
          <td>{int(r['fabb_irr']):,}</td>
        </tr>"""

    cert_att = ", ".join([c for c,v in [
        ("Biologico",cert_bio),("SQnpi",cert_sqnpi),("GlobalG.A.P.",cert_gap),
        ("VIVA",cert_viva),("ISO 14064",cert_iso),("CSRD",cert_csrd)] if v]) or "Nessuna attiva"

    az_html = ""
    for a in azioni[:6]:
        col = {"alta":"#ef4444","media":"#c9963a","bassa":"#1a6b3a"}[a["p"]]
        az_html += f"""<div style="border-left:4px solid {col};padding:.55rem 1rem;
          margin:.35rem 0;background:#f9f8f5;border-radius:0 9px 9px 0">
          <b>{a['t']}</b><br>
          <small style="color:#555">📊 {a['i']}</small>&nbsp;
          <small style="color:#1a6b3a">💶 {a['e']}</small>
        </div>"""

    rischi_html = " ".join([f'<span style="display:inline-block;padding:3px 10px;border-radius:20px;font-size:.7rem;font-weight:600;margin:2px;background:{"#fee2e2" if r["l"]=="alto" else "#fef3c7" if r["l"]=="medio" else "#d1fae5"};color:{"#991b1b" if r["l"]=="alto" else "#92400e" if r["l"]=="medio" else "#065f46"}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])

    html = f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<title>AgroLog IA — Dossier ESG — {nome_az}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Lexend',sans-serif;color:#1c1c1c;background:#fff;font-size:12px;}}
@media print{{body{{font-size:10.5px}}.noprint{{display:none}}}}
.hdr{{background:linear-gradient(135deg,#061912,#0f3520 40%,#1a6b3a);
  color:#fff;padding:2rem 2.5rem;border-bottom:4px solid #c9963a;}}
.hdr h1{{font-family:'DM Serif Display',serif;font-size:1.65rem;margin:.3rem 0 .1rem}}
.hdr p{{color:rgba(255,255,255,.62);font-size:.8rem}}
.badge{{background:#c9963a;color:#061912;font-size:.6rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;padding:2px 10px;
  border-radius:20px;margin-bottom:.5rem;display:inline-block}}
.sec{{padding:1.1rem 2.2rem;border-bottom:1px solid #ede9e0}}
.st{{font-family:'DM Serif Display',serif;font-size:1.05rem;color:#061912;
  border-left:4px solid #c9963a;padding-left:.6rem;margin-bottom:.7rem}}
.kg{{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;margin:.5rem 0}}
.k{{background:#f4f1ea;border-radius:10px;padding:.7rem .9rem;text-align:center;
  border:1px solid rgba(15,53,32,.1)}}
.kv{{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#0f3520}}
.kl{{font-size:.6rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.06em}}
table{{width:100%;border-collapse:collapse;font-size:.75rem}}
th{{background:#0f3520;color:#fff;padding:6px 7px;text-align:left;font-weight:500}}
td{{padding:4px 7px;border-bottom:1px solid #eee;vertical-align:middle}}
tr:nth-child(even) td{{background:#f9f7f3}}
.meteo-bar{{background:linear-gradient(90deg,#0a3d62,#0f3520);color:#fff;
  border-radius:9px;padding:.7rem 1.1rem;margin:.4rem 0;font-size:.78rem;line-height:1.8}}
.sign{{border:1px solid #ddd;border-radius:10px;padding:1rem 1.5rem;margin:.5rem 0}}
.ftr{{background:#061912;color:rgba(255,255,255,.45);padding:.8rem 2rem;
  font-size:.62rem;text-align:center}}
.scen{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.6rem;margin:.5rem 0}}
.sc{{border-radius:10px;padding:.8rem 1rem}}
.sc-b{{background:#f0fdf4;border:1.5px dashed #1a6b3a}}
.sc-o{{background:#fffbeb;border:1.5px dashed #c9963a}}
.sc-t{{background:#eff6ff;border:1.5px dashed #3b82f6}}
</style></head><body>

<div class="hdr">
  <div class="badge">Dossier ESG & Carbon Intelligence — AgroLog IA 2026</div>
  <h1>🌿 {nome_az}</h1>
  <p>Consulente: {agronomo} &nbsp;·&nbsp; {regione} / {zona} &nbsp;·&nbsp; {oggi}
  &nbsp;·&nbsp; IPCC Tier 1 · FAO-PM · Meteo Live Open-Meteo</p>
</div>

<div class="sec"><div class="st">Indicatori Chiave</div>
<div class="kg">
  <div class="k"><div class="kv">{score}/100</div><div class="kl">Score ESG — {rcls}</div></div>
  <div class="k"><div class="kv">{round(tot_seq,1)} t</div><div class="kl">CO₂ Sequestrata/anno</div></div>
  <div class="k"><div class="kv">{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</div><div class="kl">Bilancio Carbonico Netto</div></div>
  <div class="k"><div class="kv">€{int(val_crediti):,}</div><div class="kl">Valore Crediti CO₂/anno</div></div>
  <div class="k"><div class="kv">{int(tot_fabb):,} m³</div><div class="kl">Fabbisogno Idrico/anno</div></div>
  <div class="k"><div class="kv">€{int(tot_valore_f):,}</div><div class="kl">Valore Fondo Stimato</div></div>
  <div class="k"><div class="kv">{marg_pct}%</div><div class="kl">Margine Netto</div></div>
  <div class="k"><div class="kv">{round(stress_idx*100):.0f}%</div><div class="kl">Stress Idrico</div></div>
</div></div>

<div class="sec"><div class="st">Meteo Live — {regione} (Open-Meteo · ECMWF · {oggi})</div>
<div class="meteo-bar">
🌡️ Temp 7gg: {M['tmax']}°/{M['tmin']}°C &nbsp;|&nbsp;
🌧️ Pioggia 7gg: {M['pioggia_7g']} mm &nbsp;|&nbsp;
💧 ET₀: {M['et0']} mm/g &nbsp;|&nbsp;
📊 Pioggia 30gg: {MS['pioggia_30g']} mm &nbsp;|&nbsp;
📉 ET₀ 30gg: {MS['et0_30g']} mm &nbsp;|&nbsp;
⚡ Deficit idrico: {round(deficit_idrico)} mm &nbsp;|&nbsp;
🔥 Stress: {round(stress_idx*100):.0f}%
</div></div>

<div class="sec"><div class="st">Dettaglio Appezzamenti — Calcolo IPCC Tier 1</div>
<table><thead><tr>
<th>Campo</th><th>Ettari</th><th>Coltura</th><th>Protocollo</th>
<th>SO%</th><th>Arg/Limo%</th><th>Densità</th><th>CC</th><th>Irrigaz.</th>
<th>CO₂ Seq (t)</th><th>CO₂ Emit (t)</th><th>Netto (t)</th><th>Fabb.Irr m³</th>
</tr></thead><tbody>{righe_tab}</tbody></table></div>

<div class="sec"><div class="st">Scenari Economici</div>
<div class="scen">
<div class="sc sc-b"><b style="color:#1a6b3a">Stato Attuale</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
CO₂ netta: <b>{round(tot_netto,1)} t</b><br>
Crediti: <b>€{int(val_crediti):,}</b><br>
Costo gasolio: €{int(tot_c_diesel):,}<br>
Costo N: €{int(tot_c_n):,}<br>
Costo irr: €{int(tot_c_irr):,}<br>
Margine: <b>{marg_pct}%</b>
</div></div>
<div class="sc sc-o"><b style="color:#92400e">Rigenerativo Full</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
CO₂ netta: <b>{round(pot_netto,1)} t</b><br>
Crediti: <b>€{int(pot_cred):,}</b><br>
Risp. gasolio: <b>€{int(risp_die_eur):,}</b><br>
Risp. acqua: <b>€{int(risp_h2o_eur):,}</b><br>
Nuovi crediti: <b>€{int(extra_cred):,}</b><br>
<b>+€{int(guadagno):,}/anno</b>
</div></div>
<div class="sc sc-t"><b style="color:#1e40af">Investimento Tech</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Investimento: <b>€{int(costo_inv):,}</b><br>
Ritorno: <b>€{int(guadagno):,}/anno</b><br>
Payback: <b>{payback} anni</b><br>
{'IoT: €3.500 ✓<br>' if inv_iot else ''}
{'Drip: €'+f"{6000*tot_ha_i:,}"+'<br>' if inv_drip else ''}
{'GPS: €8.000 ✓<br>' if inv_gps else ''}
{'Biochar: €'+f"{1200*tot_ha_i:,}"+'<br>' if inv_biochar else ''}
</div></div>
</div></div>

<div class="sec"><div class="st">Piano Azioni Prioritarie</div>{az_html}</div>

<div class="sec"><div class="st">Mappa dei Rischi</div>
<div style="line-height:2.5">{rischi_html}</div></div>

<div class="sec"><div class="st">Certificazioni</div>
<p style="font-size:.82rem">Attive: <b>{cert_att}</b></p></div>

<div class="sec"><div class="st">Nota Metodologica</div>
<p style="font-size:.76rem;color:#555;line-height:1.65">
<b>Carbonio:</b> IPCC 2006 Guidelines Vol.4 Agriculture Tier 1, AR5 GWP, FMG factors Table 5.5.
Coefficiente C→CO₂: 3.667 (rapporto molecolare). EF N₂O: 0.01 kg N₂O-N/kg N (GWP 265 AR5).
Gasolio: 2.68 kgCO₂/L (DEFRA 2024). <b>Acqua:</b> FAO Penman-Monteith, Kc da FAO-56,
pioggia efficace ×0.85. Ritenzione SOM: Rawls et al. 1±1.5mm/m/% SO.
<b>Meteo live:</b> Open-Meteo API (ECMWF + DWD ICON, 1km risoluzione, aggiornamento orario).
<b>Valore fondiario:</b> CREA-AA Annuario 2025. <b>Benchmark:</b> RICA-Italia, ISPRA GHG 2024.
<b>Prezzi CO₂:</b> Xpansiv CBL Voluntary Carbon Market Q1 2026.
<i>Report previsionale — certificazione ufficiale crediti richiede verifica Ente Terzo (Verra/Gold Standard/ISAE 3000).</i>
</p></div>

<div class="sec"><div class="st">Firma e Validazione</div>
<div class="sign">
<p><b>Dottore Agronomo:</b> {agronomo} &nbsp;&nbsp;&nbsp; <b>N. Albo:</b> ______________________</p>
<p style="margin:.4rem 0"><b>Data:</b> {oggi} &nbsp;&nbsp;&nbsp; <b>Luogo:</b> ______________________</p>
<p style="margin-top:2rem;color:#bbb">Firma: ______________________ &nbsp;&nbsp;&nbsp; Timbro:</p>
</div></div>

<div class="ftr">
AgroLog IA v5.0 — Carbon & ESG Strategic Intelligence |
IPCC 2006 Tier 1 · FAO-PM Water Balance · Open-Meteo Live · CREA-AA 2025 · ISPRA GHG 2024 |
Report previsionale — verifica Ente Terzo per certificazione ufficiale dei crediti
</div></body></html>"""

    b64 = base64.b64encode(html.encode("utf-8")).decode()
    fn  = f"AgroLog_Dossier_{nome_az.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html"
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="{fn}" '
        f'style="display:inline-block;background:#c9963a;color:#fff;padding:.65rem 2rem;'
        f'border-radius:10px;text-decoration:none;font-weight:700;font-size:.95rem;margin-top:.5rem">'
        f'⬇️ Scarica Dossier ESG</a>', unsafe_allow_html=True)
    st.success(f"✅ Dossier '{fn}' generato! Aprilo nel browser → Ctrl+P → Salva come PDF.")

st.markdown("""<div class="footer">
  AgroLog IA v5.0 — Carbon & ESG Strategic Intelligence |
  IPCC Tier 1 · FAO-PM · Open-Meteo Live · CREA-AA 2025 · Xpansiv CBL Q1 2026 |
  Dati previsionali — sviluppato con 💚
</div>""", unsafe_allow_html=True)
