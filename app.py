import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import requests, base64

# ══════════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════════
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
.hero{background:linear-gradient(135deg,#061912 0%,#0f3520 45%,#1a6b3a 100%);
  padding:2.4rem 3rem 2rem;border-radius:22px;margin-bottom:2rem;
  box-shadow:0 14px 44px rgba(6,25,18,.24);border-bottom:4px solid #c9963a;
  position:relative;overflow:hidden;}
.hero::after{content:'🌿';position:absolute;right:2.5rem;top:50%;
  transform:translateY(-50%);font-size:6rem;opacity:.07;pointer-events:none;}
.hero h1{font-family:'DM Serif Display',serif;color:#fff;font-size:2rem;margin:.3rem 0 .1rem;}
.hero p{color:rgba(255,255,255,.6);font-size:.86rem;margin:0;}
.hero-meta{display:flex;gap:1rem;margin-top:.8rem;flex-wrap:wrap;}
.hero-meta span{background:rgba(255,255,255,.1);color:rgba(255,255,255,.85);
  font-size:.7rem;padding:3px 11px;border-radius:20px;border:1px solid rgba(255,255,255,.15);}
.hero-badge{background:#c9963a;color:#061912;font-size:.62rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;
  border-radius:20px;margin-bottom:.6rem;display:inline-block;}
.kpi{background:#fff;border-radius:18px;padding:1.2rem 1rem;
  border:1px solid rgba(15,53,32,.1);box-shadow:0 4px 14px rgba(6,25,18,.05);
  text-align:center;transition:all .25s;height:100%;}
.kpi:hover{transform:translateY(-4px);box-shadow:0 10px 28px rgba(6,25,18,.12);}
.kpi-v{font-size:1.75rem;font-weight:700;color:#0f3520;line-height:1.1;}
.kpi-l{font-size:.6rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.09em;margin-top:.3rem;}
.kpi-s{font-size:.76rem;color:#1a6b3a;font-weight:600;margin-top:.15rem;}
.sec{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#061912;
  border-left:5px solid #c9963a;padding-left:.7rem;margin:2.2rem 0 1rem;}
.action{background:#fff;border-radius:13px;padding:.9rem 1.15rem;margin:.4rem 0;
  border:1px solid rgba(15,53,32,.1);transition:box-shadow .2s;}
.action:hover{box-shadow:0 4px 14px rgba(6,25,18,.08);}
.act-h{border-left:4px solid #ef4444;}
.act-m{border-left:4px solid #c9963a;}
.act-l{border-left:4px solid #1a6b3a;}
.risk{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.7rem;font-weight:600;margin:3px;}
.r-alto{background:#fee2e2;color:#991b1b;}
.r-medio{background:#fef3c7;color:#92400e;}
.r-basso{background:#d1fae5;color:#065f46;}
.cert-box{border-radius:11px;padding:.85rem 1rem;margin:.3rem 0;border:1px solid rgba(15,53,32,.12);}
.cert-on{background:#f0fdf4;border-color:#1a6b3a;}
.cert-off{background:#fafaf9;}
.sc-card{border-radius:14px;padding:1.3rem 1.5rem;margin:.4rem 0;}
.sc-base{background:#f0fdf4;border:2px dashed #1a6b3a;}
.sc-opt{background:#fffbeb;border:2px dashed #c9963a;}
.sc-tech{background:#eff6ff;border:2px dashed #3b82f6;}
.sc-row{display:flex;justify-content:space-between;font-size:.8rem;padding:2px 0;line-height:1.8;}
.scope-box{border-radius:12px;padding:1rem 1.2rem;margin:.4rem 0;}
.scope1{background:#fff0f0;border:1px solid #fca5a5;}
.scope2{background:#fff7ed;border:1px solid #fdba74;}
.scope3{background:#f0fdf4;border:1px solid #86efac;}
.waste-box{background:#fff;border-radius:12px;padding:1rem 1.2rem;border:1px solid rgba(15,53,32,.1);}
div[data-testid="stSidebar"]{background:#061912;}
div[data-testid="stSidebar"] *{color:rgba(255,255,255,.85)!important;}
div[data-testid="stSidebar"] h2,div[data-testid="stSidebar"] h3{
  font-family:'DM Serif Display',serif!important;color:#fff!important;}
div[data-testid="stSidebar"] label{
  font-size:.7rem!important;text-transform:uppercase;
  letter-spacing:.05em;color:rgba(255,255,255,.48)!important;}
.stButton>button{background:#0f3520!important;color:#fff!important;
  border:none!important;border-radius:10px!important;
  font-weight:600!important;font-size:.9rem!important;padding:.6rem 1.8rem!important;}
.stButton>button:hover{background:#061912!important;}
.footer{font-size:.67rem;color:#9aab9e;text-align:center;margin-top:2.5rem;
  padding-top:1rem;border-top:1px solid rgba(15,53,32,.12);}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  COSTANTI SCIENTIFICHE
# ══════════════════════════════════════════════════════════════════════
COORDS = {
    "Marche":(43.62,13.51),"Toscana":(43.46,11.10),"Emilia-Romagna":(44.50,11.34),
    "Veneto":(45.44,11.88),"Lombardia":(45.46,9.19),"Piemonte":(45.07,7.68),
    "Puglia":(41.12,16.87),"Sicilia":(37.60,14.02),"Campania":(40.83,14.25),
    "Lazio":(41.90,12.49),"Umbria":(43.11,12.39),"Abruzzo":(42.35,13.39),
    "Calabria":(38.90,16.59),"Sardegna":(40.12,9.01),"Altra":(42.50,12.50),
}
F_CLIMA  = {"Pianura":0.93,"Collina litoranea":0.97,"Collina interna":1.04,"Montagna":1.16}
PROT = {
    "Convenzionale":     {"fmg":0.82,"diesel":155,"n_ha":115,"co2c":0.005},
    "Intermedio":        {"fmg":1.00,"diesel": 82,"n_ha": 72,"co2c":0.022},
    "Rigenerativo Full": {"fmg":1.15,"diesel": 40,"n_ha": 32,"co2c":0.055},
}
KC = {"Cereali":1.15,"Vite (DOC/IGT)":0.70,"Olivo":0.65,"Nocciolo":0.80,
      "Frutteto":1.10,"Orticole":1.20,"Foraggere":1.00,"Misto":0.90}

# Fattori emissione fertilizzanti (kgCO₂eq/kg prodotto) — fonte: IPCC + ecoinvent 3.9
EF_FERT = {
    "Urea (46% N)":          {"ef_prod":2.10, "ef_n2o":0.013, "desc":"Alta emissione produzione + N₂O idrolisi"},
    "Nitrato ammoniacale (34% N)":{"ef_prod":5.70,"ef_n2o":0.010,"desc":"Alta emissione produzione, N₂O standard"},
    "Solfato ammonico (21% N)":{"ef_prod":1.45,"ef_n2o":0.010,"desc":"Sottoprodotto industria, emissione produzione moderata"},
    "Ammonio fosfato (18N-46P)":{"ef_prod":2.90,"ef_n2o":0.010,"desc":"Include emissione produzione fosfato"},
    "Concime organico pellettato":{"ef_prod":0.35,"ef_n2o":0.006,"desc":"Bassa emissione produzione, N₂O ridotto"},
    "Letame bovino fresco":   {"ef_prod":0.10,"ef_n2o":0.005,"desc":"Emissione produzione quasi nulla, stabilizzante SOM"},
    "Compost maturo":         {"ef_prod":0.08,"ef_n2o":0.004,"desc":"Carbonio stabile, emissioni minime"},
}

# Fattori emissione fitofarmaci (kgCO₂eq/kg p.a.) — fonte: ecoinvent 3.9
EF_FITO = {
    "Erbicidi":    2.80,
    "Fungicidi":   2.40,
    "Insetticidi": 3.10,
    "Nessuno":     0.00,
}

# Fattori emissione scarti agroalimentari — fonte: IPCC 2006 Vol.5
EF_SCARTI = {
    "Paglia/stocchi (bruciatura)": 1.50,   # kgCO₂eq/kg — bruciatura in campo
    "Paglia/stocchi (interramento)": -0.12,# kgCO₂eq/kg — sequestro carbonio
    "Sansa (smaltimento)":          0.20,
    "Sansa (biogas)":              -0.45,  # evita emissioni metano
    "Vinacce (smaltimento)":        0.18,
    "Vinacce (digestato)":         -0.30,
    "Potature (bruciatura)":        1.20,
    "Potature (cippato energia)":  -0.60,
    "Potature (compostaggio)":     -0.25,
    "Acque reflue (no trattamento)":0.55,
    "Acque reflue (fitodepurazione)":-0.05,
}

# Fattori emissione materie prime acquistate
EF_MATERIE = {
    "Sementi convenzionali (kg)":  0.85,
    "Sementi certificate bio (kg)": 0.40,
    "Imballaggi plastica (kg)":    3.50,
    "Imballaggi cartone (kg)":     1.10,
    "Lubrificanti macchine (L)":   3.20,
    "Acqua potabile (m³)":         0.30,
}

# ══════════════════════════════════════════════════════════════════════
#  DATI DEFAULT TABELLA CAMPI
# ══════════════════════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌿 AgroLog IA")
    st.caption("Carbon & ESG Strategic Intelligence v7")
    st.markdown("---")
    st.markdown("### 🏢 Azienda")
    nome_az   = st.text_input("Ragione Sociale", "Az. Agr. Rossi")
    agronomo  = st.text_input("Dottore Agronomo", "Dott. [Cognome]")
    regione   = st.selectbox("Regione", list(COORDS.keys()))
    zona      = st.selectbox("Zona Altimetrica", list(F_CLIMA.keys()))
    email     = st.text_input("Email / Tel.", "")
    st.markdown("---")
    st.markdown("### 📜 Certificazioni")
    cert_bio   = st.checkbox("Biologico (Reg. UE 2018/848)")
    cert_sqnpi = st.checkbox("SQnpi")
    cert_gap   = st.checkbox("GlobalG.A.P.")
    cert_viva  = st.checkbox("VIVA Sostenibilità")
    cert_iso   = st.checkbox("ISO 14064")
    cert_csrd  = st.checkbox("CSRD / ESRS")
    st.markdown("---")
    st.markdown("### 💹 Mercato & Finanza")
    prezzo_co2   = st.number_input("Prezzo CO₂ (€/t)", 10.0, 200.0, 42.0, 1.0)
    crescita_co2 = st.slider("Crescita prezzo CO₂/anno (%)", 0, 20, 7)
    costo_diesel = st.number_input("Gasolio (€/L)", 0.7, 2.5, 1.18, 0.05)
    costo_acqua  = st.number_input("Irrigazione (€/m³)", 0.1, 2.0, 0.48, 0.05)
    fatturato    = st.number_input("Fatturato (€/anno)", 0, 5000000, 220000, 5000)
    costi_var    = st.number_input("Costi variabili (€/anno)", 0, 5000000, 115000, 5000)
    st.markdown("---")
    st.markdown("### 🔬 Tecnologia")
    inv_iot      = st.checkbox("Sensori IoT suolo (+€3.500)")
    inv_drip     = st.checkbox("Micro-irrigazione (+€6.000/ha)")
    inv_gps      = st.checkbox("Precision farming GPS (+€8.000)")
    inv_biochar  = st.checkbox("Biochar (+€1.200/ha)")

# ══════════════════════════════════════════════════════════════════════
#  METEO — Open-Meteo live + storico
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_meteo(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
               f"et0_fao_evapotranspiration,wind_speed_10m_max,weathercode"
               f"&timezone=Europe/Rome&forecast_days=7")
        d = requests.get(url, timeout=8).json().get("daily", {})
        s = lambda k, fb: [x for x in d.get(k,[]) if x is not None] or [fb]
        return {
            "tmax":      round(np.mean(s("temperature_2m_max",22)),1),
            "tmin":      round(np.mean(s("temperature_2m_min",10)),1),
            "pioggia_7g":round(sum(s("precipitation_sum",0)),1),
            "et0":       round(np.mean(s("et0_fao_evapotranspiration",3.8)),2),
            "vento":     round(max(s("wind_speed_10m_max",20)),1),
            "tmax_list": [round(x,1) for x in s("temperature_2m_max",22)][:7],
            "tmin_list": [round(x,1) for x in s("temperature_2m_min",10)][:7],
            "pioggia_list":[round(x,1) for x in s("precipitation_sum",0)][:7],
            "wcode_list":  s("weathercode",1)[:7],
        }
    except:
        return {"tmax":22,"tmin":10,"pioggia_7g":12,"et0":3.8,"vento":22,
                "tmax_list":[22]*7,"tmin_list":[10]*7,"pioggia_list":[2]*7,"wcode_list":[1]*7}

@st.cache_data(ttl=86400)
def get_storico(lat, lon):
    try:
        end_d = date.today().strftime("%Y-%m-%d")
        start_d = (date.today()-timedelta(days=30)).strftime("%Y-%m-%d")
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
               f"&start_date={start_d}&end_date={end_d}"
               f"&daily=precipitation_sum,et0_fao_evapotranspiration,temperature_2m_mean"
               f"&timezone=Europe/Rome")
        d = requests.get(url, timeout=10).json().get("daily", {})
        s = lambda k, fb: [x for x in d.get(k,[]) if x is not None] or [fb]
        p = s("precipitation_sum", 0); e = s("et0_fao_evapotranspiration",0); t = s("temperature_2m_mean",15)
        return {
            "pioggia_30g": round(sum(p),1),
            "et0_30g":     round(sum(e),1),
            "temp_30g":    round(np.mean(t),1),
            "pioggia_giorni": p,
            "et0_giorni":     e,
            "temp_giorni":    t,
        }
    except:
        return {"pioggia_30g":45,"et0_30g":90,"temp_30g":15,
                "pioggia_giorni":[1.5]*30,"et0_giorni":[3.0]*30,"temp_giorni":[15]*30}

@st.cache_data(ttl=86400)
def get_storico_annuale(lat, lon):
    """Ultimi 12 mesi mensili per media pluviometrica storica"""
    try:
        end_d   = date.today().strftime("%Y-%m-%d")
        start_d = (date.today()-timedelta(days=365)).strftime("%Y-%m-%d")
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
               f"&start_date={start_d}&end_date={end_d}"
               f"&daily=precipitation_sum,temperature_2m_mean,et0_fao_evapotranspiration"
               f"&timezone=Europe/Rome")
        d = requests.get(url, timeout=12).json().get("daily", {})
        dates = d.get("time", [])
        precip = d.get("precipitation_sum", [])
        temp   = d.get("temperature_2m_mean", [])
        et0    = d.get("et0_fao_evapotranspiration", [])
        # Aggrega per mese
        mesi = {}
        for i, dt in enumerate(dates):
            m = dt[:7]  # YYYY-MM
            if m not in mesi: mesi[m] = {"p":[],"t":[],"e":[]}
            if i < len(precip) and precip[i] is not None: mesi[m]["p"].append(precip[i])
            if i < len(temp)   and temp[i]   is not None: mesi[m]["t"].append(temp[i])
            if i < len(et0)    and et0[i]    is not None: mesi[m]["e"].append(et0[i])
        result = []
        for m in sorted(mesi.keys())[-12:]:
            result.append({
                "mese": m,
                "pioggia": round(sum(mesi[m]["p"]),1),
                "temp_media": round(np.mean(mesi[m]["t"]),1) if mesi[m]["t"] else 0,
                "et0": round(sum(mesi[m]["e"]),1),
            })
        return result
    except:
        return []

lat, lon   = COORDS.get(regione, (42.5,12.5))
M          = get_meteo(lat, lon)
MS         = get_storico(lat, lon)
MA         = get_storico_annuale(lat, lon)
deficit    = max(0, MS["et0_30g"] - MS["pioggia_30g"])
stress_idx = min(1.0, deficit / 80)

def wcode_icon(c):
    """WMO weather code → emoji"""
    if c == 0: return "☀️"
    if c <= 3: return "⛅"
    if c <= 49: return "🌫️"
    if c <= 67: return "🌧️"
    if c <= 77: return "❄️"
    if c <= 82: return "🌦️"
    if c <= 99: return "⛈️"
    return "🌤️"

# ══════════════════════════════════════════════════════════════════════
#  MOTORE SCIENTIFICO BASE
# ══════════════════════════════════════════════════════════════════════
def calcola(row, boost=False):
    prot = "Rigenerativo Full" if boost else str(row.get("Protocollo","Intermedio"))
    p    = PROT.get(prot, PROT["Intermedio"])
    ha   = max(0.1, float(row.get("Ettari",1)))
    so   = max(0.1, float(row.get("SO %",1.5)))
    arg  = max(1.0, float(row.get("Argilla %",20)))
    lim  = max(1.0, float(row.get("Limo %",30)))
    den  = max(0.7, float(row.get("Densità",1.3)))
    cc   = bool(row.get("Cover crops",False)) or boost
    col  = str(row.get("Coltura","Cereali"))
    irr  = max(0.0, float(row.get("Irrigazione m³/ha",0)))

    massa  = 0.30 * 10000 * den
    soc    = massa * (so/100) * 0.58
    f_text = 1 + (arg/100) + (lim/200)
    f_cc   = 1.15 if cc else 1.0
    f_clim = F_CLIMA.get(zona, 1.0)
    seq_ha = soc * p["co2c"] * f_text * f_cc * f_clim * p["fmg"]
    co2_seq= seq_ha * 3.667 * ha

    n_kg   = p["n_ha"] * ha
    n2o    = n_kg * 0.01 * (44/28) * 265 / 1000
    diesel = p["diesel"] * ha
    die_co2= diesel * 2.68 / 1000
    co2_emit = n2o + die_co2

    kc       = KC.get(col, 1.0)
    et0_ann  = M["et0"] * 365
    pioggia_e= MS["pioggia_30g"] * 12 * 0.85
    fabb_irr = max(0, (et0_ann*kc - pioggia_e) * 10 * ha)
    irr_tot  = irr * ha
    spreco   = max(0, irr_tot - fabb_irr)
    ret_h2o  = max(0, (so-1.0)*1.5*3*10*ha)

    return {
        "co2_seq":   round(co2_seq,3), "co2_emit":  round(co2_emit,3),
        "co2_netto": round(co2_seq-co2_emit,3),
        "n2o":       round(n2o,3),     "diesel_co2":round(die_co2,3),
        "diesel_l":  round(diesel,1),  "n_kg":      round(n_kg,1),
        "fabb_irr":  round(fabb_irr,0),"irr_tot":   round(irr_tot,0),
        "spreco":    round(spreco,0),   "ret_h2o":   round(ret_h2o,0),
        "c_diesel":  round(diesel*costo_diesel,0),
        "c_n":       round(n_kg*0.85,0),
        "c_irr":     round(irr_tot*costo_acqua,0),
        "valore_f":  round(ha*(15000+(so/1.2-1)*0.12*15000),0),
        "seq_ha":    round(seq_ha*3.667,3),
    }

# ══════════════════════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">AgroLog IA · Platform Pro 2026 · IPCC · FAO · Meteo Live · Scope 1-2-3</div>
  <h1>🌿 {nome_az}</h1>
  <p>Dossier Carbon & ESG Strategic Intelligence — {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
  <div class="hero-meta">
    <span>👨‍💼 {agronomo}</span>
    <span>📍 {regione} / {zona}</span>
    <span>🌡️ {M['tmax']}° / {M['tmin']}°C</span>
    <span>💧 Stress idrico {round(stress_idx*100):.0f}%</span>
    <span>💶 CO₂ @ €{prezzo_co2}/t</span>
    <span>📅 {date.today().strftime('%d/%m/%Y')}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE METEO — RADAR + STORICO
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🌦️ Meteo Live · Radar 7 Giorni · Storico Pluviometrico</div>', unsafe_allow_html=True)

# KPI meteo
wc = st.columns(6)
wcols=[
    (f"{M['tmax']}° / {M['tmin']}°C","Temp. 7gg","previsione"),
    (f"{M['pioggia_7g']} mm","Pioggia 7gg","prossimi giorni"),
    (f"{M['et0']} mm/g","ET₀ FAO","live"),
    (f"{MS['pioggia_30g']} mm","Pioggia 30gg","storico reale"),
    (f"{MS['et0_30g']} mm","ET₀ 30gg","storico reale"),
    (f"{round(stress_idx*100):.0f}%","Stress Idrico","indice corrente"),
]
sc = "#991b1b" if stress_idx>.5 else "#92400e" if stress_idx>.25 else "#1a6b3a"
for col,(v,l,s),clr in zip(wc,wcols,["#0f3520"]*5+[sc]):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v" style="font-size:1.3rem;color:{clr}">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s" style="color:#9aab9e;font-size:.68rem">{s}</div></div>',
                    unsafe_allow_html=True)

if stress_idx>.4:
    st.error(f"⚠️ **Stress idrico critico {round(stress_idx*100):.0f}%** — deficit {round(deficit)} mm. Rischio resa -{round(stress_idx*18,1)}%.")
elif stress_idx>.2:
    st.warning(f"ℹ️ Stress idrico moderato {round(stress_idx*100):.0f}% — monitorare nelle prossime 2 settimane.")
else:
    st.success(f"✅ Bilancio idrico equilibrato — {MS['pioggia_30g']}mm pioggia vs {MS['et0_30g']}mm ET₀ (30gg).")

# RADAR 7 GIORNI + STORICO ANNUALE
mr1, mr2 = st.columns(2)

with mr1:
    # Radar giornaliero 7 gg
    giorni_label = [(date.today()+timedelta(days=i)).strftime("%a %d") for i in range(7)]
    icons = [wcode_icon(c) for c in M["wcode_list"][:7]]
    labels_fmt = [f"{icons[i]} {giorni_label[i]}" for i in range(min(7,len(giorni_label)))]

    fig_rad = go.Figure()
    fig_rad.add_bar(x=labels_fmt, y=M["pioggia_list"][:7], name="Pioggia (mm)",
                    marker_color="#3b82f6", opacity=0.8)
    fig_rad.add_scatter(x=labels_fmt, y=M["tmax_list"][:7], name="Temp. max (°C)",
                        line=dict(color="#ef4444",width=2.5), mode="lines+markers",
                        yaxis="y2")
    fig_rad.add_scatter(x=labels_fmt, y=M["tmin_list"][:7], name="Temp. min (°C)",
                        line=dict(color="#94a3b8",width=1.5,dash="dot"), mode="lines+markers",
                        yaxis="y2")
    fig_rad.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
        font=dict(family="Lexend",color="#061912"),
        title="🌦️ Meteo Radar — Previsione 7 giorni",
        margin=dict(t=44,b=28,l=28,r=60),
        legend=dict(orientation="h",y=-0.22,font=dict(size=9)),
        yaxis=dict(title="Pioggia (mm)"),
        yaxis2=dict(title="°C",
                    overlaying="y", side="right", showgrid=False),
        barmode="overlay"
    )
    st.plotly_chart(fig_rad, use_container_width=True)

with mr2:
    if MA:
        mesi_labels = [m["mese"][5:] for m in MA]  # MM
        mesi_nomi = {"01":"Gen","02":"Feb","03":"Mar","04":"Apr","05":"Mag","06":"Giu",
                     "07":"Lug","08":"Ago","09":"Set","10":"Ott","11":"Nov","12":"Dic"}
        mesi_fmt = [mesi_nomi.get(m,m) for m in mesi_labels]
        piogge_ann = [m["pioggia"] for m in MA]
        et0_ann    = [m["et0"]     for m in MA]
        temp_ann   = [m["temp_media"] for m in MA]

        fig_ann = go.Figure()
        fig_ann.add_bar(x=mesi_fmt, y=piogge_ann, name="Pioggia mensile (mm)",
                        marker_color="#3b82f6", opacity=0.75)
        fig_ann.add_scatter(x=mesi_fmt, y=et0_ann, name="ET₀ mensile (mm)",
                            line=dict(color="#ef4444",width=2.5), mode="lines+markers",
                            yaxis="y")
        fig_ann.add_scatter(x=mesi_fmt, y=temp_ann, name="Temp. media (°C)",
                            line=dict(color="#c9963a",width=2,dash="dot"), mode="lines+markers",
                            yaxis="y2")
        fig_ann.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
            font=dict(family="Lexend",color="#061912"),
            title="📊 Storico Pluviometrico — Ultimi 12 mesi (Open-Meteo ERA5)",
            margin=dict(t=44,b=28,l=28,r=60),
            legend=dict(orientation="h",y=-0.22,font=dict(size=9)),
            yaxis=dict(title="mm"),
            yaxis2=dict(title="°C",overlaying="y",side="right",showgrid=False)
        )
        st.plotly_chart(fig_ann, use_container_width=True)

        # Statistiche pluviometriche
        tot_pioggia_ann = sum(piogge_ann)
        tot_et0_ann     = sum(et0_ann)
        bilancio_ann    = tot_pioggia_ann - tot_et0_ann
        mese_secco      = mesi_fmt[piogge_ann.index(min(piogge_ann))]
        mese_piovoso    = mesi_fmt[piogge_ann.index(max(piogge_ann))]
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:.8rem 1.1rem;
             border:1px solid rgba(15,53,32,.1);font-size:.79rem;margin-top:-.5rem">
          📊 <b>Media annua:</b> {round(tot_pioggia_ann)}mm pioggia · {round(tot_et0_ann)}mm ET₀ ·
          Bilancio <b style="color:{'#1a6b3a' if bilancio_ann>=0 else '#ef4444'}">
          {"+" if bilancio_ann>=0 else ""}{round(bilancio_ann)}mm</b> ·
          Mese più secco: <b>{mese_secco}</b> · Mese più piovoso: <b>{mese_piovoso}</b>
        </div>""", unsafe_allow_html=True)
    else:
        st.info("Dati storici annuali non disponibili momentaneamente.")

# ══════════════════════════════════════════════════════════════════════
#  TABELLA APPEZZAMENTI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📑 Inventario Fondiario</div>', unsafe_allow_html=True)
st.caption("Inserisci i dati reali — tutti gli indicatori si aggiornano istantaneamente.")

df_edit = st.data_editor(
    st.session_state.df_campi, num_rows="dynamic", use_container_width=True,
    column_config={
        "Protocollo":        st.column_config.SelectboxColumn(
                             options=["Convenzionale","Intermedio","Rigenerativo Full"],required=True),
        "Cover crops":       st.column_config.CheckboxColumn(),
        "Coltura":           st.column_config.SelectboxColumn(options=list(KC.keys()),required=True),
        "Ettari":            st.column_config.NumberColumn(min_value=0.1,max_value=5000,format="%.1f"),
        "SO %":              st.column_config.NumberColumn(min_value=0.1,max_value=8.0,format="%.2f"),
        "Argilla %":         st.column_config.NumberColumn(min_value=1,max_value=80),
        "Limo %":            st.column_config.NumberColumn(min_value=1,max_value=80),
        "Densità":           st.column_config.NumberColumn(min_value=0.7,max_value=1.9,format="%.2f"),
        "Irrigazione m³/ha": st.column_config.NumberColumn(min_value=0,max_value=10000),
    }, key="editor_v7"
)
st.session_state.df_campi = df_edit
if len(df_edit) == 0:
    st.warning("Aggiungi almeno un appezzamento."); st.stop()

# ══════════════════════════════════════════════════════════════════════
#  MODULO FERTILIZZANTI — Scope 1 + Scope 3
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🧪 Fertilizzanti & Fitofarmaci — CO₂ Scope 1 + Scope 3</div>', unsafe_allow_html=True)
st.caption("Inserisci i fertilizzanti e fitofarmaci usati nell'anno. Le emissioni vengono aggiunte al bilancio carbonico totale.")

if "df_fert" not in st.session_state:
    st.session_state.df_fert = pd.DataFrame([
        {"Prodotto":"Urea (46% N)", "Quantità (kg/anno)":2800, "Note":"Campo nord cereali"},
        {"Prodotto":"Nitrato ammoniacale (34% N)", "Quantità (kg/anno)":800, "Note":"Vigneto"},
        {"Prodotto":"Letame bovino fresco", "Quantità (kg/anno)":5000, "Note":"Oliveto"},
    ])
if "df_fito" not in st.session_state:
    st.session_state.df_fito = pd.DataFrame([
        {"Prodotto":"Erbicidi","Quantità p.a. (kg/anno)":12.0,"Note":"Cereali"},
        {"Prodotto":"Fungicidi","Quantità p.a. (kg/anno)":8.5,"Note":"Vite"},
    ])

fc1, fc2 = st.columns(2)
with fc1:
    st.markdown("**Fertilizzanti**")
    df_fert = st.data_editor(
        st.session_state.df_fert, num_rows="dynamic", use_container_width=True,
        column_config={
            "Prodotto": st.column_config.SelectboxColumn(options=list(EF_FERT.keys()),required=True),
            "Quantità (kg/anno)": st.column_config.NumberColumn(min_value=0,max_value=500000,format="%.0f"),
        }, key="editor_fert"
    )
    st.session_state.df_fert = df_fert

with fc2:
    st.markdown("**Fitofarmaci**")
    df_fito = st.data_editor(
        st.session_state.df_fito, num_rows="dynamic", use_container_width=True,
        column_config={
            "Prodotto": st.column_config.SelectboxColumn(options=list(EF_FITO.keys()),required=True),
            "Quantità p.a. (kg/anno)": st.column_config.NumberColumn(min_value=0,max_value=10000,format="%.1f"),
        }, key="editor_fito"
    )
    st.session_state.df_fito = df_fito

# Calcolo emissioni fertilizzanti
co2_fert_prod = 0.0   # Scope 3 — produzione industriale
co2_fert_n2o  = 0.0   # Scope 1 — N₂O in campo
fert_detail   = []
for _, fr in df_fert.iterrows():
    prod = str(fr.get("Prodotto",""))
    qty  = max(0.0, float(fr.get("Quantità (kg/anno)",0)))
    ef   = EF_FERT.get(prod, {"ef_prod":0,"ef_n2o":0.01,"desc":""})
    s3   = qty * ef["ef_prod"] / 1000  # tCO₂eq
    s1   = qty * ef["ef_n2o"] * (44/28) * 265 / 1000
    co2_fert_prod += s3
    co2_fert_n2o  += s1
    fert_detail.append({"prod":prod,"qty":qty,"s3":round(s3,3),"s1":round(s1,3),"ef":ef})

co2_fito_s3 = 0.0
for _, ft in df_fito.iterrows():
    prod = str(ft.get("Prodotto",""))
    qty  = max(0.0, float(ft.get("Quantità p.a. (kg/anno)",0)))
    co2_fito_s3 += qty * EF_FITO.get(prod, 0) / 1000

co2_fert_totale = co2_fert_prod + co2_fert_n2o + co2_fito_s3

# ══════════════════════════════════════════════════════════════════════
#  MODULO SCARTI E MATERIE PRIME — Scope 1 + Scope 3
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">♻️ Gestione Scarti & Materie Prime — Scope 1 + Scope 3</div>', unsafe_allow_html=True)

sc1, sc2 = st.columns(2)

if "df_scarti" not in st.session_state:
    st.session_state.df_scarti = pd.DataFrame([
        {"Scarto":"Paglia/stocchi (interramento)","Quantità (t/anno)":8.0,"Note":"Campo cereali"},
        {"Scarto":"Potature (cippato energia)","Quantità (t/anno)":3.0,"Note":"Oliveto e vigneto"},
    ])
if "df_materie" not in st.session_state:
    st.session_state.df_materie = pd.DataFrame([
        {"Materia prima":"Sementi convenzionali (kg)","Quantità":350,"Note":""},
        {"Materia prima":"Imballaggi plastica (kg)","Quantità":80,"Note":""},
    ])

with sc1:
    st.markdown("**Scarti e sottoprodotti**")
    df_scarti = st.data_editor(
        st.session_state.df_scarti, num_rows="dynamic", use_container_width=True,
        column_config={
            "Scarto": st.column_config.SelectboxColumn(options=list(EF_SCARTI.keys()),required=True),
            "Quantità (t/anno)": st.column_config.NumberColumn(min_value=0,max_value=10000,format="%.1f"),
        }, key="editor_scarti"
    )
    st.session_state.df_scarti = df_scarti

with sc2:
    st.markdown("**Materie prime acquistate**")
    df_materie = st.data_editor(
        st.session_state.df_materie, num_rows="dynamic", use_container_width=True,
        column_config={
            "Materia prima": st.column_config.SelectboxColumn(options=list(EF_MATERIE.keys()),required=True),
            "Quantità": st.column_config.NumberColumn(min_value=0,max_value=1000000,format="%.0f"),
        }, key="editor_materie"
    )
    st.session_state.df_materie = df_materie

co2_scarti = 0.0
scarti_detail = []
for _, sr in df_scarti.iterrows():
    sc = str(sr.get("Scarto",""))
    qty = max(0.0, float(sr.get("Quantità (t/anno)",0)))
    ef  = EF_SCARTI.get(sc, 0)
    co2_s = qty * ef
    co2_scarti += co2_s
    scarti_detail.append({"scarto":sc,"qty":qty,"co2":round(co2_s,3),"ef":ef})

co2_materie = 0.0
for _, mr in df_materie.iterrows():
    mat = str(mr.get("Materia prima",""))
    qty = max(0.0, float(mr.get("Quantità",0)))
    # unità variano — convertiamo sempre in unità base (kg o L o m³)
    ef  = EF_MATERIE.get(mat, 0)
    co2_materie += qty * ef / 1000  # → tCO₂eq

# ══════════════════════════════════════════════════════════════════════
#  CALCOLI AGGREGATI
# ══════════════════════════════════════════════════════════════════════
res_att = [calcola(r,False) for _,r in df_edit.iterrows()]
res_pot = [calcola(r,True)  for _,r in df_edit.iterrows()]

def S(key,src=None): return sum(r[key] for r in (src or res_att))
tot_ha      = max(1.0, float(df_edit["Ettari"].sum()))
tot_seq     = S("co2_seq");   tot_emit_base = S("co2_emit")
# Emissioni totali includono ora fertilizzanti + scarti + materie prime
tot_emit    = tot_emit_base + co2_fert_totale + max(0, co2_scarti) + co2_materie
tot_netto   = tot_seq - tot_emit
tot_die_l   = S("diesel_l");  tot_fabb    = S("fabb_irr")
tot_irr     = S("irr_tot");   tot_spreco  = S("spreco")
tot_ret     = S("ret_h2o");   tot_c_die   = S("c_diesel")
tot_c_n     = S("c_n");       tot_c_irr   = S("c_irr")
tot_vf      = S("valore_f")
val_cred    = max(0, tot_netto) * prezzo_co2
margine     = fatturato - costi_var
marg_pct    = round(margine/fatturato*100,1) if fatturato>0 else 0

pot_netto   = S("co2_netto",res_pot) - co2_fert_totale*0.4 - max(0,co2_scarti)*0.3
pot_die_l   = S("diesel_l",res_pot)
pot_cred    = max(0, pot_netto) * prezzo_co2
risp_die    = (tot_die_l - pot_die_l) * costo_diesel
risp_h2o    = tot_spreco * costo_acqua
extra_cred  = pot_cred - val_cred
guadagno    = risp_die + risp_h2o + extra_cred

tot_ha_i    = max(1, int(tot_ha))
costo_inv   = ((3500 if inv_iot else 0)+(6000*tot_ha_i if inv_drip else 0)+
               (8000 if inv_gps else 0)+(1200*tot_ha_i if inv_biochar else 0))
payback     = round(costo_inv/max(guadagno,1),1) if costo_inv>0 else 0

# Score ESG
score = 28
score += min(25, int(max(0, tot_netto/tot_ha)*12))
for c,v in [(14,cert_bio),(8,cert_sqnpi),(7,cert_gap),(8,cert_viva),(10,cert_iso),(8,cert_csrd)]:
    if v: score += c
cc_r = sum(1 for _,r in df_edit.iterrows() if r.get("Cover crops",False))/max(len(df_edit),1)
score += int(cc_r*12)
if tot_spreco < tot_fabb*0.1: score += 7
for v,pts in [(inv_iot,4),(inv_drip,5),(inv_gps,4),(inv_biochar,6)]: score += pts if v else 0
# Bonus per gestione scarti virtuosa
n_scarti_virtuosi = sum(1 for _,sr in df_scarti.iterrows() if EF_SCARTI.get(str(sr.get("Scarto","")),0) < 0)
score += min(8, n_scarti_virtuosi*3)
score = min(100, score)

if score>=80:   rating,rcls,rcol,rbg = "A — Eccellente","A","#065f46","#d1fae5"
elif score>=65: rating,rcls,rcol,rbg = "B — Conforme ESG","B","#1e40af","#dbeafe"
elif score>=48: rating,rcls,rcol,rbg = "C — Sviluppabile","C","#92400e","#fef3c7"
else:           rating,rcls,rcol,rbg = "D — Critico","D","#991b1b","#fee2e2"

# ══════════════════════════════════════════════════════════════════════
#  BILANCIO SCOPE 1-2-3 DETTAGLIATO
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🏭 Bilancio GHG Completo — Scope 1 · 2 · 3 (GHG Protocol)</div>', unsafe_allow_html=True)

sb1, sb2, sb3 = st.columns(3)

scope1_total = tot_emit_base + co2_fert_n2o + max(0, sum(
    r["qty"]*r["ef"] for r in scarti_detail if r["ef"] > 0))
scope2_total = 0.0  # elettricità non inclusa (estendibile)
scope3_total = co2_fert_prod + co2_fito_s3 + co2_materie + abs(min(0, co2_scarti))

with sb1:
    st.markdown(f"""
    <div class="scope-box scope1">
      <div style="font-size:.85rem;font-weight:700;color:#991b1b;margin-bottom:.5rem">
        🔴 Scope 1 — Emissioni Dirette</div>
      <div style="font-size:.78rem;line-height:1.9">
        Gasolio macchine: <b>{round(S('diesel_co2'),2)} tCO₂</b><br>
        N₂O fertilizzanti campo: <b>{round(S('n2o')+co2_fert_n2o,2)} tCO₂eq</b><br>
        Combustione scarti: <b>{round(max(0,sum(r['qty']*r['ef'] for r in scarti_detail if r['ef']>0)),2)} tCO₂</b><br>
        <hr style="border:none;border-top:1px solid #fca5a5;margin:.4rem 0">
        <b>Totale Scope 1: {round(scope1_total,2)} tCO₂eq/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

with sb2:
    st.markdown(f"""
    <div class="scope-box scope2">
      <div style="font-size:.85rem;font-weight:700;color:#92400e;margin-bottom:.5rem">
        🟡 Scope 2 — Emissioni Indirette Energia</div>
      <div style="font-size:.78rem;line-height:1.9">
        Elettricità acquistata: <b>0 tCO₂</b><br>
        <span style="color:#9ca3af;font-size:.72rem">(Aggiungi pompe irrigazione,<br>celle frigorifere, impianti)</span><br>
        <hr style="border:none;border-top:1px solid #fdba74;margin:.4rem 0">
        <b>Totale Scope 2: {round(scope2_total,2)} tCO₂eq/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

with sb3:
    st.markdown(f"""
    <div class="scope-box scope3">
      <div style="font-size:.85rem;font-weight:700;color:#065f46;margin-bottom:.5rem">
        🟢 Scope 3 — Catena del valore (upstream)</div>
      <div style="font-size:.78rem;line-height:1.9">
        Produzione fertilizzanti: <b>{round(co2_fert_prod,2)} tCO₂eq</b><br>
        Produzione fitofarmaci: <b>{round(co2_fito_s3,2)} tCO₂eq</b><br>
        Materie prime acquistate: <b>{round(co2_materie,2)} tCO₂eq</b><br>
        <hr style="border:none;border-top:1px solid #86efac;margin:.4rem 0">
        <b>Totale Scope 3: {round(scope3_total,2)} tCO₂eq/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

# Riepilogo bilancio
bal_col1, bal_col2 = st.columns([2,1])
with bal_col1:
    # Grafico waterfall del bilancio
    seq_bosco  = sum(r["ret_h2o"] for r in res_att)*0  # placeholder
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative","relative","relative","relative","relative","relative","total"],
        x=["Sequestro<br>suolo","Scarti<br>virtuosi","Gasolio<br>macchine","N₂O<br>campo",
           "Fertilizz.<br>Scope3","Scarti<br>emissivi","Bilancio<br>netto"],
        y=[tot_seq,
           abs(min(0,co2_scarti)),
           -(S("diesel_co2")),
           -(S("n2o")+co2_fert_n2o),
           -(co2_fert_prod+co2_fito_s3+co2_materie),
           -(max(0,co2_scarti)),
           0],
        connector={"line":{"color":"rgba(15,53,32,.2)"}},
        increasing={"marker":{"color":"#1a6b3a"}},
        decreasing={"marker":{"color":"#ef4444"}},
        totals={"marker":{"color":"#c9963a"}},
        text=[f"+{round(tot_seq,1)}",
              f"+{round(abs(min(0,co2_scarti)),1)}",
              f"-{round(S('diesel_co2'),1)}",
              f"-{round(S('n2o')+co2_fert_n2o,1)}",
              f"-{round(co2_fert_prod+co2_fito_s3+co2_materie,1)}",
              f"-{round(max(0,co2_scarti),1)}",
              f"{round(tot_netto,1)}"],
        textposition="outside",
    ))
    fig_wf.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
        font=dict(family="Lexend",color="#061912"),
        title="Bilancio GHG Waterfall — tCO₂eq/anno",
        margin=dict(t=44,b=28,l=28,r=16),
        yaxis_title="tCO₂eq/anno",
        showlegend=False
    )
    st.plotly_chart(fig_wf, use_container_width=True)

with bal_col2:
    col_netto = "#065f46" if tot_netto>=0 else "#991b1b"
    st.markdown(f"""
    <div style="background:#fff;border-radius:14px;padding:1.2rem 1.4rem;
         border:1px solid rgba(15,53,32,.1);margin-top:.3rem">
      <div style="font-family:'DM Serif Display',serif;font-size:1rem;color:#061912;margin-bottom:.8rem">
        📊 Riepilogo GHG</div>
      <table style="width:100%;font-size:.78rem;border-collapse:collapse">
        <tr><td style="padding:4px 0;color:#7a8c7e">Sequestro suolo</td>
            <td style="text-align:right;color:#1a6b3a;font-weight:600">+{round(tot_seq,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">Scarti virtuosi</td>
            <td style="text-align:right;color:#1a6b3a;font-weight:600">+{round(abs(min(0,co2_scarti)),1)} t</td></tr>
        <tr style="border-top:1px solid #eee"><td style="padding:4px 0;color:#7a8c7e">Gasolio (Sc.1)</td>
            <td style="text-align:right;color:#ef4444;font-weight:600">-{round(S('diesel_co2'),1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">N₂O (Sc.1)</td>
            <td style="text-align:right;color:#ef4444;font-weight:600">-{round(S('n2o')+co2_fert_n2o,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">Fertilizz. (Sc.3)</td>
            <td style="text-align:right;color:#ef4444;font-weight:600">-{round(co2_fert_prod+co2_fito_s3,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">Materie prime (Sc.3)</td>
            <td style="text-align:right;color:#ef4444;font-weight:600">-{round(co2_materie,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">Scarti emissivi</td>
            <td style="text-align:right;color:#ef4444;font-weight:600">-{round(max(0,co2_scarti),1)} t</td></tr>
        <tr style="border-top:2px solid #1a6b3a"><td style="padding:6px 0;font-weight:700">Bilancio NETTO</td>
            <td style="text-align:right;font-weight:700;font-size:.95rem;color:{col_netto}">
            {"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#7a8c7e">Valore crediti</td>
            <td style="text-align:right;color:#1a6b3a;font-weight:600">€{int(val_cred):,}</td></tr>
      </table>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  KPI STRATEGICI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📊 Indicatori Strategici</div>', unsafe_allow_html=True)
kcols = st.columns(7)
kpis = [
    (f"{score}/100","Score ESG",
     f'<span style="background:{rbg};color:{rcol};padding:2px 10px;border-radius:20px;font-weight:700;font-size:.72rem">{rcls}</span>'),
    (f"{round(tot_seq,1)} t","CO₂ Sequestrata/anno",f"{round(tot_seq/tot_ha,2)} t/ha"),
    (f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t',
     "Bilancio GHG Netto (Sc.1+3)","✅ Carbon Positive" if tot_netto>=0 else "⚠️ Emittente"),
    (f"€{int(val_cred):,}","Valore Crediti CO₂",f"@ €{prezzo_co2}/tCO₂"),
    (f"{int(tot_fabb):,} m³","Fabbisogno Idrico",f"Spreco {int(tot_spreco):,} m³"),
    (f"€{int(tot_vf):,}","Valore Fondo Stimato",f"{int(tot_ha)} ha · CREA-AA"),
    (f"{marg_pct}%","Margine Netto",f"€{margine:,}/anno"),
]
for col,(v,l,s) in zip(kcols,kpis):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s">{s}</div></div>',unsafe_allow_html=True)

# Benchmark
delta_s=score-52; delta_c=round(tot_seq/tot_ha-2.4,2)
bm1,bm2=st.columns(2)
with bm1:
    clr="#1a6b3a" if delta_s>=0 else "#c9963a"
    st.markdown(f"""<div style="background:#fff;border-radius:12px;padding:.75rem 1.1rem;
      border:1px solid rgba(15,53,32,.1);margin-top:.5rem;font-size:.79rem">
      📊 <b>Benchmark CREA-AA 2025:</b>&nbsp;
      Score ESG <b style="color:{clr}">{"+" if delta_s>=0 else ""}{delta_s} pt</b> vs media 52/100&nbsp;·&nbsp;
      CO₂/ha <b style="color:{clr}">{"+" if delta_c>=0 else ""}{delta_c} t</b> vs media 2.4 t/ha
    </div>""",unsafe_allow_html=True)
with bm2:
    pct=max(5,min(95,100-int((score-30)/0.7)))
    st.markdown(f"""<div style="background:#fff;border-radius:12px;padding:.75rem 1.1rem;
      border:1px solid rgba(15,53,32,.1);margin-top:.5rem;font-size:.79rem">
      🏆 <b>Posizionamento:</b>&nbsp;
      Top <b style="color:#1a6b3a">{pct}%</b> aziende agricole italiane&nbsp;·&nbsp;
      Potenziale aggiuntivo: <b>+{max(0,80-score)} pt</b> a scenario rigenerativo
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  GRAFICI ANALISI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📈 Analisi Multi-Dimensionale</div>', unsafe_allow_html=True)
PLT = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#faf9f6",
           font=dict(family="Lexend",color="#061912"),margin=dict(t=44,b=28,l=28,r=16))

g1,g2,g3 = st.columns(3)
with g1:
    # Breakdown emissioni per categoria
    categorie = ["Seq. suolo","Gasolio","N₂O campo","Fertilizz.\nSc.3","Fitofarmaci\nSc.3","Materie\nprime","Scarti"]
    valori    = [tot_seq, -S("diesel_co2"), -(S("n2o")+co2_fert_n2o),
                 -co2_fert_prod, -co2_fito_s3, -co2_materie, -co2_scarti]
    colori    = ["#1a6b3a" if v>0 else "#ef4444" for v in valori]
    fig_br = go.Figure(go.Bar(x=categorie, y=valori, marker_color=colori, opacity=.88))
    fig_br.update_layout(**PLT, title="Breakdown emissioni/sequestro (t/anno)",
                         yaxis_title="tCO₂eq/anno")
    st.plotly_chart(fig_br, use_container_width=True)

with g2:
    cats=["Carbonio","Acqua","Biodiversità","Certificazioni","Economia","Tecnologia"]
    c_s=min(100,int(tot_netto/tot_ha*12+50))
    a_s=max(0,100-int(tot_spreco/max(tot_fabb+1,1)*100))
    b_s=int(cc_r*70+30)
    ce_s=min(100,14*cert_bio+8*cert_sqnpi+7*cert_gap+8*cert_viva+10*cert_iso+8*cert_csrd)
    e_s=min(100,max(0,int(marg_pct*3)))
    t_s=min(100,inv_iot*25+inv_drip*30+inv_gps*25+inv_biochar*20)
    vals=[c_s,a_s,b_s,ce_s,e_s,t_s]
    fig_r=go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=cats+[cats[0]],fill="toself",
        line=dict(color="#1a6b3a",width=2.5),fillcolor="rgba(26,107,58,0.18)",name="Azienda"))
    fig_r.add_trace(go.Scatterpolar(r=[50]*7,theta=cats+[cats[0]],
        line=dict(color="#94a3b8",width=1.5,dash="dot"),name="Media settore",
        fillcolor="rgba(0,0,0,0)"))
    fig_r.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",font=dict(family="Lexend",color="#061912"),
        title="Radar ESG 6 Dimensioni",
        polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=9),
                                   gridcolor="rgba(15,53,32,.12)"),
                   angularaxis=dict(tickfont=dict(size=10))),
        legend=dict(orientation="h",y=-0.12,font=dict(size=9)),
        margin=dict(t=50,b=20,l=20,r=20)
    )
    st.plotly_chart(fig_r, use_container_width=True)

with g3:
    anni=list(range(2026,2032))
    v_b=[max(0,tot_netto)*prezzo_co2*(i+1) for i in range(6)]
    v_p=[max(0,pot_netto)*prezzo_co2*((1+crescita_co2/100)**i)*(i+1) for i in range(6)]
    v_t=[max(0,pot_netto)*prezzo_co2*((1+crescita_co2/100)**i)*(i+1)+guadagno*(i+1)-costo_inv for i in range(6)]
    fig_p=go.Figure()
    fig_p.add_scatter(x=anni,y=v_b,name="Base",line=dict(color="#94a3b8",width=2,dash="dot"),mode="lines+markers")
    fig_p.add_scatter(x=anni,y=v_p,name="Rigenerativo",line=dict(color="#1a6b3a",width=3),mode="lines+markers",
                      fill="tonexty",fillcolor="rgba(26,107,58,0.07)")
    fig_p.add_scatter(x=anni,y=v_t,name="Tech+Rig.",line=dict(color="#c9963a",width=3),mode="lines+markers",
                      fill="tonexty",fillcolor="rgba(201,150,58,0.07)")
    fig_p.update_layout(**PLT,title="Capitalizzazione CO₂ — 3 scenari",
                        yaxis=dict(tickprefix="€",tickformat=",.0f"),
                        legend=dict(orientation="h",y=-0.22,font=dict(size=9)))
    st.plotly_chart(fig_p, use_container_width=True)

g4,g5=st.columns(2)
with g4:
    sx=np.linspace(0.5,5,24); ay=np.linspace(5,60,24)
    z=np.array([[s*(1+a/100)*PROT["Rigenerativo Full"]["co2c"]*3.667 for s in sx] for a in ay])
    fig_h=go.Figure(go.Heatmap(z=z,x=sx,y=ay,
        colorscale=[[0,"#d8f3dc"],[0.5,"#1a6b3a"],[1,"#061912"]],
        colorbar=dict(title="tCO₂/ha")))
    fig_h.add_trace(go.Scatter(x=df_edit["SO %"].tolist(),y=df_edit["Argilla %"].tolist(),
        mode="markers+text",marker=dict(color="#c9963a",size=14,symbol="x",line=dict(width=2.5)),
        text=df_edit["Campo"].tolist(),textposition="top center",name="Campi"))
    fig_h.update_layout(**PLT,title="Potenziale sequestro — Argilla × SO%",
        xaxis_title="SO%",yaxis_title="Argilla%")
    st.plotly_chart(fig_h,use_container_width=True)

with g5:
    df_w=df_edit.copy()
    df_w["Fabbisogno"]=[r["fabb_irr"] for r in res_att]
    df_w["Attuale"]   =[r["irr_tot"]  for r in res_att]
    df_w["Ritenzione"]=[r["ret_h2o"]  for r in res_att]
    fig_w=go.Figure()
    fig_w.add_bar(x=df_w["Campo"],y=df_w["Fabbisogno"],name="Fabbisogno",marker_color="#0a3d62")
    fig_w.add_bar(x=df_w["Campo"],y=df_w["Attuale"],name="Irrig. attuale",marker_color="#3b82f6")
    fig_w.add_bar(x=df_w["Campo"],y=df_w["Ritenzione"],name="Ritenzione SOM",marker_color="#1a6b3a")
    fig_w.update_layout(**PLT,title="Bilancio idrico per campo (m³/anno)",barmode="group",
                        legend=dict(orientation="h",y=-0.22,font=dict(size=9)))
    st.plotly_chart(fig_w,use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
#  SCENARI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🚀 Business Case & ROI Sostenibilità</div>',unsafe_allow_html=True)
s1,s2,s3=st.columns(3)
def row(l,v): return f'<div class="sc-row"><span>{l}</span><b>{v}</b></div>'
with s1:
    st.markdown(f"""<div class="sc-card sc-base">
    <div style="font-size:.92rem;font-weight:700;color:#1a6b3a;margin-bottom:.6rem">📍 Stato Attuale</div>
    {row("CO₂ netta Sc.1+3",f"{round(tot_netto,1)} t/anno")}
    {row("Valore crediti CO₂",f"€{int(val_cred):,}/anno")}
    {row("Emissioni fertilizz.",f"{round(co2_fert_totale,1)} tCO₂eq")}
    {row("Emissioni scarti",f"{round(max(0,co2_scarti),1)} tCO₂eq")}
    {row("Costo gasolio",f"€{int(tot_c_die):,}/anno")}
    {row("Margine netto",f"€{margine:,} ({marg_pct}%)")}
    </div>""",unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div class="sc-card sc-opt">
    <div style="font-size:.92rem;font-weight:700;color:#92400e;margin-bottom:.6rem">⚡ Scenario Rigenerativo</div>
    {row("CO₂ netta",f"{round(pot_netto,1)} t/anno")}
    {row("Crediti CO₂",f"€{int(pot_cred):,}/anno")}
    {row("Risparmio gasolio",f'<span style="color:#1a6b3a">€{int(risp_die):,}</span>')}
    {row("Risparmio acqua",f'<span style="color:#1a6b3a">€{int(risp_h2o):,}</span>')}
    {row("Nuovi crediti",f'<span style="color:#1a6b3a">€{int(extra_cred):,}</span>')}
    <div style="border-top:1px dashed #c9963a;margin-top:.5rem;padding-top:.5rem;text-align:right;font-size:.85rem;color:#92400e">
    <b>+€{int(guadagno):,}/anno totale</b></div>
    </div>""",unsafe_allow_html=True)
with s3:
    tech_l=""
    if inv_iot:    tech_l+=row("Sensori IoT","€3.500")
    if inv_drip:   tech_l+=row("Micro-irrigazione",f"€{6000*tot_ha_i:,}")
    if inv_gps:    tech_l+=row("Precision GPS","€8.000")
    if inv_biochar:tech_l+=row("Biochar",f"€{1200*tot_ha_i:,}")
    if not tech_l: tech_l='<div style="font-size:.78rem;color:#7a8c7e;padding:4px 0">Seleziona tecnologie ←</div>'
    st.markdown(f"""<div class="sc-card sc-tech">
    <div style="font-size:.92rem;font-weight:700;color:#1e40af;margin-bottom:.6rem">🔬 Investimento Tech</div>
    {tech_l}
    {row("Totale investimento",f"€{int(costo_inv):,}")}
    {row("Ritorno annuo",f"€{int(guadagno):,}")}
    <div style="border-top:1px dashed #3b82f6;margin-top:.5rem;padding-top:.5rem;text-align:right;font-size:.85rem;color:#1e40af">
    <b>Payback: {payback} anni</b></div>
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  CERTIFICAZIONI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📜 Gap Analysis Certificazioni</div>',unsafe_allow_html=True)
certs=[
    ("Biologico (Reg. UE 2018/848)",cert_bio,"+14 pt","12-24 mesi","Prezzo +15-25%","#1a6b3a"),
    ("SQnpi – Produzione Integrata",cert_sqnpi,"+8 pt","6-12 mesi","Accesso GDO +12%","#1a6b3a"),
    ("GlobalG.A.P.",cert_gap,"+7 pt","6 mesi","Export EU/USA","#c9963a"),
    ("VIVA Sostenibilità",cert_viva,"+8 pt","12 mesi","Premio viticolo +10%","#c9963a"),
    ("ISO 14064 Carbon FP",cert_iso,"+10 pt","6-9 mesi","Crediti @ €42/t","#0a3d62"),
    ("CSRD / ESRS Reporting",cert_csrd,"+8 pt","12-18 mesi","Filiere >€40M","#0a3d62"),
]
cc1,cc2,cc3=st.columns(3)
for i,(nome,att,punti,tempo,val,colore) in enumerate(certs):
    with [cc1,cc2,cc3][i%3]:
        cls="cert-on" if att else "cert-off"
        ico="✅" if att else "○"
        brd=f"border-left:4px solid {colore};" if att else ""
        st.markdown(f"""<div class="cert-box {cls}" style="{brd}">
          <b style="font-size:.83rem">{ico} {nome}</b><br>
          <span style="font-size:.7rem;color:#7a8c7e">
          <b style="color:{colore}">{punti} ESG</b> · {tempo} · 💶 {val}</span>
        </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  AZIONI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🎯 Piano d\'Azione Prioritario</div>',unsafe_allow_html=True)
azioni=[]
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    azioni.append({"p":"alta","t":"Convertire appezzamenti convenzionali → Minima lavorazione",
        "i":f"IPCC FMG +0.18 · +{round(tot_ha*0.025*3.667,1)} tCO₂/anno",
        "e":f"€{round(tot_ha*0.025*3.667*prezzo_co2):,}/anno nuovi crediti",
        "c":"Prerequisito GlobalG.A.P. e ISO 14064"})
if co2_fert_prod > 1.0:
    azioni.append({"p":"alta","t":"Sostituire fertilizzanti minerali con organici/letame",
        "i":f"Emissioni Scope 3 fertilizzanti: {round(co2_fert_prod,1)} tCO₂eq/anno",
        "e":f"Risparmio stimato -{round(co2_fert_prod*0.6,1)} tCO₂eq · +6 pt ESG",
        "c":"Obbligatorio per accesso Biologico e Carbon Credits Verra"})
if any(EF_SCARTI.get(str(sr.get("Scarto","")),0) > 0.5 for _,sr in df_scarti.iterrows()):
    azioni.append({"p":"alta","t":"Convertire bruciatura scarti in compostaggio o biogas",
        "i":f"Emissioni scarti emissivi: {round(max(0,co2_scarti),1)} tCO₂eq/anno",
        "e":f"Risparmio potenziale -{round(max(0,co2_scarti)*0.8,1)} tCO₂eq · +3 pt ESG",
        "c":"PAC misura 'gestione scarti' · incentivi regionali biogas"})
if tot_spreco>300:
    azioni.append({"p":"alta","t":"Eliminare spreco irriguo con micro-irrigazione",
        "i":f"Spreco attuale {int(tot_spreco):,} m³/anno",
        "e":f"€{int(tot_spreco*costo_acqua):,}/anno risparmio diretto",
        "c":"PAC Eco-Scheme misura idrica"})
if not cert_bio and not cert_sqnpi:
    azioni.append({"p":"media","t":"Avviare certificazione SQnpi",
        "i":"Gateway filiera GDO e export UE","e":"Prezzo vendita +12-18%",
        "c":"6-12 mesi · CAA locale"})
if not cert_iso:
    azioni.append({"p":"media","t":"Certificazione ISO 14064 — bilancio Scope 1+2+3",
        "i":f"Bilancio netto Sc.1+3: {round(tot_netto,1)} tCO₂eq/anno certificabile",
        "e":f"€{round(max(0,tot_netto)*42):,}/anno su mercato ufficiale",
        "c":"Verra VCS · Gold Standard · ora include Scope 3"})

pm={"alta":("act-h","🔴"),"media":("act-m","🟡"),"bassa":("act-l","🟢")}
for i,az in enumerate(azioni[:6],1):
    cls,ico=pm[az["p"]]
    st.markdown(f"""<div class="action {cls}">
      <div style="font-size:.88rem;font-weight:600">{ico} {i}. {az['t']}</div>
      <div style="margin-top:.25rem;font-size:.78rem;color:#7a8c7e">📊 {az['i']}</div>
      <div style="font-size:.78rem;color:#1a6b3a">💶 {az['e']}
      <span style="color:#9ca3af"> · 📜 {az['c']}</span></div>
    </div>""",unsafe_allow_html=True)

# RISCHI
st.markdown('<div class="sec">⚠️ Mappa dei Rischi</div>',unsafe_allow_html=True)
rischi=[]
if stress_idx>.4: rischi.append({"l":"alto","t":f"Stress idrico critico {round(stress_idx*100):.0f}% — rischio produttivo immediato"})
if tot_netto<0:   rischi.append({"l":"alto","t":"Bilancio GHG Sc.1+3 negativo — azienda emittente netta"})
if co2_fert_prod>2.0: rischi.append({"l":"alto","t":f"Emissioni Scope 3 fertilizzanti elevate ({round(co2_fert_prod,1)} t) — vulnerabile a normativa CSRD"})
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    rischi.append({"l":"alto","t":"Lavorazione convenzionale: perdita SOM >0.5% stimata in 5 anni"})
if not any([cert_bio,cert_sqnpi,cert_gap]):
    rischi.append({"l":"medio","t":"Zero certificazioni: esclusione filiere premium e crediti ufficiali"})
if marg_pct<20: rischi.append({"l":"medio","t":f"Margine {marg_pct}% sotto soglia resilienza aziendale"})
rischi.append({"l":"medio","t":"CSRD 2026: filiere >€40M richiedono ESG Scope 1+2+3 dei fornitori entro 2027"})
rischi.append({"l":"basso","t":"Volatilità mercato CO₂ volontario: range €25-65/t nel 2026"})
rischi.append({"l":"basso","t":"Scenario RCP4.5: +1.2°C area mediterranea entro 2035"})
rm={"alto":"r-alto","medio":"r-medio","basso":"r-basso"}
st.markdown('<div style="line-height:3">'+
    " ".join([f'<span class="risk {rm[r["l"]]}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])+
    "</div>",unsafe_allow_html=True)

# METODOLOGIA
with st.expander("🔬 Metodologia Scientifica Completa — IPCC + GHG Protocol + FAO"):
    st.markdown("""
| Modulo | Formula / Riferimento |
|--------|-----------------------|
| **Carbon IPCC Tier 1** | `SOC × coeff × f_tessitura × f_CC × f_clima × FMG × 3.667` |
| **SOC Stock** | `0.30m × 10.000m²/ha × Densità × (SO%/100) × 0.58` |
| **FMG** | Conv=0.82 / Int=1.00 / Rig=1.15 (IPCC 2006 Table 5.5) |
| **N₂O campo (Scope 1)** | `N_kg × EF × (44/28) × GWP` — EF=0.01, GWP=265 AR5 |
| **N₂O fertilizzanti specifici** | EF variabile per tipo (urea 1.3%, nitrato 1.0%, organico 0.6%) |
| **Emissioni produzione fertilizzanti (Scope 3)** | Fattori ecoinvent 3.9 — kgCO₂eq/kg prodotto |
| **Emissioni fitofarmaci (Scope 3)** | Fattori ecoinvent 3.9 — kgCO₂eq/kg p.a. |
| **Emissioni materie prime (Scope 3)** | Fattori medi letteratura LCA |
| **Scarti — bruciatura (Scope 1)** | IPCC 2006 Vol.5 — kgCO₂eq/t residuo |
| **Scarti — sequestro (credito)** | Interramento: -0.12 · Biogas: -0.45 · Compost: -0.25 tCO₂eq/t |
| **Gasolio (Scope 1)** | `L × 2.68 kgCO₂/L` — DEFRA 2024 |
| **Acqua FAO-PM** | `ET₀ live (Open-Meteo) × Kc (FAO-56) × ha − pioggia efficace×0.85` |
| **Meteo radar 7gg** | Open-Meteo Forecast API — ECMWF IFS + DWD ICON · 1km |
| **Storico pluviometrico 12 mesi** | Open-Meteo Archive API — ERA5 reanalisys · 1km |
| **Valore fondiario** | `ha × €15.000 × (1 + Δ_SO×0.12)` — CREA-AA 2025 |
    """)

# ══════════════════════════════════════════════════════════════════════
#  REPORT HTML COMPLETO
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📄 Genera Dossier Professionale</div>',unsafe_allow_html=True)
st.info("Dossier completo con bilancio GHG Scope 1+2+3, meteo storico, fertilizzanti, scarti. **Ctrl+P → Salva come PDF.**")

if st.button("🖨️ Genera Dossier ESG Completo v7"):
    oggi = datetime.now().strftime("%d/%m/%Y")

    # Tabella campi
    righe_tab=""
    for i,(_,row_) in enumerate(df_edit.iterrows()):
        r=res_att[i]
        nc="#1a6b3a" if r["co2_netto"]>=0 else "#ef4444"
        righe_tab+=f"""<tr>
          <td><b>{row_.get("Campo","")}</b></td><td>{row_.get("Ettari","")} ha</td>
          <td>{row_.get("Coltura","")}</td><td>{row_.get("Protocollo","")}</td>
          <td>{row_.get("SO %","")}%</td>
          <td>{row_.get("Argilla %","")}%/{row_.get("Limo %","")}%</td>
          <td>{"✓" if row_.get("Cover crops",False) else "—"}</td>
          <td style="color:#1a6b3a"><b>{r["co2_seq"]}</b></td>
          <td style="color:#ef4444">{r["co2_emit"]}</td>
          <td style="color:{nc}"><b>{"+" if r["co2_netto"]>=0 else ""}{r["co2_netto"]}</b></td>
          <td>{int(r["fabb_irr"]):,}</td>
        </tr>"""

    # Tabella fertilizzanti
    righe_fert=""
    for fd in fert_detail:
        righe_fert+=f"""<tr>
          <td>{fd['prod']}</td><td>{int(fd['qty']):,} kg</td>
          <td style="color:#ef4444">{fd['s1']} t</td>
          <td style="color:#c9963a">{fd['s3']} t</td>
          <td style="font-size:.7rem;color:#777">{fd['ef']['desc']}</td>
        </tr>"""

    # Tabella scarti
    righe_scarti=""
    for sd in scarti_detail:
        col="#ef4444" if sd["ef"]>0 else "#1a6b3a"
        segno="+" if sd["ef"]>0 else ""
        righe_scarti+=f"""<tr>
          <td>{sd['scarto']}</td><td>{sd['qty']} t/anno</td>
          <td style="color:{col}"><b>{segno}{sd['co2']} tCO₂eq</b></td>
        </tr>"""

    # Storico meteo
    storico_html=""
    if MA:
        mesi_nomi={"01":"Gen","02":"Feb","03":"Mar","04":"Apr","05":"Mag","06":"Giu",
                   "07":"Lug","08":"Ago","09":"Set","10":"Ott","11":"Nov","12":"Dic"}
        for m in MA:
            mn=mesi_nomi.get(m["mese"][5:],m["mese"][5:])
            bal=round(m["pioggia"]-m["et0"],0)
            bc="#1a6b3a" if bal>=0 else "#ef4444"
            storico_html+=f"""<tr>
              <td>{mn} {m["mese"][:4]}</td>
              <td style="color:#3b82f6">{m["pioggia"]} mm</td>
              <td style="color:#ef4444">{m["et0"]} mm</td>
              <td style="color:{bc}"><b>{"+" if bal>=0 else ""}{bal} mm</b></td>
              <td>{m["temp_media"]}°C</td>
            </tr>"""

    cert_att=", ".join([c for c,v in [
        ("Biologico",cert_bio),("SQnpi",cert_sqnpi),("GlobalG.A.P.",cert_gap),
        ("VIVA",cert_viva),("ISO 14064",cert_iso),("CSRD",cert_csrd)] if v]) or "Nessuna attiva"

    az_html=""
    for a in azioni[:6]:
        cl={"alta":"#ef4444","media":"#c9963a","bassa":"#1a6b3a"}[a["p"]]
        az_html+=f"""<div style="border-left:4px solid {cl};padding:.5rem 1rem;
          margin:.3rem 0;background:#f9f8f5;border-radius:0 9px 9px 0">
          <b style="font-size:.84rem">{a["t"]}</b><br>
          <span style="font-size:.75rem;color:#555">📊 {a["i"]}</span> ·
          <span style="font-size:.75rem;color:#1a6b3a">💶 {a["e"]}</span>
        </div>"""

    r_html=" ".join([
        f'<span style="display:inline-block;padding:3px 10px;border-radius:20px;'
        f'font-size:.7rem;font-weight:600;margin:2px;'
        f'background:{"#fee2e2" if r["l"]=="alto" else "#fef3c7" if r["l"]=="medio" else "#d1fae5"};'
        f'color:{"#991b1b" if r["l"]=="alto" else "#92400e" if r["l"]=="medio" else "#065f46"}">'
        f'{r["l"].upper()} — {r["t"]}</span>'
        for r in rischi])

    html=f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<title>AgroLog IA v7 — {nome_az} — {oggi}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Lexend',sans-serif;color:#1c1c1c;background:#fff;font-size:11.5px;line-height:1.5}}
@media print{{body{{font-size:10px}};@page{{margin:1.5cm}}}}
.hdr{{background:linear-gradient(135deg,#061912,#0f3520 45%,#1a6b3a);
  color:#fff;padding:1.8rem 2.5rem;border-bottom:4px solid #c9963a;}}
.hdr h1{{font-family:'DM Serif Display',serif;font-size:1.6rem;margin:.3rem 0 .2rem}}
.hdr p{{color:rgba(255,255,255,.6);font-size:.78rem}}
.badge{{background:#c9963a;color:#061912;font-size:.58rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;padding:2px 10px;
  border-radius:20px;margin-bottom:.5rem;display:inline-block}}
.meta{{display:flex;gap:.8rem;margin-top:.6rem;flex-wrap:wrap}}
.meta span{{background:rgba(255,255,255,.12);color:rgba(255,255,255,.8);
  font-size:.66rem;padding:3px 9px;border-radius:15px}}
.sec{{padding:1rem 2rem;border-bottom:1px solid #ede9e0}}
.st{{font-family:'DM Serif Display',serif;font-size:1rem;color:#061912;
  border-left:4px solid #c9963a;padding-left:.6rem;margin-bottom:.7rem}}
.kg{{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin:.5rem 0}}
.k{{background:#f4f1ea;border-radius:10px;padding:.65rem .9rem;text-align:center;
  border:1px solid rgba(15,53,32,.1)}}
.kv{{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#0f3520}}
.kl{{font-size:.58rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.06em;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:.75rem}}
th{{background:#0f3520;color:#fff;padding:5px 7px;text-align:left;font-weight:500}}
td{{padding:4px 7px;border-bottom:1px solid #eee;vertical-align:middle}}
tr:nth-child(even) td{{background:#f9f7f3}}
.meteo{{background:linear-gradient(90deg,#0a2d4a,#0f3520);color:#fff;
  border-radius:9px;padding:.65rem 1.1rem;margin:.4rem 0;font-size:.78rem;line-height:2}}
.scope-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5rem;margin:.5rem 0}}
.sc1{{background:#fff0f0;border:1.5px solid #fca5a5;border-radius:9px;padding:.8rem 1rem}}
.sc2{{background:#fff7ed;border:1.5px solid #fdba74;border-radius:9px;padding:.8rem 1rem}}
.sc3{{background:#f0fdf4;border:1.5px solid #86efac;border-radius:9px;padding:.8rem 1rem}}
.scen{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5rem;margin:.5rem 0}}
.sc{{border-radius:10px;padding:.9rem 1.1rem}}
.sc-b{{background:#f0fdf4;border:1.5px dashed #1a6b3a}}
.sc-o{{background:#fffbeb;border:1.5px dashed #c9963a}}
.sc-t{{background:#eff6ff;border:1.5px dashed #3b82f6}}
.sc-r{{display:flex;justify-content:space-between;font-size:.78rem;padding:2px 0}}
.sign{{border:1px solid #ddd;border-radius:10px;padding:1rem 1.5rem;margin:.5rem 0}}
.ftr{{background:#061912;color:rgba(255,255,255,.4);padding:.7rem 2rem;
  font-size:.6rem;text-align:center;margin-top:1rem}}
</style></head><body>

<div class="hdr">
  <div class="badge">Dossier ESG & Carbon Intelligence v7 — AgroLog IA 2026 — GHG Protocol Scope 1+2+3</div>
  <h1>🌿 {nome_az}</h1>
  <p>Consulente: {agronomo} · {regione} / {zona} · {oggi} · IPCC Tier 1 · FAO-PM · Open-Meteo Live · ecoinvent 3.9</p>
  <div class="meta">
    <span>📊 Score ESG: {score}/100 — {rcls}</span>
    <span>🌿 Bilancio GHG: {"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t/anno</span>
    <span>💶 Crediti: €{int(val_cred):,}/anno</span>
    <span>💧 Stress idrico: {round(stress_idx*100):.0f}%</span>
    <span>🌡️ {M["tmax"]}° / {M["tmin"]}°C</span>
  </div>
</div>

<div class="sec"><div class="st">Indicatori Chiave</div>
<div class="kg">
  <div class="k"><div class="kv">{score}/100</div><div class="kl">Score ESG — {rcls}</div></div>
  <div class="k"><div class="kv">{round(tot_seq,1)} t</div><div class="kl">CO₂ Sequestrata/anno</div></div>
  <div class="k"><div class="kv">{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</div><div class="kl">Bilancio GHG Netto Sc.1+3</div></div>
  <div class="k"><div class="kv">€{int(val_cred):,}</div><div class="kl">Valore Crediti CO₂/anno</div></div>
  <div class="k"><div class="kv">{round(co2_fert_totale,1)} t</div><div class="kl">Emissioni Fertilizzanti Sc.1+3</div></div>
  <div class="k"><div class="kv">{round(co2_scarti,1)} t</div><div class="kl">Emissioni/Crediti Scarti</div></div>
  <div class="k"><div class="kv">{int(tot_fabb):,} m³</div><div class="kl">Fabbisogno Idrico/anno</div></div>
  <div class="k"><div class="kv">{marg_pct}%</div><div class="kl">Margine Netto</div></div>
</div></div>

<div class="sec"><div class="st">Meteo Live & Storico — {regione} (Open-Meteo ERA5 · {oggi})</div>
<div class="meteo">
🌡️ {M["tmax"]}°/{M["tmin"]}°C &nbsp;|&nbsp;
🌧️ Pioggia 7gg: {M["pioggia_7g"]} mm &nbsp;|&nbsp;
💧 ET₀: {M["et0"]} mm/g &nbsp;|&nbsp;
📊 Pioggia 30gg: {MS["pioggia_30g"]} mm &nbsp;|&nbsp;
⚡ Deficit: {round(deficit)} mm &nbsp;|&nbsp;
🔥 Stress: {round(stress_idx*100):.0f}%
</div>
{"<table><thead><tr><th>Mese</th><th>Pioggia</th><th>ET₀</th><th>Bilancio</th><th>Temp. media</th></tr></thead><tbody>"+storico_html+"</tbody></table>" if storico_html else "<p style='font-size:.78rem;color:#999'>Dati storici non disponibili</p>"}
</div>

<div class="sec"><div class="st">Bilancio GHG — Scope 1 + Scope 2 + Scope 3 (GHG Protocol)</div>
<div class="scope-grid">
<div class="sc1"><b style="color:#991b1b;font-size:.85rem">🔴 Scope 1 — Dirette</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Gasolio: <b>{round(S("diesel_co2"),2)} tCO₂</b><br>
N₂O campo+fertilizz.: <b>{round(S("n2o")+co2_fert_n2o,2)} tCO₂eq</b><br>
Combustione scarti: <b>{round(max(0,sum(r["qty"]*r["ef"] for r in scarti_detail if r["ef"]>0)),2)} tCO₂</b><br>
<b>Tot. Sc.1: {round(scope1_total,2)} t</b></div></div>
<div class="sc2"><b style="color:#92400e;font-size:.85rem">🟡 Scope 2 — Energia</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Elettricità: <b>0 t</b><br>
<span style="color:#999">(pompe, celle frigorifere)</span><br>
<b>Tot. Sc.2: {round(scope2_total,2)} t</b></div></div>
<div class="sc3"><b style="color:#065f46;font-size:.85rem">🟢 Scope 3 — Catena valore</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Produzione fertilizz.: <b>{round(co2_fert_prod,2)} tCO₂eq</b><br>
Produzione fitofarmaci: <b>{round(co2_fito_s3,2)} tCO₂eq</b><br>
Materie prime: <b>{round(co2_materie,2)} tCO₂eq</b><br>
<b>Tot. Sc.3: {round(scope3_total,2)} t</b></div></div>
</div></div>

<div class="sec"><div class="st">Fertilizzanti & Fitofarmaci — Emissioni IPCC + ecoinvent 3.9</div>
<table><thead><tr>
<th>Prodotto</th><th>Quantità</th><th>N₂O Sc.1 (tCO₂eq)</th><th>Produzione Sc.3 (tCO₂eq)</th><th>Nota</th>
</tr></thead><tbody>{righe_fert}</tbody>
<tfoot><tr style="background:#f0fdf4">
<td colspan="2"><b>TOTALE fertilizzanti</b></td>
<td><b style="color:#ef4444">{round(co2_fert_n2o,2)} tCO₂eq</b></td>
<td><b style="color:#c9963a">{round(co2_fert_prod,2)} tCO₂eq</b></td>
<td></td></tr></tfoot></table></div>

<div class="sec"><div class="st">Gestione Scarti & Sottoprodotti</div>
<table><thead><tr><th>Scarto/Sottoprodotto</th><th>Quantità</th><th>CO₂eq (t) — + emissione / - credito</th></tr></thead>
<tbody>{righe_scarti}</tbody>
<tfoot><tr style="background:#f0fdf4"><td colspan="2"><b>BILANCIO SCARTI</b></td>
<td><b style="color:{'#ef4444' if co2_scarti>0 else '#1a6b3a'}">{"+" if co2_scarti>0 else ""}{round(co2_scarti,2)} tCO₂eq</b></td></tr></tfoot>
</table></div>

<div class="sec"><div class="st">Dettaglio Appezzamenti — IPCC Tier 1</div>
<table><thead><tr>
<th>Campo</th><th>ha</th><th>Coltura</th><th>Protocollo</th>
<th>SO%</th><th>Arg/Limo%</th><th>CC</th>
<th>CO₂ Seq (t)</th><th>CO₂ Emit (t)</th><th>Netto (t)</th><th>Fabb.Irr m³</th>
</tr></thead><tbody>{righe_tab}</tbody>
<tfoot><tr style="background:#f0fdf4;font-weight:600">
<td>TOTALE</td><td>{round(tot_ha,1)} ha</td><td colspan="5"></td>
<td style="color:#1a6b3a">{round(tot_seq,1)}</td>
<td style="color:#ef4444">{round(tot_emit_base,1)}</td>
<td>{"+" if (tot_seq-tot_emit_base)>=0 else ""}{round(tot_seq-tot_emit_base,1)}</td>
<td>{int(tot_fabb):,}</td>
</tr></tfoot></table></div>

<div class="sec"><div class="st">Scenari Economici</div>
<div class="scen">
<div class="sc sc-b"><b style="color:#1a6b3a;font-size:.87rem">📍 Stato Attuale</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta Sc.1+3</span><b>{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</b></div>
<div class="sc-r"><span>Crediti CO₂</span><b>€{int(val_cred):,}/anno</b></div>
<div class="sc-r"><span>Em. fertilizzanti</span><b>{round(co2_fert_totale,1)} t</b></div>
<div class="sc-r"><span>Costo gasolio</span><b>€{int(tot_c_die):,}</b></div>
<div class="sc-r"><span>Margine</span><b>{marg_pct}%</b></div>
</div></div>
<div class="sc sc-o"><b style="color:#92400e;font-size:.87rem">⚡ Rigenerativo</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta</span><b>{round(pot_netto,1)} t</b></div>
<div class="sc-r"><span>Crediti</span><b>€{int(pot_cred):,}/anno</b></div>
<div class="sc-r"><span>Risp. gasolio</span><b style="color:#1a6b3a">€{int(risp_die):,}</b></div>
<div class="sc-r"><span>Risp. acqua</span><b style="color:#1a6b3a">€{int(risp_h2o):,}</b></div>
<div style="border-top:1px dashed #c9963a;margin-top:.4rem;padding-top:.3rem;text-align:right">
<b style="color:#92400e">+€{int(guadagno):,}/anno</b></div>
</div></div>
<div class="sc sc-t"><b style="color:#1e40af;font-size:.87rem">🔬 Tech</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>Investimento</span><b>€{int(costo_inv):,}</b></div>
<div class="sc-r"><span>Ritorno/anno</span><b style="color:#1a6b3a">€{int(guadagno):,}</b></div>
<div class="sc-r"><span>Payback</span><b style="color:#1e40af">{payback} anni</b></div>
</div></div>
</div></div>

<div class="sec"><div class="st">Piano Azioni Prioritarie</div>{az_html}</div>

<div class="sec"><div class="st">Mappa dei Rischi</div>
<div style="line-height:2.5">{r_html}</div></div>

<div class="sec"><div class="st">Certificazioni Attive</div>
<p style="font-size:.82rem">Attive: <b>{cert_att}</b></p></div>

<div class="sec"><div class="st">Nota Metodologica</div>
<p style="font-size:.75rem;color:#555;line-height:1.65">
<b>Carbonio suolo:</b> IPCC 2006 Vol.4 Tier 1, AR5 GWP.
<b>Fertilizzanti (Scope 1+3):</b> EF produzione da ecoinvent 3.9; N₂O specifici per tipo (urea EF=0.013, nitrato=0.010, organico=0.006).
<b>Fitofarmaci (Scope 3):</b> fattori ecoinvent 3.9.
<b>Scarti:</b> IPCC 2006 Vol.5 — combustione, interramento, biogas, compostaggio.
<b>Materie prime (Scope 3):</b> fattori LCA letteratura.
<b>Acqua:</b> FAO Penman-Monteith, Kc da FAO-56.
<b>Meteo radar:</b> Open-Meteo Forecast API (ECMWF IFS + DWD ICON, 1km, orario).
<b>Storico pluviometrico:</b> Open-Meteo Archive API (ERA5 reanalisys, 1km, 12 mesi).
<b>Valore fondiario:</b> CREA-AA 2025.
<b>Prezzi CO₂:</b> Xpansiv CBL Q1 2026.
<i>Report previsionale — certif. ufficiale crediti richiede verifica Ente Terzo (Verra VCS / Gold Standard / ISAE 3000).</i>
</p></div>

<div class="sec"><div class="st">Firma e Validazione</div>
<div class="sign">
<table style="font-size:.82rem;border:none">
<tr><td style="border:none;padding:4px 8px"><b>Dottore Agronomo:</b></td>
    <td style="border:none">{agronomo}</td>
    <td style="border:none;padding:4px 8px"><b>N. Albo:</b></td>
    <td style="border:none">______________________</td></tr>
<tr><td style="border:none;padding:4px 8px"><b>Data:</b></td>
    <td style="border:none">{oggi}</td>
    <td style="border:none;padding:4px 8px"><b>Luogo:</b></td>
    <td style="border:none">______________________</td></tr>
</table>
<div style="margin-top:2rem;display:flex;gap:5rem">
  <p style="color:#bbb;font-size:.8rem">Firma: ______________________</p>
  <div><p style="color:#bbb;font-size:.8rem">Timbro:</p>
  <div style="width:75px;height:75px;border:1px dashed #ddd;border-radius:50%;margin-top:.3rem"></div></div>
</div></div></div>

<div class="ftr">AgroLog IA v7.0 — Carbon & ESG Strategic Intelligence |
IPCC 2006 Tier 1 · FAO-PM · GHG Protocol Scope 1+2+3 · ecoinvent 3.9 · Open-Meteo Live + ERA5 |
CREA-AA 2025 · ISPRA GHG 2024 · Xpansiv CBL Q1 2026 |
Dati previsionali — verifica Ente Terzo per certificazione ufficiale crediti carbonio</div>
</body></html>"""

    b64=base64.b64encode(html.encode("utf-8")).decode()
    fn=f"AgroLog_v7_{nome_az.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html"
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="{fn}" '
        f'style="display:inline-block;background:#c9963a;color:#fff;padding:.7rem 2.2rem;'
        f'border-radius:10px;text-decoration:none;font-weight:700;font-size:.95rem;'
        f'margin-top:.6rem;box-shadow:0 4px 12px rgba(201,150,58,.35)">'
        f'⬇️ Scarica Dossier ESG v7 — Scope 1+2+3</a>',
        unsafe_allow_html=True)
    st.success(f"✅ '{fn}' generato — Apri nel browser → Ctrl+P → Salva come PDF.")

st.markdown("""<div class="footer">
  AgroLog IA v7.0 — Carbon & ESG Strategic Intelligence |
  IPCC Tier 1 · FAO-PM · GHG Protocol Scope 1+2+3 · Open-Meteo Live+ERA5 · ecoinvent 3.9 |
  Sviluppato con 💚 — ogni giorno più preciso
</div>""",unsafe_allow_html=True)
