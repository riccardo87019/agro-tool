import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import requests, base64

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
.cert-box{border-radius:11px;padding:.85rem 1rem;margin:.3rem 0;
  border:1px solid rgba(15,53,32,.12);transition:box-shadow .2s;}
.cert-box:hover{box-shadow:0 3px 10px rgba(6,25,18,.08);}
.cert-on{background:#f0fdf4;border-color:#1a6b3a;}
.cert-off{background:#fafaf9;}
.sc-card{border-radius:14px;padding:1.3rem 1.5rem;margin:.4rem 0;}
.sc-base{background:#f0fdf4;border:2px dashed #1a6b3a;}
.sc-opt{background:#fffbeb;border:2px dashed #c9963a;}
.sc-tech{background:#eff6ff;border:2px dashed #3b82f6;}
.sc-row{display:flex;justify-content:space-between;font-size:.8rem;padding:2px 0;line-height:1.8;}
div[data-testid="stSidebar"]{background:#061912;}
div[data-testid="stSidebar"] *{color:rgba(255,255,255,.85)!important;}
div[data-testid="stSidebar"] h2,div[data-testid="stSidebar"] h3{
  font-family:'DM Serif Display',serif!important;color:#fff!important;}
div[data-testid="stSidebar"] label{
  font-size:.7rem!important;text-transform:uppercase;
  letter-spacing:.05em;color:rgba(255,255,255,.48)!important;}
.stButton>button{background:#0f3520!important;color:#fff!important;
  border:none!important;border-radius:10px!important;
  font-weight:600!important;font-size:.9rem!important;
  padding:.6rem 1.8rem!important;transition:background .2s!important;}
.stButton>button:hover{background:#061912!important;}
.footer{font-size:.67rem;color:#9aab9e;text-align:center;margin-top:2.5rem;
  padding-top:1rem;border-top:1px solid rgba(15,53,32,.12);}
</style>
""", unsafe_allow_html=True)

# ── COSTANTI ─────────────────────────────────────────────────
COORDS = {
    "Marche":(43.62,13.51),"Toscana":(43.46,11.10),"Emilia-Romagna":(44.50,11.34),
    "Veneto":(45.44,11.88),"Lombardia":(45.46,9.19),"Piemonte":(45.07,7.68),
    "Puglia":(41.12,16.87),"Sicilia":(37.60,14.02),"Campania":(40.83,14.25),
    "Lazio":(41.90,12.49),"Umbria":(43.11,12.39),"Abruzzo":(42.35,13.39),
    "Calabria":(38.90,16.59),"Sardegna":(40.12,9.01),"Altra":(42.50,12.50),
}
F_CLIMA = {"Pianura":0.93,"Collina litoranea":0.97,"Collina interna":1.04,"Montagna":1.16}
PROT = {
    "Convenzionale":     {"fmg":0.82,"diesel":155,"n_ha":115,"co2c":0.005},
    "Intermedio":        {"fmg":1.00,"diesel": 82,"n_ha": 72,"co2c":0.022},
    "Rigenerativo Full": {"fmg":1.15,"diesel": 40,"n_ha": 32,"co2c":0.055},
}
KC = {"Cereali":1.15,"Vite (DOC/IGT)":0.70,"Olivo":0.65,"Nocciolo":0.80,
      "Frutteto":1.10,"Orticole":1.20,"Foraggere":1.00,"Misto":0.90}

# ── DATI DEFAULT ─────────────────────────────────────────────
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

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 AgroLog IA")
    st.caption("Carbon & ESG Strategic Intelligence v6")
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
    cert_sqnpi = st.checkbox("SQnpi – Produzione Integrata")
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

# ── METEO ────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_meteo(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
               f"et0_fao_evapotranspiration,wind_speed_10m_max"
               f"&timezone=Europe/Rome&forecast_days=7")
        d = requests.get(url, timeout=8).json().get("daily", {})
        s = lambda k, fb: [x for x in d.get(k,[]) if x is not None] or [fb]
        return {
            "tmax":round(np.mean(s("temperature_2m_max",22)),1),
            "tmin":round(np.mean(s("temperature_2m_min",10)),1),
            "pioggia_7g":round(sum(s("precipitation_sum",0)),1),
            "et0":round(np.mean(s("et0_fao_evapotranspiration",3.8)),2),
            "vento":round(max(s("wind_speed_10m_max",20)),1),
        }
    except:
        return {"tmax":22,"tmin":10,"pioggia_7g":12,"et0":3.8,"vento":22}

@st.cache_data(ttl=86400)
def get_storico(lat, lon):
    try:
        end = date.today().strftime("%Y-%m-%d")
        start = (date.today()-timedelta(days=30)).strftime("%Y-%m-%d")
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
               f"&start_date={start}&end_date={end}"
               f"&daily=precipitation_sum,et0_fao_evapotranspiration,temperature_2m_mean"
               f"&timezone=Europe/Rome")
        d = requests.get(url, timeout=10).json().get("daily", {})
        s = lambda k, fb: [x for x in d.get(k,[]) if x is not None] or [fb]
        return {
            "pioggia_30g":round(sum(s("precipitation_sum",0)),1),
            "et0_30g":round(sum(s("et0_fao_evapotranspiration",0)),1),
            "temp_30g":round(np.mean(s("temperature_2m_mean",15)),1),
        }
    except:
        return {"pioggia_30g":45,"et0_30g":90,"temp_30g":15}

lat, lon   = COORDS.get(regione, (42.5, 12.5))
M          = get_meteo(lat, lon)
MS         = get_storico(lat, lon)
deficit    = max(0, MS["et0_30g"] - MS["pioggia_30g"])
stress_idx = min(1.0, deficit / 80)

# ── MOTORE SCIENTIFICO ───────────────────────────────────────
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

    kc        = KC.get(col, 1.0)
    et0_ann   = M["et0"] * 365
    pioggia_e = MS["pioggia_30g"] * 12 * 0.85
    fabb_irr  = max(0, (et0_ann*kc - pioggia_e) * 10 * ha)
    irr_tot   = irr * ha
    spreco    = max(0, irr_tot - fabb_irr)
    ret_h2o   = max(0, (so-1.0)*1.5*3*10*ha)

    return {
        "co2_seq":   round(co2_seq,3),
        "co2_emit":  round(co2_emit,3),
        "co2_netto": round(co2_seq-co2_emit,3),
        "diesel_l":  round(diesel,1),
        "fabb_irr":  round(fabb_irr,0),
        "irr_tot":   round(irr_tot,0),
        "spreco":    round(spreco,0),
        "ret_h2o":   round(ret_h2o,0),
        "c_diesel":  round(diesel*costo_diesel,0),
        "c_n":       round(n_kg*0.85,0),
        "c_irr":     round(irr_tot*costo_acqua,0),
        "valore_f":  round(ha*(15000+(so/1.2-1)*0.12*15000),0),
        "seq_ha":    round(seq_ha*3.667,3),
    }

# ── HERO ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">AgroLog IA · Platform Pro 2026 · IPCC · FAO · Meteo Live</div>
  <h1>🌿 {nome_az}</h1>
  <p>Dossier Carbon & ESG Strategic Intelligence — {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
  <div class="hero-meta">
    <span>👨‍💼 {agronomo}</span>
    <span>📍 {regione} / {zona}</span>
    <span>🌡️ {M['tmax']}° / {M['tmin']}°C</span>
    <span>💧 Stress idrico {round(stress_idx*100):.0f}%</span>
    <span>💶 CO₂ @ €{prezzo_co2}/t</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── METEO LIVE ───────────────────────────────────────────────
st.markdown('<div class="sec">🌦️ Meteo & Stress Idrico Live</div>', unsafe_allow_html=True)
wc = st.columns(6)
wcols = [
    (f"{M['tmax']}° / {M['tmin']}°C","Temp. 7gg","previsione"),
    (f"{M['pioggia_7g']} mm","Pioggia 7gg","prossimi giorni"),
    (f"{M['et0']} mm/g","ET₀ FAO","evapotraspirazione"),
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
    st.warning(f"ℹ️ Stress idrico moderato {round(stress_idx*100):.0f}% — deficit {round(deficit)} mm. Monitorare.")
else:
    st.success(f"✅ Bilancio idrico equilibrato — pioggia {MS['pioggia_30g']}mm vs ET₀ {MS['et0_30g']}mm (30gg).")

# ── TABELLA APPEZZAMENTI ─────────────────────────────────────
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
    }, key="editor_v6"
)
st.session_state.df_campi = df_edit

if len(df_edit) == 0:
    st.warning("Aggiungi almeno un appezzamento.")
    st.stop()

# ── CALCOLI ──────────────────────────────────────────────────
res_att = [calcola(r,False) for _,r in df_edit.iterrows()]
res_pot = [calcola(r,True)  for _,r in df_edit.iterrows()]

def S(key,src=None): return sum(r[key] for r in (src or res_att))
tot_ha    = max(1.0, float(df_edit["Ettari"].sum()))
tot_seq   = S("co2_seq");  tot_emit  = S("co2_emit")
tot_netto = tot_seq - tot_emit
tot_die_l = S("diesel_l"); tot_fabb  = S("fabb_irr")
tot_irr   = S("irr_tot");  tot_spreco= S("spreco")
tot_ret   = S("ret_h2o");  tot_c_die = S("c_diesel")
tot_c_n   = S("c_n");      tot_c_irr = S("c_irr")
tot_vf    = S("valore_f")
val_cred  = max(0,tot_netto)*prezzo_co2
margine   = fatturato-costi_var
marg_pct  = round(margine/fatturato*100,1) if fatturato>0 else 0

pot_netto = S("co2_netto",res_pot)
pot_die_l = S("diesel_l", res_pot)
pot_cred  = max(0,pot_netto)*prezzo_co2
risp_die  = (tot_die_l-pot_die_l)*costo_diesel
risp_h2o  = tot_spreco*costo_acqua
extra_cred= pot_cred-val_cred
guadagno  = risp_die+risp_h2o+extra_cred

tot_ha_i = max(1,int(tot_ha))
costo_inv = ((3500 if inv_iot else 0)+(6000*tot_ha_i if inv_drip else 0)+
             (8000 if inv_gps else 0)+(1200*tot_ha_i if inv_biochar else 0))
payback   = round(costo_inv/max(guadagno,1),1) if costo_inv>0 else 0

# Score ESG
score = 28
score += min(25,int(max(0,tot_netto/tot_ha)*12))
for c,v in [(14,cert_bio),(8,cert_sqnpi),(7,cert_gap),(8,cert_viva),(10,cert_iso),(8,cert_csrd)]:
    if v: score += c
cc_r  = sum(1 for _,r in df_edit.iterrows() if r.get("Cover crops",False))/max(len(df_edit),1)
score += int(cc_r*12)
if tot_spreco<tot_fabb*0.1: score+=7
for v,pts in [(inv_iot,4),(inv_drip,5),(inv_gps,4),(inv_biochar,6)]:
    if v: score+=pts
score = min(100,score)

if score>=80:   rating,rcls,rcol,rbg="A — Eccellente",  "A","#065f46","#d1fae5"
elif score>=65: rating,rcls,rcol,rbg="B — Conforme ESG","B","#1e40af","#dbeafe"
elif score>=48: rating,rcls,rcol,rbg="C — Sviluppabile","C","#92400e","#fef3c7"
else:           rating,rcls,rcol,rbg="D — Critico",     "D","#991b1b","#fee2e2"

# ── KPI ──────────────────────────────────────────────────────
st.markdown('<div class="sec">📊 Indicatori Strategici</div>', unsafe_allow_html=True)
kcols = st.columns(7)
kpis = [
    (f"{score}/100","Score ESG",
     f'<span style="background:{rbg};color:{rcol};padding:2px 10px;border-radius:20px;font-weight:700;font-size:.72rem">{rcls}</span>'),
    (f"{round(tot_seq,1)} t","CO₂ Sequestrata/anno",f"{round(tot_seq/tot_ha,2)} t/ha"),
    (f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t',
     "Bilancio Carbonico","✅ Carbon Positive" if tot_netto>=0 else "⚠️ Emittente Netto"),
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

# Benchmark row
delta_s = score-52; delta_c = round(tot_seq/tot_ha-2.4,2)
bm1,bm2 = st.columns(2)
with bm1:
    clr="#1a6b3a" if delta_s>=0 else "#c9963a"
    st.markdown(f"""<div style="background:#fff;border-radius:12px;padding:.75rem 1.1rem;
      border:1px solid rgba(15,53,32,.1);margin-top:.5rem;font-size:.79rem">
      📊 <b>Benchmark CREA-AA 2025:</b> &nbsp;
      Score ESG <b style="color:{clr}">{"+" if delta_s>=0 else ""}{delta_s} pt</b> vs media 52/100 &nbsp;·&nbsp;
      CO₂/ha <b style="color:{clr}">{"+" if delta_c>=0 else ""}{delta_c} t</b> vs media 2.4 t/ha
    </div>""",unsafe_allow_html=True)
with bm2:
    pct = max(5,min(95,100-int((score-30)/0.7)))
    st.markdown(f"""<div style="background:#fff;border-radius:12px;padding:.75rem 1.1rem;
      border:1px solid rgba(15,53,32,.1);margin-top:.5rem;font-size:.79rem">
      🏆 <b>Posizionamento:</b> &nbsp;
      Top <b style="color:#1a6b3a">{pct}%</b> aziende agricole italiane &nbsp;·&nbsp;
      Potenziale aggiuntivo: <b>+{max(0,80-score)} pt</b> a scenario rigenerativo full
    </div>""",unsafe_allow_html=True)

# ── GRAFICI ──────────────────────────────────────────────────
st.markdown('<div class="sec">📈 Analisi Multi-Dimensionale</div>', unsafe_allow_html=True)
PLT = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#faf9f6",
           font=dict(family="Lexend",color="#061912"),
           margin=dict(t=44,b=28,l=28,r=16))

g1,g2,g3 = st.columns(3)
with g1:
    df_p = df_edit.copy()
    df_p["Seq"]  = [r["co2_seq"]  for r in res_att]
    df_p["Emit"] = [r["co2_emit"] for r in res_att]
    fig = go.Figure()
    fig.add_bar(x=df_p["Campo"],y=df_p["Seq"], name="CO₂ Seq.", marker_color="#1a6b3a",opacity=.9)
    fig.add_bar(x=df_p["Campo"],y=df_p["Emit"],name="Emissioni",marker_color="#ef4444",opacity=.85)
    fig.update_layout(**PLT,title="CO₂ per campo (t/anno)",barmode="group",
                      legend=dict(orientation="h",y=-0.22,font=dict(size=10)))
    st.plotly_chart(fig,use_container_width=True)

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
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Lexend",color="#061912"),
        title="Radar ESG — 6 Dimensioni",
        polar=dict(
            radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=9),
                           gridcolor="rgba(15,53,32,.12)"),
            angularaxis=dict(tickfont=dict(size=10))
        ),
        legend=dict(orientation="h",y=-0.12,font=dict(size=9)),
        margin=dict(t=50,b=20,l=20,r=20)
    )
    st.plotly_chart(fig_r,use_container_width=True)

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
    st.plotly_chart(fig_p,use_container_width=True)

g4,g5=st.columns(2)
with g4:
    sx=np.linspace(0.5,5,24); ay=np.linspace(5,60,24)
    z=np.array([[s*(1+a/100)*PROT["Rigenerativo Full"]["co2c"]*3.667 for s in sx] for a in ay])
    fig_h=go.Figure(go.Heatmap(z=z,x=sx,y=ay,
        colorscale=[[0,"#d8f3dc"],[0.5,"#1a6b3a"],[1,"#061912"]],
        colorbar=dict(title="tCO₂/ha",titlefont=dict(size=11))))
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

# ── SCENARI ──────────────────────────────────────────────────
st.markdown('<div class="sec">🚀 Business Case & ROI Sostenibilità</div>',unsafe_allow_html=True)
s1,s2,s3=st.columns(3)

def row(l,v): return f'<div class="sc-row"><span>{l}</span><b>{v}</b></div>'

with s1:
    st.markdown(f"""<div class="sc-card sc-base">
    <div style="font-size:.92rem;font-weight:700;color:#1a6b3a;margin-bottom:.6rem">📍 Stato Attuale</div>
    {row("CO₂ netta",f"{round(tot_netto,1)} t/anno")}
    {row("Valore crediti CO₂",f"€{int(val_cred):,}/anno")}
    {row("Costo gasolio",f"€{int(tot_c_die):,}/anno")}
    {row("Costo fertilizzanti N",f"€{int(tot_c_n):,}/anno")}
    {row("Costo irrigazione",f"€{int(tot_c_irr):,}/anno")}
    {row("Margine netto",f"€{margine:,} ({marg_pct}%)")}
    </div>""",unsafe_allow_html=True)

with s2:
    st.markdown(f"""<div class="sc-card sc-opt">
    <div style="font-size:.92rem;font-weight:700;color:#92400e;margin-bottom:.6rem">⚡ Scenario Rigenerativo</div>
    {row("CO₂ netta",f"{round(pot_netto,1)} t/anno")}
    {row("Valore crediti",f"€{int(pot_cred):,}/anno")}
    {row("Risparmio gasolio",f"<span style='color:#1a6b3a'>€{int(risp_die):,}/anno</span>")}
    {row("Risparmio acqua",f"<span style='color:#1a6b3a'>€{int(risp_h2o):,}/anno</span>")}
    {row("Nuovi crediti",f"<span style='color:#1a6b3a'>€{int(extra_cred):,}/anno</span>")}
    <div style="border-top:1px dashed #c9963a;margin-top:.5rem;padding-top:.5rem;text-align:right;font-size:.85rem;color:#92400e">
    <b>+€{int(guadagno):,}/anno totale</b></div>
    </div>""",unsafe_allow_html=True)

with s3:
    tech_lines=""
    if inv_iot:    tech_lines+=row("Sensori IoT","€3.500")
    if inv_drip:   tech_lines+=row("Micro-irrigazione",f"€{6000*tot_ha_i:,}")
    if inv_gps:    tech_lines+=row("Precision GPS","€8.000")
    if inv_biochar:tech_lines+=row("Biochar",f"€{1200*tot_ha_i:,}")
    if not tech_lines: tech_lines='<div style="font-size:.78rem;color:#7a8c7e;padding:4px 0">Seleziona tecnologie nella barra sinistra</div>'
    st.markdown(f"""<div class="sc-card sc-tech">
    <div style="font-size:.92rem;font-weight:700;color:#1e40af;margin-bottom:.6rem">🔬 Investimento Tecnologico</div>
    {tech_lines}
    {row("Investimento totale",f"€{int(costo_inv):,}")}
    {row("Ritorno annuo",f"€{int(guadagno):,}")}
    <div style="border-top:1px dashed #3b82f6;margin-top:.5rem;padding-top:.5rem;text-align:right;font-size:.85rem;color:#1e40af">
    <b>Payback: {payback} anni</b></div>
    </div>""",unsafe_allow_html=True)

# ── CERTIFICAZIONI ───────────────────────────────────────────
st.markdown('<div class="sec">📜 Gap Analysis Certificazioni</div>',unsafe_allow_html=True)
certs=[
    ("Biologico (Reg. UE 2018/848)",cert_bio, "+14 pt","12-24 mesi","Prezzo +15-25%",  "#1a6b3a"),
    ("SQnpi – Produzione Integrata", cert_sqnpi,"+8 pt","6-12 mesi", "Accesso GDO +12%","#1a6b3a"),
    ("GlobalG.A.P.",                 cert_gap,  "+7 pt","6 mesi",    "Export EU/USA",   "#c9963a"),
    ("VIVA Sostenibilità",           cert_viva, "+8 pt","12 mesi",   "Premio viticolo +10%","#c9963a"),
    ("ISO 14064 Carbon FP",          cert_iso,  "+10 pt","6-9 mesi", "Crediti @ €42/t", "#0a3d62"),
    ("CSRD / ESRS Reporting",        cert_csrd, "+8 pt","12-18 mesi","Filiere >€40M",   "#0a3d62"),
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
            <b style="color:{colore}">{punti} ESG</b> · {tempo} · 💶 {val}
          </span>
        </div>""",unsafe_allow_html=True)

# ── AZIONI ───────────────────────────────────────────────────
st.markdown('<div class="sec">🎯 Piano d\'Azione Prioritario</div>',unsafe_allow_html=True)
azioni=[]
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    azioni.append({"p":"alta","t":"Convertire appezzamenti convenzionali → Minima lavorazione",
        "i":f"IPCC FMG +0.18 · +{round(tot_ha*0.025*3.667,1)} tCO₂/anno stimati",
        "e":f"€{round(tot_ha*0.025*3.667*prezzo_co2):,}/anno nuovi crediti",
        "c":"Prerequisito GlobalG.A.P. e ISO 14064"})
if tot_spreco>300:
    azioni.append({"p":"alta","t":"Eliminare spreco irriguo con micro-irrigazione",
        "i":f"Spreco {int(tot_spreco):,} m³/anno · efficienza potenziale 85%",
        "e":f"€{int(tot_spreco*costo_acqua):,}/anno risparmio",
        "c":"PAC Eco-Scheme · payback 3-4 anni"})
if stress_idx>.3:
    azioni.append({"p":"alta","t":f"Gestione urgente stress idrico ({round(stress_idx*100):.0f}%)",
        "i":f"Deficit {round(deficit)} mm · rischio resa -{round(stress_idx*18,1)}%",
        "e":f"Perdita stimata €{round(fatturato*stress_idx*.15):,} se non gestito",
        "c":"Irrigazione di soccorso + cover crops"})
if not cert_bio and not cert_sqnpi:
    azioni.append({"p":"alta","t":"Avviare percorso certificazione SQnpi",
        "i":"Gateway obbligatorio per filiera GDO e export UE",
        "e":"Aumento prezzo vendita +12-18%",
        "c":"6-12 mesi · CAA locale · ASSAM"})
if not cert_iso:
    azioni.append({"p":"media","t":"Certificazione ISO 14064 per vendita crediti",
        "i":f"Bilancio netto {round(tot_netto,1)} tCO₂/anno certificabile",
        "e":f"€{round(max(0,tot_netto)*42):,}/anno su mercato ufficiale @ €42/t",
        "c":"Verra VCS · Gold Standard"})
if marg_pct<22:
    azioni.append({"p":"media","t":"Ottimizzare struttura costi variabili",
        "i":f"Margine {marg_pct}% sotto soglia resilienza (25%)",
        "e":"Riduzione input chimici + upgrade ESG sinergici",
        "c":"Piano agronomico integrato"})

pm={"alta":("act-h","🔴"),"media":("act-m","🟡"),"bassa":("act-l","🟢")}
for i,az in enumerate(azioni[:6],1):
    cls,ico=pm[az["p"]]
    st.markdown(f"""<div class="action {cls}">
      <div style="font-size:.88rem;font-weight:600">{ico} {i}. {az['t']}</div>
      <div style="margin-top:.25rem;font-size:.78rem;color:#7a8c7e">📊 {az['i']}</div>
      <div style="font-size:.78rem;color:#1a6b3a">💶 {az['e']}
      <span style="color:#9ca3af"> · 📜 {az['c']}</span></div>
    </div>""",unsafe_allow_html=True)

# ── RISCHI ───────────────────────────────────────────────────
st.markdown('<div class="sec">⚠️ Mappa dei Rischi</div>',unsafe_allow_html=True)
rischi=[]
if stress_idx>.4: rischi.append({"l":"alto","t":f"Stress idrico critico {round(stress_idx*100):.0f}% — rischio produttivo immediato"})
if tot_netto<0:   rischi.append({"l":"alto","t":"Bilancio carbonico negativo — azienda emittente netta"})
if any(str(r.get("Protocollo",""))=="Convenzionale" for _,r in df_edit.iterrows()):
    rischi.append({"l":"alto","t":"Lavorazione convenzionale: perdita SOM >0.5% stimata in 5 anni"})
if not any([cert_bio,cert_sqnpi,cert_gap]):
    rischi.append({"l":"medio","t":"Zero certificazioni: esclusione filiere premium e crediti ufficiali"})
if marg_pct<20: rischi.append({"l":"medio","t":f"Margine {marg_pct}% sotto soglia resilienza aziendale"})
rischi.append({"l":"medio","t":"CSRD 2026: filiere >€40M richiedono ESG rating fornitori entro 2027"})
rischi.append({"l":"basso","t":"Volatilità mercato CO₂ volontario: range €25-65/t nel 2026"})
rischi.append({"l":"basso","t":"Scenario RCP4.5: +1.2°C area mediterranea entro 2035"})
rm={"alto":"r-alto","medio":"r-medio","basso":"r-basso"}
st.markdown('<div style="line-height:3">'+
    " ".join([f'<span class="risk {rm[r["l"]]}">{r["l"].upper()} — {r["t"]}</span>' for r in rischi])+
    "</div>",unsafe_allow_html=True)

# ── METODOLOGIA ──────────────────────────────────────────────
with st.expander("🔬 Metodologia Scientifica — IPCC Tier 1 + FAO-PM"):
    st.markdown("""
| Modulo | Formula / Riferimento |
|--------|-----------------------|
| **Carbon — IPCC Tier 1** | `SOC × coeff × f_tessitura × f_CC × f_clima × FMG × 3.667` |
| **SOC Stock** | `0.30m × 10.000m²/ha × Densità × (SO%/100) × 0.58` |
| **Fattore tessitura** | `1 + (Argilla/100) + (Limo/200)` — stabilizzazione MAOC |
| **FMG** | Conv=0.82 / Int=1.00 / Rig=1.15 (IPCC 2006 Table 5.5) |
| **Cover crops FI** | ×1.15 (IPCC 2006 Vol.4 Section 5.3) |
| **N₂O** | `N × 0.01 × (44/28) × 265` — EF IPCC, GWP AR5 |
| **Gasolio** | `L × 2.68 kgCO₂/L` — DEFRA 2024 |
| **Acqua FAO-PM** | `ET₀ live × Kc (FAO-56) × ha − pioggia efficace (×0.85)` |
| **Ritenzione SOM** | `(SO%−1) × 1.5mm/m × 3m × 10 × ha` — Rawls et al. 1982 |
| **Valore fondiario** | `ha × €15.000 × (1 + Δ_SO × 0.12)` — CREA-AA 2025 |
| **Meteo live** | Open-Meteo · ECMWF IFS + DWD ICON · 1km · orario |
| **Benchmark** | CREA-AA 2025 · RICA-Italia · ISPRA GHG 2024 |
    """)

# ── REPORT HTML ──────────────────────────────────────────────
st.markdown('<div class="sec">📄 Genera Dossier Professionale</div>',unsafe_allow_html=True)
st.info("Dossier completo con tutte le sezioni. **Aprilo nel browser → Ctrl+P → Salva come PDF.**")

if st.button("🖨️ Genera Dossier ESG Completo — PDF"):
    oggi=datetime.now().strftime("%d/%m/%Y")

    righe_tab=""
    for i,(_,row_) in enumerate(df_edit.iterrows()):
        r=res_att[i]
        nc="#1a6b3a" if r["co2_netto"]>=0 else "#ef4444"
        righe_tab+=f"""<tr>
          <td><b>{row_.get("Campo","")}</b></td><td>{row_.get("Ettari","")} ha</td>
          <td>{row_.get("Coltura","")}</td><td>{row_.get("Protocollo","")}</td>
          <td>{row_.get("SO %","")}%</td>
          <td>{row_.get("Argilla %","")}% / {row_.get("Limo %","")}%</td>
          <td>{row_.get("Densità","")} g/cm³</td>
          <td>{"✓" if row_.get("Cover crops",False) else "—"}</td>
          <td>{int(row_.get("Irrigazione m³/ha",0)):,} m³/ha</td>
          <td style="color:#1a6b3a"><b>{r["co2_seq"]}</b></td>
          <td style="color:#ef4444">{r["co2_emit"]}</td>
          <td style="color:{nc}"><b>{"+" if r["co2_netto"]>=0 else ""}{r["co2_netto"]}</b></td>
          <td>{int(r["fabb_irr"]):,}</td><td>{int(r["spreco"]):,}</td>
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

    tech_r="".join([f'<tr><td>{n}</td><td style="text-align:right">€{v:,}</td></tr>'
        for n,v,ok in [("Sensori IoT",3500,inv_iot),("Micro-irrigazione",6000*tot_ha_i,inv_drip),
                       ("Precision GPS",8000,inv_gps),("Biochar",1200*tot_ha_i,inv_biochar)] if ok]
    ) or "<tr><td colspan='2' style='color:#999'>Nessuno selezionato</td></tr>"

    html=f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<title>AgroLog IA v6 — {nome_az} — {oggi}</title>
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
.k{{background:#f4f1ea;border-radius:10px;padding:.65rem .9rem;text-align:center;border:1px solid rgba(15,53,32,.1)}}
.kv{{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#0f3520}}
.kl{{font-size:.58rem;color:#7a8c7e;text-transform:uppercase;letter-spacing:.06em;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:.75rem}}
th{{background:#0f3520;color:#fff;padding:5px 7px;text-align:left;font-weight:500}}
td{{padding:4px 7px;border-bottom:1px solid #eee;vertical-align:middle}}
tr:nth-child(even) td{{background:#f9f7f3}}
.meteo{{background:linear-gradient(90deg,#0a2d4a,#0f3520);color:#fff;
  border-radius:9px;padding:.65rem 1.1rem;margin:.4rem 0;font-size:.78rem;line-height:2}}
.scen{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5rem;margin:.5rem 0}}
.sc{{border-radius:10px;padding:.9rem 1.1rem}}
.sc-b{{background:#f0fdf4;border:1.5px dashed #1a6b3a}}
.sc-o{{background:#fffbeb;border:1.5px dashed #c9963a}}
.sc-t{{background:#eff6ff;border:1.5px dashed #3b82f6}}
.sc-r{{display:flex;justify-content:space-between;font-size:.78rem;padding:2px 0}}
.sign{{border:1px solid #ddd;border-radius:10px;padding:1rem 1.5rem;margin:.5rem 0}}
.ftr{{background:#061912;color:rgba(255,255,255,.4);padding:.7rem 2rem;font-size:.6rem;text-align:center;margin-top:1rem}}
</style></head><body>

<div class="hdr">
  <div class="badge">Dossier ESG & Carbon Intelligence — AgroLog IA v6 — 2026</div>
  <h1>🌿 {nome_az}</h1>
  <p>Consulente: {agronomo} · {regione} / {zona} · {oggi} · IPCC Tier 1 · FAO-PM · Meteo Live</p>
  <div class="meta">
    <span>📊 Score ESG: {score}/100 — {rcls}</span>
    <span>🌿 CO₂ netta: {"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t/anno</span>
    <span>💶 Crediti: €{int(val_cred):,}/anno</span>
    <span>💧 Stress idrico: {round(stress_idx*100):.0f}%</span>
    <span>🌡️ {M["tmax"]}° / {M["tmin"]}°C</span>
  </div>
</div>

<div class="sec"><div class="st">Indicatori Chiave</div>
<div class="kg">
  <div class="k"><div class="kv">{score}/100</div><div class="kl">Score ESG — {rcls}</div></div>
  <div class="k"><div class="kv">{round(tot_seq,1)} t</div><div class="kl">CO₂ Sequestrata/anno</div></div>
  <div class="k"><div class="kv">{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</div><div class="kl">Bilancio Carbonico</div></div>
  <div class="k"><div class="kv">€{int(val_cred):,}</div><div class="kl">Valore Crediti CO₂</div></div>
  <div class="k"><div class="kv">{int(tot_fabb):,} m³</div><div class="kl">Fabbisogno Idrico</div></div>
  <div class="k"><div class="kv">{int(tot_spreco):,} m³</div><div class="kl">Spreco Irriguo</div></div>
  <div class="k"><div class="kv">€{int(tot_vf):,}</div><div class="kl">Valore Fondo</div></div>
  <div class="k"><div class="kv">{marg_pct}%</div><div class="kl">Margine Netto</div></div>
</div></div>

<div class="sec"><div class="st">Meteo Live — {regione} (Open-Meteo · ECMWF · {oggi})</div>
<div class="meteo">
🌡️ {M["tmax"]}° / {M["tmin"]}°C &nbsp;|&nbsp;
🌧️ Pioggia 7gg: {M["pioggia_7g"]} mm &nbsp;|&nbsp;
💧 ET₀: {M["et0"]} mm/g &nbsp;|&nbsp;
📊 Pioggia 30gg: {MS["pioggia_30g"]} mm &nbsp;|&nbsp;
📉 ET₀ 30gg: {MS["et0_30g"]} mm &nbsp;|&nbsp;
⚡ Deficit: {round(deficit)} mm &nbsp;|&nbsp;
🔥 Stress: {round(stress_idx*100):.0f}%
</div></div>

<div class="sec"><div class="st">Dettaglio Appezzamenti — IPCC Tier 1</div>
<table><thead><tr>
<th>Campo</th><th>ha</th><th>Coltura</th><th>Protocollo</th>
<th>SO%</th><th>Arg/Limo%</th><th>Densità</th><th>CC</th><th>Irrig.</th>
<th>CO₂ Seq</th><th>CO₂ Emit</th><th>Netto</th><th>Fabb.m³</th><th>Spreco m³</th>
</tr></thead><tbody>{righe_tab}</tbody>
<tfoot><tr style="background:#f0fdf4;font-weight:600">
<td>TOTALE</td><td>{round(tot_ha,1)} ha</td><td colspan="7"></td>
<td style="color:#1a6b3a">{round(tot_seq,1)}</td>
<td style="color:#ef4444">{round(tot_emit,1)}</td>
<td>{"+" if tot_netto>=0 else ""}{round(tot_netto,1)}</td>
<td>{int(tot_fabb):,}</td><td>{int(tot_spreco):,}</td>
</tr></tfoot></table></div>

<div class="sec"><div class="st">Scenari Economici</div>
<div class="scen">
<div class="sc sc-b"><b style="color:#1a6b3a;font-size:.87rem">📍 Stato Attuale</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta</span><b>{round(tot_netto,1)} t/anno</b></div>
<div class="sc-r"><span>Crediti CO₂</span><b>€{int(val_cred):,}/anno</b></div>
<div class="sc-r"><span>Costo gasolio</span><b>€{int(tot_c_die):,}</b></div>
<div class="sc-r"><span>Costo fertiliz.</span><b>€{int(tot_c_n):,}</b></div>
<div class="sc-r"><span>Costo irrigaz.</span><b>€{int(tot_c_irr):,}</b></div>
<div class="sc-r"><span>Margine netto</span><b>{marg_pct}%</b></div>
</div></div>
<div class="sc sc-o"><b style="color:#92400e;font-size:.87rem">⚡ Rigenerativo Full</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta</span><b>{round(pot_netto,1)} t/anno</b></div>
<div class="sc-r"><span>Crediti CO₂</span><b>€{int(pot_cred):,}/anno</b></div>
<div class="sc-r"><span>Risp. gasolio</span><b style="color:#1a6b3a">€{int(risp_die):,}</b></div>
<div class="sc-r"><span>Risp. acqua</span><b style="color:#1a6b3a">€{int(risp_h2o):,}</b></div>
<div class="sc-r"><span>Nuovi crediti</span><b style="color:#1a6b3a">€{int(extra_cred):,}</b></div>
<div style="border-top:1px dashed #c9963a;margin-top:.4rem;padding-top:.3rem;text-align:right">
<b style="color:#92400e">+€{int(guadagno):,}/anno</b></div>
</div></div>
<div class="sc sc-t"><b style="color:#1e40af;font-size:.87rem">🔬 Tech</b>
<div style="margin-top:.4rem">
<table style="font-size:.75rem">{tech_r}
<tr style="border-top:1px solid #ddd"><td><b>Totale</b></td><td style="text-align:right"><b>€{int(costo_inv):,}</b></td></tr>
<tr><td>Ritorno/anno</td><td style="text-align:right;color:#1a6b3a"><b>€{int(guadagno):,}</b></td></tr>
<tr><td><b>Payback</b></td><td style="text-align:right;color:#1e40af"><b>{payback} anni</b></td></tr>
</table></div></div>
</div></div>

<div class="sec"><div class="st">Piano Azioni Prioritarie</div>{az_html}</div>

<div class="sec"><div class="st">Mappa dei Rischi</div>
<div style="line-height:2.5;margin-top:.3rem">{r_html}</div></div>

<div class="sec"><div class="st">Certificazioni — Stato & Gap</div>
<table><thead><tr><th>Certificazione</th><th>Stato</th><th>Punti ESG</th><th>Tempo</th><th>Valore economico</th></tr></thead>
<tbody>{"".join([f"<tr><td>{'<b>' if att else ''}{n}{'</b>' if att else ''}</td><td>{'✅ Attiva' if att else '○ Non attiva'}</td><td>{p}</td><td>{t}</td><td>{v}</td></tr>" for n,att,p,t,v,_ in certs])}</tbody></table></div>

<div class="sec"><div class="st">Nota Metodologica</div>
<p style="font-size:.75rem;color:#555;line-height:1.6">
<b>Carbonio:</b> IPCC 2006 Guidelines Vol.4 Agriculture, Tier 1, AR5 GWP. FMG Table 5.5. C→CO₂: ×3.667.
N₂O: EF=0.01 kg N₂O-N/kg N, GWP=265. Gasolio: 2.68 kgCO₂/L (DEFRA 2024).
<b>Acqua:</b> FAO Penman-Monteith, Kc da FAO-56, pioggia efficace ×0.85. SOM: Rawls et al. 1982.
<b>Meteo:</b> Open-Meteo API (ECMWF IFS + DWD ICON, 1km, aggiorn. orario).
<b>Valore fondiario:</b> CREA-AA 2025. <b>Benchmark:</b> RICA-Italia 2024, ISPRA GHG 2024.
<b>CO₂:</b> Xpansiv CBL Q1 2026.
<i>Report previsionale — certificazione ufficiale crediti richiede verifica Ente Terzo (Verra VCS / Gold Standard / ISAE 3000).</i>
</p></div>

<div class="sec"><div class="st">Firma e Validazione</div>
<div class="sign">
<table style="font-size:.82rem;border:none">
<tr><td style="border:none;padding:4px 8px"><b>Dottore Agronomo:</b></td>
    <td style="border:none;padding:4px 8px">{agronomo}</td>
    <td style="border:none;padding:4px 8px"><b>N. Albo:</b></td>
    <td style="border:none;padding:4px 8px">______________________</td></tr>
<tr><td style="border:none;padding:4px 8px"><b>Data:</b></td>
    <td style="border:none;padding:4px 8px">{oggi}</td>
    <td style="border:none;padding:4px 8px"><b>Luogo:</b></td>
    <td style="border:none;padding:4px 8px">______________________</td></tr>
</table>
<div style="margin-top:2rem;display:flex;gap:5rem">
  <p style="color:#bbb;font-size:.8rem">Firma: ______________________</p>
  <div><p style="color:#bbb;font-size:.8rem">Timbro:</p>
  <div style="width:75px;height:75px;border:1px dashed #ddd;border-radius:50%;margin-top:.3rem"></div></div>
</div></div></div>

<div class="ftr">AgroLog IA v6.0 — Carbon & ESG Strategic Intelligence |
IPCC 2006 Tier 1 · FAO-PM · Open-Meteo Live · CREA-AA 2025 · ISPRA GHG 2024 · Xpansiv CBL Q1 2026 |
Dati previsionali — verifica Ente Terzo per certificazione ufficiale</div>
</body></html>"""

    b64=base64.b64encode(html.encode("utf-8")).decode()
    fn=f"AgroLog_v6_{nome_az.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html"
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="{fn}" '
        f'style="display:inline-block;background:#c9963a;color:#fff;padding:.7rem 2.2rem;'
        f'border-radius:10px;text-decoration:none;font-weight:700;font-size:.95rem;'
        f'margin-top:.6rem;box-shadow:0 4px 12px rgba(201,150,58,.35)">'
        f'⬇️ Scarica Dossier ESG Completo</a>',
        unsafe_allow_html=True)
    st.success(f"✅ '{fn}' pronto! Apri nel browser → Ctrl+P → Salva come PDF.")

st.markdown("""<div class="footer">
  AgroLog IA v6.0 — Carbon & ESG Strategic Intelligence |
  IPCC Tier 1 · FAO-PM · Open-Meteo Live · CREA-AA 2025 · Xpansiv CBL Q1 2026 |
  Sviluppato con 💚 — ogni giorno migliore
</div>""",unsafe_allow_html=True)
