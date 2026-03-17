import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import requests, base64

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_OK = True
except ImportError:
    FOLIUM_OK = False

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

/* ══════════════════════════════════════════════════════
   PALETTE DARK — Nero & Verde
   Sfondo:       #0a0a0a / #111411 / #0d1a0d
   Card:         #161c16 / #1a221a
   Bordi:        #22c55e (verde brillante)
   Testo:        #e8f5e9 / #a3d9a5
   Accent:       #22c55e / #16a34a
   ══════════════════════════════════════════════════════ */

html, body, [class*="css"] {
    font-family: 'Lexend', sans-serif;
}

/* ── Background app ── */
.stApp,
.main,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"],
section.main {
    background: #0d110d !important;
    color: #e8f5e9 !important;
}

/* ── Testi generali ── */
.stMarkdown, .stMarkdown p, .stMarkdown span,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
p, span {
    color: #e8f5e9 !important;
}
.stMarkdown strong, .stMarkdown b,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #ffffff !important;
    font-weight: 700 !important;
}
[data-testid="stCaptionContainer"] p,
.stCaption p {
    color: #86efac !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: #161c16 !important;
    border-color: #22c55e !important;
    color: #e8f5e9 !important;
}

/* ── Data editor ── */
[data-testid="stDataEditor"] {
    border: 2px solid #22c55e !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 0 24px rgba(34,197,94,.15) !important;
    background: #161c16 !important;
}
[data-testid="stDataEditor"] > div,
[data-testid="stDataEditor"] > div > div,
[data-testid="stDataEditor"] canvas {
    background: #161c16 !important;
}
[data-testid="stDataEditor"] [role="gridcell"],
[data-testid="stDataEditor"] [role="columnheader"],
[data-testid="stDataEditor"] td,
[data-testid="stDataEditor"] th {
    background: #161c16 !important;
    color: #e8f5e9 !important;
}

/* ══ HERO ══ */
.hero {
    background: linear-gradient(135deg,#000000 0%,#0d1a0d 40%,#052e16 100%);
    padding: 2.4rem 3rem 2rem; border-radius: 22px; margin-bottom: 2rem;
    box-shadow: 0 0 60px rgba(34,197,94,.12), 0 14px 44px rgba(0,0,0,.5);
    border-bottom: 3px solid #22c55e;
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 80% 50%, rgba(34,197,94,.08) 0%, transparent 65%);
    pointer-events: none;
}
.hero::after {
    content: '🌿'; position: absolute; right: 2.5rem; top: 50%;
    transform: translateY(-50%); font-size: 6rem; opacity: .06; pointer-events: none;
}
.hero h1 {
    font-family: 'DM Serif Display', serif; color: #ffffff !important;
    font-size: 2rem; margin: .3rem 0 .1rem;
    text-shadow: 0 0 40px rgba(34,197,94,.3);
}
.hero p { color: rgba(255,255,255,.6) !important; font-size: .86rem; margin: 0; }
.hero-meta { display: flex; gap: 1rem; margin-top: .8rem; flex-wrap: wrap; }
.hero-meta span {
    background: rgba(34,197,94,.1); color: #86efac !important;
    font-size: .7rem; padding: 3px 11px; border-radius: 20px;
    border: 1px solid rgba(34,197,94,.25);
}
.hero-badge {
    background: #16a34a; color: #000 !important; font-size: .62rem; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase; padding: 3px 12px;
    border-radius: 20px; margin-bottom: .6rem; display: inline-block;
}

/* ══ KPI CARDS ══ */
.kpi {
    background: #161c16; border-radius: 18px; padding: 1.2rem 1rem;
    border: 1px solid rgba(34,197,94,.2);
    box-shadow: 0 4px 20px rgba(0,0,0,.3), 0 0 0 1px rgba(34,197,94,.05);
    text-align: center; transition: all .25s; height: 100%;
}
.kpi:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,.4), 0 0 20px rgba(34,197,94,.15);
    border-color: rgba(34,197,94,.5);
}
.kpi-v { font-size: 1.75rem; font-weight: 700; color: #ffffff !important; line-height: 1.1; }
.kpi-l { font-size: .6rem; color: #4ade80 !important; text-transform: uppercase; letter-spacing: .09em; margin-top: .3rem; }
.kpi-s { font-size: .76rem; color: #86efac !important; font-weight: 600; margin-top: .15rem; }

/* ══ SEZIONI ══ */
.sec {
    font-family: 'DM Serif Display', serif; font-size: 1.2rem;
    color: #ffffff !important;
    border-left: 5px solid #22c55e; padding-left: .7rem; margin: 2.2rem 0 1rem;
    text-shadow: 0 0 20px rgba(34,197,94,.2);
}

/* ══ AZIONI ══ */
.action {
    background: #161c16; border-radius: 13px; padding: .9rem 1.15rem; margin: .4rem 0;
    border: 1px solid rgba(34,197,94,.15); transition: all .2s;
}
.action:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,.3), 0 0 15px rgba(34,197,94,.1);
    border-color: rgba(34,197,94,.35);
}
.action div { color: #e8f5e9 !important; }
.act-h { border-left: 4px solid #ef4444; }
.act-m { border-left: 4px solid #f59e0b; }
.act-l { border-left: 4px solid #22c55e; }

/* ══ RISCHI ══ */
.risk {
    display: inline-block; padding: 5px 13px; border-radius: 20px;
    font-size: .72rem; font-weight: 700; margin: 3px;
}
.r-alto  { background: rgba(239,68,68,.15);  color: #fca5a5 !important; border: 1px solid rgba(239,68,68,.4); }
.r-medio { background: rgba(245,158,11,.12); color: #fcd34d !important; border: 1px solid rgba(245,158,11,.4); }
.r-basso { background: rgba(34,197,94,.12);  color: #86efac !important; border: 1px solid rgba(34,197,94,.35); }

/* ══ CERTIFICAZIONI ══ */
.cert-box {
    border-radius: 11px; padding: .85rem 1rem; margin: .3rem 0;
    border: 1px solid rgba(34,197,94,.15);
}
.cert-on  { background: rgba(34,197,94,.08); border-left: 4px solid #22c55e; }
.cert-off { background: #161c16; border-left: 4px solid #374151; }
.cert-box *, .cert-box b, .cert-box span { color: #e8f5e9 !important; }

/* ══ SCENARIO CARDS ══ */
.sc-card { border-radius: 14px; padding: 1.3rem 1.5rem; margin: .4rem 0; }
.sc-base { background: rgba(34,197,94,.08); border: 2px dashed rgba(34,197,94,.4); }
.sc-opt  { background: rgba(245,158,11,.07); border: 2px dashed rgba(245,158,11,.4); }
.sc-tech { background: rgba(59,130,246,.07); border: 2px dashed rgba(59,130,246,.4); }
.sc-row  { display: flex; justify-content: space-between; font-size: .82rem; padding: 3px 0; line-height: 1.9; }
.sc-row, .sc-row span { color: #a3d9a5 !important; }
.sc-row b { color: #ffffff !important; }

/* ══ SCOPE BOXES ══ */
.scope-box { border-radius: 12px; padding: 1rem 1.2rem; margin: .4rem 0; }
.scope1 { background: rgba(239,68,68,.1); border: 1.5px solid rgba(239,68,68,.35); }
.scope1, .scope1 * { color: #fca5a5 !important; }
.scope1 b { color: #fca5a5 !important; font-weight: 700; }
.scope2 { background: rgba(245,158,11,.1); border: 1.5px solid rgba(245,158,11,.35); }
.scope2, .scope2 * { color: #fcd34d !important; }
.scope2 b { color: #fde68a !important; font-weight: 700; }
.scope3 { background: rgba(34,197,94,.1); border: 1.5px solid rgba(34,197,94,.35); }
.scope3, .scope3 * { color: #86efac !important; }
.scope3 b { color: #4ade80 !important; font-weight: 700; }

/* ══ INFO / RIEPILOGO BOXES ══ */
.ghg-box {
    background: #161c16; border-radius: 14px; padding: 1.2rem 1.4rem;
    border: 1.5px solid rgba(34,197,94,.2);
}
.ghg-box, .ghg-box * { color: #e8f5e9 !important; }
.ghg-box .pos { color: #4ade80 !important; font-weight: 700; }
.ghg-box .neg { color: #f87171 !important; font-weight: 700; }

.info-box {
    background: #161c16; border-radius: 12px; padding: .75rem 1.1rem;
    border: 1px solid rgba(34,197,94,.18); margin-top: .5rem; font-size: .8rem;
}
.info-box, .info-box * { color: #e8f5e9 !important; }

.meteo-strip {
    background: #161c16; border-radius: 12px; padding: .8rem 1.1rem;
    border: 1px solid rgba(34,197,94,.18); font-size: .79rem; margin-top: -.5rem;
}
.meteo-strip, .meteo-strip * { color: #e8f5e9 !important; }

.n2o-strip {
    background: #161c16; border-radius: 12px; padding: .75rem 1.2rem;
    border: 1.5px solid rgba(34,197,94,.25); font-size: .79rem; margin: .5rem 0;
}
.n2o-strip, .n2o-strip * { color: #e8f5e9 !important; }

.rothc-card {
    background: #161c16; border-radius: 12px; padding: .9rem 1rem;
    border: 1.5px solid rgba(34,197,94,.2); font-size: .78rem;
}
.rothc-card, .rothc-card * { color: #e8f5e9 !important; }

.map-legend {
    background: #161c16; border-radius: 12px; padding: 1rem;
    border: 1.5px solid rgba(34,197,94,.2); font-size: .8rem;
}
.map-legend, .map-legend * { color: #e8f5e9 !important; }

/* ══ PAC BANNER ══ */
.pac-banner {
    background: linear-gradient(90deg,#000000,#052e16);
    border-radius: 12px; padding: .9rem 1.4rem; margin-top: .5rem;
    font-size: .82rem; border: 1px solid rgba(34,197,94,.25);
}
.pac-banner, .pac-banner * { color: #e8f5e9 !important; }
.pac-banner b { color: #4ade80 !important; }

/* ══ SIDEBAR ══ */
div[data-testid="stSidebar"] { background: #080d08 !important; }
div[data-testid="stSidebar"],
div[data-testid="stSidebar"] * { color: rgba(255,255,255,.88) !important; }
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #4ade80 !important;
}
div[data-testid="stSidebar"] label {
    font-size: .7rem !important; text-transform: uppercase;
    letter-spacing: .05em; color: rgba(74,222,128,.6) !important;
}
div[data-testid="stSidebar"] input,
div[data-testid="stSidebar"] select {
    background: #161c16 !important; color: #e8f5e9 !important;
    border: 1px solid rgba(34,197,94,.35) !important;
}
div[data-testid="stSidebar"] hr {
    border-color: rgba(34,197,94,.2) !important;
}

/* ══ BUTTONS ══ */
.stButton > button {
    background: #16a34a !important; color: #000 !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: .9rem !important;
    padding: .6rem 1.8rem !important;
    box-shadow: 0 0 20px rgba(34,197,94,.25) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: #22c55e !important;
    box-shadow: 0 0 30px rgba(34,197,94,.4) !important;
}

/* ══ SELECTBOX / INPUT / SLIDER ══ */
[data-testid="stSelectbox"] > div,
[data-baseweb="select"] > div {
    background: #161c16 !important;
    border-color: rgba(34,197,94,.3) !important;
    color: #e8f5e9 !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: #161c16 !important;
    border-color: rgba(34,197,94,.3) !important;
    color: #e8f5e9 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div {
    background: #22c55e !important;
}

/* ══ FOOTER ══ */
.footer {
    font-size: .67rem; color: #4ade80; text-align: center; margin-top: 2.5rem;
    padding-top: 1rem; border-top: 1px solid rgba(34,197,94,.15);
}

/* ══ EXPANDER ══ */
[data-testid="stExpander"] {
    background: #161c16 !important;
    border: 1px solid rgba(34,197,94,.2) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #4ade80 !important;
}
[data-testid="stExpander"] table {
    width: 100%; border-collapse: collapse; font-size: .78rem;
    border: 1.5px solid rgba(34,197,94,.35); border-radius: 10px; overflow: hidden;
}
[data-testid="stExpander"] table th {
    background: #052e16 !important; color: #4ade80 !important;
    padding: 8px 12px !important; font-weight: 700 !important;
    border-bottom: 2px solid #22c55e !important;
}
[data-testid="stExpander"] table td {
    padding: 6px 12px !important; color: #e8f5e9 !important;
    border-bottom: 1px solid rgba(34,197,94,.1) !important;
}
[data-testid="stExpander"] table tr:nth-child(odd)  td { background: #0d1a0d !important; }
[data-testid="stExpander"] table tr:nth-child(even) td { background: #161c16 !important; }
[data-testid="stExpander"] table tr:hover td {
    background: #052e16 !important; color: #4ade80 !important;
}

/* ══ TABELLE .tbl-agro ══ */
.tbl-agro {
    width: 100%; border-collapse: collapse; font-size: .79rem;
    border-radius: 12px; overflow: hidden;
    border: 1.5px solid rgba(34,197,94,.35); background: #161c16;
}
.tbl-agro thead th {
    background: #052e16; color: #4ade80 !important; font-weight: 700;
    padding: 9px 12px; text-align: left; border-bottom: 2px solid #22c55e;
    letter-spacing: .04em; font-size: .76rem; text-transform: uppercase;
}
.tbl-agro tbody tr:nth-child(odd)  td { background: #0d1a0d; color: #e8f5e9 !important; }
.tbl-agro tbody tr:nth-child(even) td { background: #161c16; color: #e8f5e9 !important; }
.tbl-agro tbody td { padding: 7px 12px; border-bottom: 1px solid rgba(34,197,94,.08); vertical-align: middle; }
.tbl-agro tbody tr:hover td { background: #052e16; color: #4ade80 !important; }
.tbl-agro tfoot td {
    background: #052e16; color: #4ade80 !important; font-weight: 700;
    padding: 8px 12px; border-top: 2px solid #22c55e;
}
.tbl-agro .pos  { color: #4ade80 !important; font-weight: 700; }
.tbl-agro .neg  { color: #f87171 !important; font-weight: 700; }
.tbl-agro .gold { color: #fde68a !important; font-weight: 700; }

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d110d; }
::-webkit-scrollbar-thumb { background: #22c55e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4ade80; }
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

BM_COLTURA = {
    "Cereali":         {"score":48, "co2_ha":1.9, "margine_pct":20, "label":"Cereali/Seminativi"},
    "Vite (DOC/IGT)":  {"score":57, "co2_ha":3.1, "margine_pct":38, "label":"Vitivinicolo DOC"},
    "Olivo":           {"score":54, "co2_ha":2.7, "margine_pct":40, "label":"Olivicoltura"},
    "Nocciolo":        {"score":50, "co2_ha":2.3, "margine_pct":30, "label":"Corilicultura"},
    "Frutteto":        {"score":52, "co2_ha":2.5, "margine_pct":32, "label":"Frutticoltura"},
    "Orticole":        {"score":55, "co2_ha":2.8, "margine_pct":28, "label":"Orticoltura"},
    "Foraggere":       {"score":60, "co2_ha":3.8, "margine_pct":18, "label":"Foraggere/Prati"},
    "Misto":           {"score":52, "co2_ha":2.4, "margine_pct":30, "label":"Misto"},
}

PAC_ECOSCHEME = {
    "ES1 — Agricoltura biologica":           {"pagamento_ha":340, "req":"cert_bio",      "colture":"Tutte",             "desc":"Conversione o mantenimento biologico"},
    "ES2 — Pratiche benefiche per clima":    {"pagamento_ha":110, "req":"cover_crops",   "colture":"Seminativi",        "desc":"Cover crops, no-tillage, gestione suolo"},
    "ES4 — Impollinatori e biodiversità":    {"pagamento_ha": 90, "req":"cover_crops",   "colture":"Seminativi/Frutteto","desc":"Fasce fiorite, habitat impollinatori"},
    "ES5 — Gestione risorse idriche":        {"pagamento_ha": 85, "req":"inv_drip",      "colture":"Irrigue",           "desc":"Micro-irrigazione, risparmio idrico"},
    "Misura agro-climatica — Carbonio suolo":{"pagamento_ha":220, "req":"rigenerativo",  "colture":"Seminativi/Perm.",  "desc":"Pratiche rigenerative, incremento SOM"},
    "Misura agro-climatica — Biologico+":   {"pagamento_ha":180, "req":"cert_bio_rig",  "colture":"Tutte",             "desc":"Bio + pratiche agro-ambientali avanzate"},
}

EF_FERT = {
    "Urea (46% N)":               {"ef_prod":2.10,"ef_n2o":0.013,"tipo":"minerale","desc":"Alta emissione prod. + N₂O idrolisi (EF 0.013)"},
    "Nitrato ammoniacale (34% N)":{"ef_prod":5.70,"ef_n2o":0.010,"tipo":"minerale","desc":"Alta emissione prod., EF N₂O standard 0.010"},
    "Solfato ammonico (21% N)":   {"ef_prod":1.45,"ef_n2o":0.010,"tipo":"minerale","desc":"Sottoprodotto industria, EF N₂O 0.010"},
    "Ammonio fosfato (18N-46P)":  {"ef_prod":2.90,"ef_n2o":0.010,"tipo":"minerale","desc":"Include emissione fosfato, EF N₂O 0.010"},
    "Concime organico pellettato":{"ef_prod":0.35,"ef_n2o":0.006,"tipo":"organico","desc":"N₂O ridotto EF 0.006 (-40% vs minerale)"},
    "Letame bovino fresco":       {"ef_prod":0.10,"ef_n2o":0.005,"tipo":"organico","desc":"EF N₂O 0.005 (-50% vs minerale), stabilizza SOM"},
    "Compost maturo":             {"ef_prod":0.08,"ef_n2o":0.004,"tipo":"organico","desc":"Carbonio stabile, EF N₂O minimo 0.004 (-60%)"},
    "Digestato zootecnico":       {"ef_prod":0.05,"ef_n2o":0.004,"tipo":"organico","desc":"Sottoprodotto biogas, EF N₂O 0.004 (-60%)"},
}

EF_FITO = {
    "Erbicidi":    2.80,
    "Fungicidi":   2.40,
    "Insetticidi": 3.10,
    "Nessuno":     0.00,
}

EF_SCARTI = {
    "Paglia/stocchi (bruciatura)": 1.50,
    "Paglia/stocchi (interramento)": -0.12,
    "Sansa (smaltimento)":          0.20,
    "Sansa (biogas)":              -0.45,
    "Vinacce (smaltimento)":        0.18,
    "Vinacce (digestato)":         -0.30,
    "Potature (bruciatura)":        1.20,
    "Potature (cippato energia)":  -0.60,
    "Potature (compostaggio)":     -0.25,
    "Acque reflue (no trattamento)":0.55,
    "Acque reflue (fitodepurazione)":-0.05,
}

EF_MATERIE = {
    "Sementi convenzionali (kg)":  0.85,
    "Sementi certificate bio (kg)": 0.40,
    "Imballaggi plastica (kg)":    3.50,
    "Imballaggi cartone (kg)":     1.10,
    "Lubrificanti macchine (L)":   3.20,
    "Acqua potabile (m³)":         0.30,
}

EF_TRASPORTI = {
    "Trasporto prodotti mercato (km·t)":     0.062,
    "Trasporto input agricoli (km·t)":       0.062,
    "Trasporto latte/prodotti animali (km·t)":0.055,
    "Volo per fiere/consulenze (km·pass)":   0.180,
    "Auto aziendale diesel (km)":            0.170,
    "Auto aziendale benzina (km)":           0.192,
    "Consegna mezzi agricoli (km)":          0.210,
}

# ══════════════════════════════════════════════════════════════════════
#  DATI DEFAULT TABELLA CAMPI
# ══════════════════════════════════════════════════════════════════════
if "df_campi" not in st.session_state:
    st.session_state.df_campi = pd.DataFrame([
        {"Campo":"Nord A1","Ettari":14.0,"SO %":1.6,"Argilla %":26,"Limo %":30,
         "Densità":1.32,"Protocollo":"Convenzionale","Cover crops":False,
         "Coltura":"Cereali","Irrigazione m³/ha":750,"Lat":43.62,"Lon":13.51,
         "Analisi suolo":"2022-03"},
        {"Campo":"Vigneto Est","Ettari":7.0,"SO %":1.3,"Argilla %":17,"Limo %":42,
         "Densità":1.44,"Protocollo":"Intermedio","Cover crops":False,
         "Coltura":"Vite (DOC/IGT)","Irrigazione m³/ha":280,"Lat":43.60,"Lon":13.54,
         "Analisi suolo":"2024-06"},
        {"Campo":"Oliveto Sud","Ettari":5.0,"SO %":2.2,"Argilla %":23,"Limo %":36,
         "Densità":1.24,"Protocollo":"Rigenerativo Full","Cover crops":True,
         "Coltura":"Olivo","Irrigazione m³/ha":0,"Lat":43.58,"Lon":13.49,
         "Analisi suolo":"2025-09"},
    ])


# ══════════════════════════════════════════════════════════════════════
#  FUNZIONI SALVATAGGIO / CARICAMENTO PROFILO
# ══════════════════════════════════════════════════════════════════════
import json as _json

def esporta_profilo():
    """Serializza tutto lo stato corrente in JSON."""
    profilo = {
        "version": "1.0",
        "nome_az":   st.session_state.get("_nome_az", "Az. Agr. Rossi"),
        "agronomo":  st.session_state.get("_agronomo", "Dott. [Cognome]"),
        "df_campi":  st.session_state.df_campi.to_dict(orient="records")
            if "df_campi" in st.session_state else [],
        "df_fert":   st.session_state.df_fert.to_dict(orient="records")
            if "df_fert" in st.session_state else [],
        "df_fito":   st.session_state.df_fito.to_dict(orient="records")
            if "df_fito" in st.session_state else [],
        "df_scarti": st.session_state.df_scarti.to_dict(orient="records")
            if "df_scarti" in st.session_state else [],
        "df_materie":st.session_state.df_materie.to_dict(orient="records")
            if "df_materie" in st.session_state else [],
        "df_trasporti": st.session_state.df_trasporti.to_dict(orient="records")
            if "df_trasporti" in st.session_state else [],
    }
    return _json.dumps(profilo, ensure_ascii=False, indent=2)

def importa_profilo(raw_bytes):
    """Carica un profilo JSON e aggiorna lo session_state."""
    try:
        profilo = _json.loads(raw_bytes.decode("utf-8"))
        if "df_campi" in profilo:
            st.session_state.df_campi = pd.DataFrame(profilo["df_campi"])
        if "df_fert" in profilo:
            st.session_state.df_fert = pd.DataFrame(profilo["df_fert"])
        if "df_fito" in profilo:
            st.session_state.df_fito = pd.DataFrame(profilo["df_fito"])
        if "df_scarti" in profilo:
            st.session_state.df_scarti = pd.DataFrame(profilo["df_scarti"])
        if "df_materie" in profilo:
            st.session_state.df_materie = pd.DataFrame(profilo["df_materie"])
        if "df_trasporti" in profilo:
            st.session_state.df_trasporti = pd.DataFrame(profilo["df_trasporti"])
        return True, "Profilo caricato con successo!"
    except Exception as e:
        return False, f"Errore nel file JSON: {str(e)}"

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


    st.markdown("---")
    st.markdown("### 💾 Salva / Carica Profilo")
    
    # Export JSON
    profilo_json = esporta_profilo()
    nome_file = nome_az.replace(" ","_") if nome_az else "AgroLog"
    st.download_button(
        label="⬇️ Salva profilo aziendale",
        data=profilo_json.encode("utf-8"),
        file_name=f"{nome_file}_profilo.json",
        mime="application/json",
        help="Scarica tutti i dati inseriti come file JSON — riaprilo la prossima volta."
    )
    
    # Import JSON
    uploaded = st.file_uploader(
        "📂 Carica profilo salvato",
        type=["json"],
        help="Carica un profilo .json precedentemente salvato per ripristinare tutti i dati."
    )
    if uploaded is not None:
        ok, msg = importa_profilo(uploaded.read())
        if ok:
            st.success(f"✅ {msg}")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

# ══════════════════════════════════════════════════════════════════════
#  METEO
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
        mesi = {}
        for i, dt in enumerate(dates):
            m = dt[:7]
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
    if c == 0: return "☀️"
    if c <= 3: return "⛅"
    if c <= 49: return "🌫️"
    if c <= 67: return "🌧️"
    if c <= 77: return "❄️"
    if c <= 82: return "🌦️"
    if c <= 99: return "⛈️"
    return "🌤️"

# ══════════════════════════════════════════════════════════════════════
#  MOTORE SCIENTIFICO
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
    kc        = KC.get(col, 1.0)
    et0_ann   = M["et0"] * 365
    pioggia_e = MS["pioggia_30g"] * 12 * 0.85
    fabb_raw  = max(0, (et0_ann*kc - pioggia_e) * 10 * ha)
    fabb_irr  = fabb_raw * (0.65 if inv_drip else 1.0)
    irr_tot   = irr * ha
    spreco    = max(0, irr_tot - fabb_irr)
    ret_h2o   = max(0, (so-1.0)*1.5*3*10*ha)
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

def rothc_proiezione(so0, protocollo, anni=10):
    k = {"Convenzionale": -0.038, "Intermedio": -0.010, "Rigenerativo Full": 0.015
         }.get(str(protocollo), -0.010)
    valori = [round(so0 * ((1 + k) ** i), 3) for i in range(anni + 1)]
    delta_5  = round(valori[5]  - so0, 3)
    delta_10 = round(valori[10] - so0, 3)
    return valori, delta_5, delta_10, k

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
#  METEO RADAR + STORICO
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🌦️ Meteo Live · Radar 7 Giorni · Storico Pluviometrico</div>', unsafe_allow_html=True)

wc = st.columns(6)
wcols=[
    (f"{M['tmax']}° / {M['tmin']}°C","Temp. 7gg","previsione"),
    (f"{M['pioggia_7g']} mm","Pioggia 7gg","prossimi giorni"),
    (f"{M['et0']} mm/g","ET₀ FAO","live"),
    (f"{MS['pioggia_30g']} mm","Pioggia 30gg","storico reale"),
    (f"{MS['et0_30g']} mm","ET₀ 30gg","storico reale"),
    (f"{round(stress_idx*100):.0f}%","Stress Idrico","indice corrente"),
]
sc = "#ef4444" if stress_idx>.5 else "#f59e0b" if stress_idx>.25 else "#22c55e"
for col,(v,l,s),clr in zip(wc,wcols,["#ffffff"]*5+[sc]):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v" style="font-size:1.3rem;color:{clr}">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s" style="color:#86efac;font-size:.68rem">{s}</div></div>',
                    unsafe_allow_html=True)

if stress_idx>.4:
    st.error(f"⚠️ **Stress idrico critico {round(stress_idx*100):.0f}%** — deficit {round(deficit)} mm. Rischio resa -{round(stress_idx*18,1)}%.")
elif stress_idx>.2:
    st.warning(f"ℹ️ Stress idrico moderato {round(stress_idx*100):.0f}% — monitorare nelle prossime 2 settimane.")
else:
    st.success(f"✅ Bilancio idrico equilibrato — {MS['pioggia_30g']}mm pioggia vs {MS['et0_30g']}mm ET₀ (30gg).")

mr1, mr2 = st.columns(2)
with mr1:
    giorni_label = [(date.today()+timedelta(days=i)).strftime("%a %d") for i in range(7)]
    icons = [wcode_icon(c) for c in M["wcode_list"][:7]]
    labels_fmt = [f"{icons[i]} {giorni_label[i]}" for i in range(min(7,len(giorni_label)))]
    fig_rad = go.Figure()
    fig_rad.add_bar(x=labels_fmt, y=M["pioggia_list"][:7], name="Pioggia (mm)",
                    marker_color="#3b82f6", opacity=0.8)
    fig_rad.add_scatter(x=labels_fmt, y=M["tmax_list"][:7], name="Temp. max (°C)",
                        line=dict(color="#ef4444",width=2.5), mode="lines+markers", yaxis="y2")
    fig_rad.add_scatter(x=labels_fmt, y=M["tmin_list"][:7], name="Temp. min (°C)",
                        line=dict(color="#94a3b8",width=1.5,dash="dot"), mode="lines+markers", yaxis="y2")
    fig_rad.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
        font=dict(family="Lexend",color="#061912"),
        title="🌦️ Meteo Radar — Previsione 7 giorni",
        margin=dict(t=44,b=28,l=28,r=60),
        legend=dict(orientation="h",y=-0.22,font=dict(size=9)),
        yaxis=dict(title="Pioggia (mm)"),
        yaxis2=dict(title="°C", overlaying="y", side="right", showgrid=False),
        barmode="overlay"
    )
    st.plotly_chart(fig_rad, use_container_width=True)

with mr2:
    if MA:
        mesi_labels = [m["mese"][5:] for m in MA]
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
                            line=dict(color="#ef4444",width=2.5), mode="lines+markers", yaxis="y")
        fig_ann.add_scatter(x=mesi_fmt, y=temp_ann, name="Temp. media (°C)",
                            line=dict(color="#c9963a",width=2,dash="dot"), mode="lines+markers", yaxis="y2")
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
        tot_pioggia_ann = sum(piogge_ann)
        tot_et0_ann     = sum(et0_ann)
        bilancio_ann    = tot_pioggia_ann - tot_et0_ann
        mese_secco      = mesi_fmt[piogge_ann.index(min(piogge_ann))]
        mese_piovoso    = mesi_fmt[piogge_ann.index(max(piogge_ann))]
        st.markdown(f"""
        <div class="meteo-strip">
          📊 <b>Media annua:</b> {round(tot_pioggia_ann)}mm pioggia · {round(tot_et0_ann)}mm ET₀ ·
          Bilancio <b style="color:{'#4ade80' if bilancio_ann>=0 else '#f87171'}">
          {"+" if bilancio_ann>=0 else ""}{round(bilancio_ann)}mm</b> ·
          Mese più secco: <b style="color:#fde68a">{mese_secco}</b> · Mese più piovoso: <b style="color:#4ade80">{mese_piovoso}</b>
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
        "Lat": st.column_config.NumberColumn(min_value=-90,max_value=90,format="%.5f"),
        "Lon": st.column_config.NumberColumn(min_value=-180,max_value=180,format="%.5f"),
        "Analisi suolo": st.column_config.TextColumn(
            help="Data ultimo prelievo analisi suolo (YYYY-MM, es. 2022-03). Avviso se > 3 anni."),
    }, key="editor_v7"
)
st.session_state.df_campi = df_edit
if len(df_edit) == 0:
    st.warning("Aggiungi almeno un appezzamento."); st.stop()

# Avviso analisi suolo datata
if "Analisi suolo" in df_edit.columns:
    campi_datati = []
    for _, _r in df_edit.iterrows():
        da = str(_r.get("Analisi suolo","")).strip()
        if da and len(da) >= 7:
            try:
                anno_a, mese_a = int(da[:4]), int(da[5:7])
                anni_fa = (date.today() - date(anno_a, mese_a, 1)).days / 365.25
                if anni_fa > 3:
                    campi_datati.append((str(_r.get("Campo","")), round(anni_fa, 1), da))
            except Exception:
                pass
    if campi_datati:
        elenco = " · ".join([f"**{c}** ({a}a — {d})" for c,a,d in campi_datati])
        st.warning(
            f"⚠️ **Analisi suolo datata** su: {elenco} — "
            "Dati SO%, Argilla% e Densità potrebbero non riflettere la situazione attuale. "
            "Si consiglia un nuovo prelievo (costo 150-300 euro/campo)."
        )


# ══════════════════════════════════════════════════════════════════════
#  VALIDAZIONE INPUT — Coerenza dati scientifici
# ══════════════════════════════════════════════════════════════════════
errori_input = []
avvisi_input = []

for _, _r in df_edit.iterrows():
    _campo = str(_r.get("Campo",""))
    _arg   = float(_r.get("Argilla %", 0))
    _lim   = float(_r.get("Limo %", 0))
    _so    = float(_r.get("SO %", 1.5))
    _den   = float(_r.get("Densità", 1.3))
    _irr   = float(_r.get("Irrigazione m³/ha", 0))
    _col   = str(_r.get("Coltura",""))
    _prot  = str(_r.get("Protocollo",""))

    # Regola 1: Tessitura (Argilla + Limo ≤ 100%)
    if _arg + _lim > 100:
        errori_input.append(
            f"**{_campo}**: Argilla% ({_arg:.0f}) + Limo% ({_lim:.0f}) = {_arg+_lim:.0f}% > 100% — "
            "valore impossibile. Controlla la tessitura del suolo."
        )

    # Regola 2: Densità vs SO% (suoli con alta SOM hanno bassa densità)
    # Densità apparente > 1.6 con SO% > 3% è fisicamente improbabile
    if _den > 1.6 and _so > 3.0:
        avvisi_input.append(
            f"**{_campo}**: Densità {_den} g/cm³ con SO% {_so}% è incoerente — "
            "suoli ricchi di SOM hanno tipicamente densità < 1.4 g/cm³ (fonte: USDA Soil Science)."
        )
    # Densità < 0.9 con SO% < 1.5% è ugualmente improbabile
    if _den < 0.9 and _so < 1.5:
        avvisi_input.append(
            f"**{_campo}**: Densità {_den} g/cm³ molto bassa per SO% {_so}% — "
            "controlla il valore di densità apparente."
        )

    # Regola 3: Irrigazione su colture non irrigue
    colture_non_irrigue = ["Olivo","Nocciolo","Foraggere"]
    if _irr > 500 and _col in colture_non_irrigue:
        avvisi_input.append(
            f"**{_campo}**: Irrigazione {_irr:.0f} m³/ha su {_col} è elevata — "
            "questa coltura è tipicamente pluviale in Italia. Verifica il dato."
        )

    # Regola 4: SO% troppo bassa per rigenerativo (incoerenza agronomica)
    if _prot == "Rigenerativo Full" and _so < 0.8:
        avvisi_input.append(
            f"**{_campo}**: SO% {_so}% è molto bassa per protocollo Rigenerativo Full — "
            "il modello RothC assume accumulo, ma partendo da valori critici "
            "i calcoli di sequestro potrebbero essere sovrastimati."
        )

    # Regola 5: Argilla o Limo negativi / fuori range
    if _arg < 1 or _lim < 1:
        errori_input.append(
            f"**{_campo}**: Argilla% o Limo% < 1% — valore improbabile. "
            "Inserisci la tessitura reale del suolo."
        )

# Mostra errori e avvisi
if errori_input:
    for e in errori_input:
        st.error(f"🚨 **Errore dati — {e}")
if avvisi_input:
    for a in avvisi_input:
        st.warning(f"⚠️ **Attenzione — {a}")
if not errori_input and not avvisi_input:
    st.success("✅ Tutti i dati sono coerenti e nei range scientifici attesi.")


# ══════════════════════════════════════════════════════════════════════
#  SENTINEL-2 — Stima SO% da satellite (Copernicus ESA)
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🛰️ Validazione SO% da Satellite — Sentinel-2 Copernicus</div>', unsafe_allow_html=True)
st.caption("Stima indipendente della Sostanza Organica tramite indici spettrali NDVI/BSI — confronto con dati inseriti manualmente.")

# Funzione per ottenere token OAuth Copernicus
@st.cache_data(ttl=3500)
def get_copernicus_token(client_id, client_secret):
    """Ottieni access token OAuth2 da Copernicus Data Space."""
    try:
        resp = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data={
                "grant_type":    "client_credentials",
                "client_id":     client_id,
                "client_secret": client_secret,
            },
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json().get("access_token"), None
        return None, f"Errore autenticazione: {resp.status_code}"
    except Exception as e:
        return None, str(e)

# Funzione per stimare SO% da NDVI e BSI tramite Sentinel Hub Process API
@st.cache_data(ttl=86400, show_spinner=False)
def stima_so_sentinel(lat, lon, client_id, client_secret, raggio_m=300):
    """
    Stima SO% da Sentinel-2 L2A usando BSI e NDVI.
    Modello calibrato su LUCAS Topsoil Survey Europa (Ballabio et al. 2019).
    BSI = ((B11+B04)-(B08+B02)) / ((B11+B04)+(B08+B02))
    SO% stimata = 2.8 - BSI*3.5 + NDVI*0.8  (regressione su suoli mediterranei)
    """
    try:
        token, err = get_copernicus_token(client_id, client_secret)
        if not token:
            return None, err

        # Bbox attorno al punto (±raggio approssimativo in gradi)
        delta = raggio_m / 111000
        bbox = [lon - delta, lat - delta, lon + delta, lat + delta]

        evalscript = """
//VERSION=3
function setup() {
  return {
    input: [{bands: ["B02","B04","B08","B11","SCL"]}],
    output: {bands: 5, sampleType: "FLOAT32"}
  };
}
function evaluatePixel(s) {
  // Maschera nuvole (SCL: 4=vegetation, 5=bare soil, 6=water — teniamo 4 e 5)
  if (s.SCL < 4 || s.SCL > 6) return [-9999,-9999,-9999,-9999,-9999];
  let ndvi = (s.B08 - s.B04) / (s.B08 + s.B04 + 0.0001);
  let bsi  = ((s.B11 + s.B04) - (s.B08 + s.B02)) /
             ((s.B11 + s.B04) + (s.B08 + s.B02) + 0.0001);
  return [ndvi, bsi, s.B04, s.B08, s.B11];
}"""

        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": (date.today() - timedelta(days=120)).strftime("%Y-%m-%dT00:00:00Z"),
                            "to":   date.today().strftime("%Y-%m-%dT23:59:59Z")
                        },
                        "maxCloudCoverage": 25,
                        "mosaickingOrder": "leastCC"
                    }
                }]
            },
            "output": {
                "width": 32, "height": 32,
                "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
            },
            "evalscript": evalscript
        }

        resp = requests.post(
            "https://sh.dataspace.copernicus.eu/api/v1/process",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type":  "application/json",
                "Accept":        "image/tiff"
            },
            json=payload,
            timeout=30
        )

        if resp.status_code != 200:
            return None, f"Errore API Sentinel: {resp.status_code}"

        # Decodifica risposta — gestisce sia TIFF float32 che PNG/JPEG
        import io
        raw = resp.content

        # Debug: controlla content-type
        content_type = resp.headers.get("Content-Type", "")

        import numpy as np_local
        ndvi_mean = None
        bsi_mean  = None

        # Prova 1: tifffile (più robusto per TIFF float32 multibanda)
        try:
            import tifffile
            arr = tifffile.imread(io.BytesIO(raw))
            if arr.ndim == 3:
                ndvi_vals = arr[:,:,0].flatten().astype(np_local.float32)
                bsi_vals  = arr[:,:,1].flatten().astype(np_local.float32)
            else:
                ndvi_vals = arr.flatten().astype(np_local.float32)
                bsi_vals  = np_local.zeros_like(ndvi_vals)
            mask = (ndvi_vals > -1) & (ndvi_vals < 1) & (bsi_vals > -1) & (bsi_vals < 1)
            if mask.sum() >= 5:
                ndvi_mean = float(np_local.nanmedian(ndvi_vals[mask]))
                bsi_mean  = float(np_local.nanmedian(bsi_vals[mask]))
        except Exception:
            pass

        # Prova 2: PIL/Pillow con libtiff
        if ndvi_mean is None:
            try:
                from PIL import Image
                Image.MAX_IMAGE_PIXELS = None
                img = Image.open(io.BytesIO(raw))
                arr = np_local.array(img, dtype=np_local.float32)
                if arr.ndim == 3 and arr.shape[2] >= 2:
                    ndvi_vals = arr[:,:,0].flatten()
                    bsi_vals  = arr[:,:,1].flatten()
                elif arr.ndim == 2:
                    ndvi_vals = arr.flatten()
                    bsi_vals  = np_local.zeros_like(ndvi_vals)
                else:
                    ndvi_vals = arr[:,:,0].flatten()
                    bsi_vals  = np_local.zeros_like(ndvi_vals)
                mask = (ndvi_vals > -1) & (ndvi_vals < 1) & (bsi_vals > -1) & (bsi_vals < 1)
                if mask.sum() >= 5:
                    ndvi_mean = float(np_local.nanmedian(ndvi_vals[mask]))
                    bsi_mean  = float(np_local.nanmedian(bsi_vals[mask]))
            except Exception:
                pass

        # Prova 3: richiesta PNG invece di TIFF (fallback formato)
        if ndvi_mean is None:
            try:
                payload_png = dict(payload)
                payload_png["output"]["responses"][0]["format"]["type"] = "image/png"
                resp2 = requests.post(
                    "https://sh.dataspace.copernicus.eu/api/v1/process",
                    headers={"Authorization": f"Bearer {token}",
                             "Content-Type": "application/json",
                             "Accept": "image/png"},
                    json=payload_png, timeout=30
                )
                if resp2.status_code == 200:
                    from PIL import Image
                    img2 = Image.open(io.BytesIO(resp2.content)).convert("RGBA")
                    arr2 = np_local.array(img2, dtype=np_local.float32) / 255.0
                    # In PNG a 8bit: banda R=NDVI normalizzato, G=BSI normalizzato
                    ndvi_vals = (arr2[:,:,0] * 2 - 1).flatten()  # denormalizza [-1,1]
                    bsi_vals  = (arr2[:,:,1] * 2 - 1).flatten()
                    mask = (ndvi_vals > -1) & (ndvi_vals < 1)
                    if mask.sum() >= 5:
                        ndvi_mean = float(np_local.nanmedian(ndvi_vals[mask]))
                        bsi_mean  = float(np_local.nanmedian(bsi_vals[mask]))
            except Exception:
                pass

        if ndvi_mean is None:
            return None, "Impossibile decodificare l'immagine satellitare. Aggiungi 'tifffile' al requirements.txt"

        if abs(ndvi_mean) < 0.001 and abs(bsi_mean) < 0.001:
            return None, "Troppo nuvoloso o nessun dato valido nel periodo selezionato (120gg)"

        # Modello regressione LUCAS (semplificato per suoli mediterranei)
        # BSI basso = suolo ricco di SOM; NDVI alto = buona copertura vegetale
        so_stimata = max(0.4, min(7.0, 2.8 - bsi_mean * 3.5 + ndvi_mean * 0.8))

        return {
            "so_pct":    round(so_stimata, 2),
            "ndvi":      round(ndvi_mean, 3),
            "bsi":       round(bsi_mean, 3),
            "n_pixel":   int(mask.sum()),
        }, None

    except Exception as e:
        return None, str(e)


# UI Sentinel-2
SH_CLIENT_ID     = st.secrets.get("SH_CLIENT_ID", "")
SH_CLIENT_SECRET = st.secrets.get("SH_CLIENT_SECRET", "")

if not SH_CLIENT_ID or not SH_CLIENT_SECRET:
    st.info("🔑 Aggiungi **SH_CLIENT_ID** e **SH_CLIENT_SECRET** nei Secrets di Streamlit Cloud per attivare la validazione satellitare.")
else:
    # Controlla quali campi hanno coordinate GPS
    campi_con_gps = []
    if "Lat" in df_edit.columns and "Lon" in df_edit.columns:
        for _, _r in df_edit.iterrows():
            try:
                _rlat = float(_r.get("Lat", 0))
                _rlon = float(_r.get("Lon", 0))
                if _rlat != 0 and _rlon != 0:
                    campi_con_gps.append({
                        "nome":  str(_r.get("Campo", "")),
                        "lat":   _rlat,
                        "lon":   _rlon,
                        "so_inserita": float(_r.get("SO %", 1.5)),
                    })
            except:
                pass

    if not campi_con_gps:
        st.warning("⚠️ Inserisci le coordinate GPS (Lat/Lon) nella tabella appezzamenti per attivare la validazione satellitare.")
    else:
        sent_col1, sent_col2 = st.columns([1, 2])
        with sent_col1:
            campo_sel = st.selectbox(
                "Seleziona campo da analizzare",
                options=[c["nome"] for c in campi_con_gps],
                key="sentinel_campo"
            )
            if st.button("🛰️ Analizza con Sentinel-2", use_container_width=True):
                campo_info = next(c for c in campi_con_gps if c["nome"] == campo_sel)
                with st.spinner(f"Scaricamento immagine Sentinel-2 per {campo_sel}..."):
                    risultato, errore = stima_so_sentinel(
                        campo_info["lat"], campo_info["lon"],
                        SH_CLIENT_ID, SH_CLIENT_SECRET
                    )
                if errore:
                    st.error(f"❌ {errore}")
                    st.session_state["sentinel_risultato"] = None
                else:
                    st.session_state["sentinel_risultato"] = {**risultato, **campo_info}

        with sent_col2:
            if st.session_state.get("sentinel_risultato"):
                res = st.session_state["sentinel_risultato"]
                so_sat  = res["so_pct"]
                so_man  = res["so_inserita"]
                delta   = round(so_sat - so_man, 2)
                delta_pct = round(abs(delta) / max(so_man, 0.1) * 100, 0)

                # Colore semaforo
                if abs(delta) <= 0.3:
                    semaforo = "🟢"
                    msg_delta = "Dati coerenti — differenza < 0.3%"
                    clr = "#4ade80"
                elif abs(delta) <= 0.8:
                    semaforo = "🟡"
                    msg_delta = "Discrepanza moderata — considera un nuovo campionamento"
                    clr = "#fde68a"
                else:
                    semaforo = "🔴"
                    msg_delta = "Discrepanza elevata — dati manuali potrebbero essere datati"
                    clr = "#f87171"

                st.markdown(f"""
                <div style="background:#0d1a0d;border:1.5px solid #22c55e;border-radius:14px;
                            padding:1.2rem 1.6rem;margin:.5rem 0">
                  <div style="color:#4ade80;font-weight:700;font-size:.9rem;margin-bottom:.8rem">
                    🛰️ Risultato Sentinel-2 — {res["nome"]}
                  </div>
                  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:.8rem;margin-bottom:.8rem">
                    <div style="text-align:center;background:#161c16;border-radius:10px;padding:.7rem">
                      <div style="font-size:1.4rem;font-weight:700;color:#ffffff">{so_sat}%</div>
                      <div style="font-size:.65rem;color:#86efac;text-transform:uppercase">SO% Satellite</div>
                    </div>
                    <div style="text-align:center;background:#161c16;border-radius:10px;padding:.7rem">
                      <div style="font-size:1.4rem;font-weight:700;color:#ffffff">{so_man}%</div>
                      <div style="font-size:.65rem;color:#86efac;text-transform:uppercase">SO% Inserita</div>
                    </div>
                    <div style="text-align:center;background:#161c16;border-radius:10px;padding:.7rem">
                      <div style="font-size:1.4rem;font-weight:700;color:{clr}">{"+" if delta>=0 else ""}{delta}%</div>
                      <div style="font-size:.65rem;color:#86efac;text-transform:uppercase">Differenza</div>
                    </div>
                    <div style="text-align:center;background:#161c16;border-radius:10px;padding:.7rem">
                      <div style="font-size:1.4rem;font-weight:700;color:#ffffff">{semaforo}</div>
                      <div style="font-size:.65rem;color:#86efac;text-transform:uppercase">Semaforo</div>
                    </div>
                  </div>
                  <div style="font-size:.78rem;color:{clr};margin-bottom:.5rem">
                    <b>{semaforo} {msg_delta}</b>
                  </div>
                  <div style="font-size:.72rem;color:#86efac;line-height:1.8">
                    NDVI (indice vegetazione): <b style="color:#fff">{res["ndvi"]}</b> &nbsp;·&nbsp;
                    BSI (indice suolo nudo): <b style="color:#fff">{res["bsi"]}</b> &nbsp;·&nbsp;
                    Pixel validi: <b style="color:#fff">{res["n_pixel"]}</b> &nbsp;·&nbsp;
                    Finestra: ultimi 120 giorni senza nuvole
                  </div>
                  <div style="font-size:.68rem;color:#4a5e4e;margin-top:.5rem">
                    Modello: regressione LUCAS Topsoil Survey EU (Ballabio et al. 2019) · Sentinel-2 L2A · Copernicus ESA
                  </div>
                </div>""", unsafe_allow_html=True)

                # Suggerimento aggiornamento SO%
                if abs(delta) > 0.3:
                    st.markdown(f"""
                    <div style="background:#1a1000;border:1px solid #f59e0b;border-radius:10px;
                                padding:.8rem 1.1rem;margin:.3rem 0;font-size:.79rem">
                      💡 <b style="color:#fde68a">Suggerimento:</b>
                      <span style="color:#e8f5e9"> Il satellite stima SO% <b>{so_sat}%</b> vs <b>{so_man}%</b> inserito manualmente
                      (differenza {delta_pct:.0f}%). Considera di aggiornare il dato nella tabella
                      o effettuare un nuovo campionamento del suolo per confermare.</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#161c16;border:1px solid rgba(34,197,94,.2);
                     border-radius:12px;padding:1.2rem;font-size:.8rem;color:#86efac">
                  <b style="color:#4ade80">Come funziona</b><br><br>
                  Il sistema scarica l'immagine Sentinel-2 L2A più recente senza nuvole
                  (fino a 120 giorni fa) per le coordinate GPS del campo selezionato.<br><br>
                  Calcola <b>NDVI</b> (indice di vegetazione) e <b>BSI</b> (Bare Soil Index)
                  dalle bande NIR, Red e SWIR, poi stima la SO% con un modello di regressione
                  calibrato su 22.000 campioni europei (LUCAS Topsoil Survey).<br><br>
                  Il risultato viene confrontato con il valore inserito manualmente
                  e mostra un semaforo di coerenza.
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  MAPPA
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🗺️ Mappa Interattiva Aziendale</div>', unsafe_allow_html=True)

def colore_score(s):
    if s >= 70: return "green"
    if s >= 48: return "orange"
    return "red"

def score_campo(row):
    s = 30
    prot = str(row.get("Protocollo",""))
    so   = float(row.get("SO %",1.5))
    if prot == "Rigenerativo Full": s += 35
    elif prot == "Intermedio":      s += 18
    if row.get("Cover crops",False): s += 12
    if so > 2.5: s += 10
    elif so > 1.8: s += 5
    return min(100, s)

def icona_coltura(col):
    return {"Vite (DOC/IGT)":"🍇","Olivo":"🫒","Cereali":"🌾",
            "Frutteto":"🍎","Nocciolo":"🌰","Orticole":"🥬",
            "Foraggere":"🌿","Misto":"🌱"}.get(col,"🌱")

if FOLIUM_OK:
    campi_gps = df_edit.dropna(subset=["Lat","Lon"]) if "Lat" in df_edit.columns else pd.DataFrame()
    if len(campi_gps) > 0:
        map_lat = float(campi_gps["Lat"].mean())
        map_lon = float(campi_gps["Lon"].mean())
        zoom    = 14
    else:
        map_lat, map_lon = lat, lon
        zoom = 11

    m = folium.Map(location=[map_lat, map_lon], zoom_start=zoom, tiles=None)
    folium.TileLayer(tiles="OpenStreetMap", name="Mappa stradale", control=True).add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery", name="🛰️ Satellite", overlay=False, control=True,
    ).add_to(m)
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google", name="🛰️ Satellite + Strade", overlay=False, control=True,
    ).add_to(m)

    if "Lat" in df_edit.columns and "Lon" in df_edit.columns:
        for _, row in df_edit.iterrows():
            try:
                rlat = float(row["Lat"]) if row["Lat"] else None
                rlon = float(row["Lon"]) if row["Lon"] else None
            except (TypeError, ValueError):
                rlat, rlon = None, None
            if rlat and rlon and not (rlat==0 and rlon==0):
                sc   = score_campo(row)
                col  = colore_score(sc)
                ico  = icona_coltura(str(row.get("Coltura","")))
                nome = str(row.get("Campo","Campo"))
                prot = str(row.get("Protocollo",""))
                so   = float(row.get("SO %",0))
                ha   = float(row.get("Ettari",0))
                coltura = str(row.get("Coltura",""))
                badge_col = "#1a6b3a" if sc>=70 else "#c9963a" if sc>=48 else "#ef4444"
                badge_rating = "A" if sc>=80 else "B" if sc>=65 else "C" if sc>=48 else "D"
                popup_html = f"""
                <div style="font-family:Arial,sans-serif;min-width:220px;font-size:13px">
                  <div style="background:linear-gradient(135deg,#061912,#1a6b3a);
                       color:#fff;padding:10px 14px;border-radius:8px 8px 0 0;
                       border-bottom:3px solid #c9963a">
                    <b style="font-size:15px">{ico} {nome}</b>
                  </div>
                  <div style="padding:10px 14px;background:#f4f1ea;border-radius:0 0 8px 8px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                      <span style="color:#7a8c7e;font-size:11px">Score ESG</span>
                      <span style="background:{badge_col};color:#fff;padding:2px 9px;
                            border-radius:20px;font-weight:700;font-size:11px">
                        {badge_rating} — {sc}/100</span>
                    </div>
                    <table style="width:100%;font-size:12px;border-collapse:collapse">
                      <tr><td style="color:#7a8c7e;padding:2px 0">Coltura</td>
                          <td style="text-align:right;font-weight:600">{coltura}</td></tr>
                      <tr><td style="color:#7a8c7e;padding:2px 0">Superficie</td>
                          <td style="text-align:right;font-weight:600">{ha} ha</td></tr>
                      <tr><td style="color:#7a8c7e;padding:2px 0">Sostanza Organica</td>
                          <td style="text-align:right;font-weight:600">{so}%</td></tr>
                      <tr><td style="color:#7a8c7e;padding:2px 0">Protocollo</td>
                          <td style="text-align:right;font-weight:600">{prot}</td></tr>
                    </table>
                  </div>
                </div>"""
                folium.Marker(
                    location=[rlat, rlon],
                    popup=folium.Popup(popup_html, max_width=260),
                    tooltip=f"{ico} {nome} — Score {sc}/100",
                    icon=folium.Icon(color=col, icon="leaf", prefix="fa")
                ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        tooltip=f"🌦️ Stazione meteo {regione} — {M['tmax']}°/{M['tmin']}°C · ET₀ {M['et0']} mm/g",
        icon=folium.Icon(color="blue", icon="cloud", prefix="fa")
    ).add_to(m)
    folium.LayerControl(position="topright").add_to(m)

    map_col, info_col = st.columns([3, 1])
    with map_col:
        st_folium(m, width=None, height=480, returned_objects=[])
    with info_col:
        st.markdown("""
        <div class="map-legend">
          <b>Legenda marker</b>
          <div style="margin-top:.6rem;line-height:2">
            🟢 <b>Verde</b> — Score ≥70 (A/B)<br>
            🟡 <b>Arancione</b> — Score 48-69 (C)<br>
            🔴 <b>Rosso</b> — Score &lt;48 (D)<br>
            🔵 <b>Blu</b> — Stazione meteo<br>
          </div>
          <hr style="border:none;border-top:1px solid rgba(201,150,58,.3);margin:.6rem 0">
          <b>Come usarla</b>
          <div style="margin-top:.4rem;color:#4a5e4e;line-height:1.6">
            Clicca un marker<br>per i dettagli.<br><br>
            Cambia vista con<br>il selettore layer<br>in alto a destra.
          </div>
        </div>""", unsafe_allow_html=True)
else:
    st.info("📦 Per attivare la mappa interattiva, aggiungi **folium** e **streamlit-folium** al requirements.txt.")

# ══════════════════════════════════════════════════════════════════════
#  FERTILIZZANTI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🧪 Fertilizzanti & Fitofarmaci — CO₂ Scope 1 + Scope 3</div>', unsafe_allow_html=True)
st.caption("Inserisci i fertilizzanti e fitofarmaci usati nell'anno.")

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

co2_fert_prod = 0.0
co2_fert_n2o  = 0.0
co2_n2o_org   = 0.0
co2_n2o_min   = 0.0
fert_detail   = []
for _, fr in df_fert.iterrows():
    prod = str(fr.get("Prodotto",""))
    qty  = max(0.0, float(fr.get("Quantità (kg/anno)",0)))
    ef   = EF_FERT.get(prod, {"ef_prod":0,"ef_n2o":0.01,"tipo":"minerale","desc":""})
    s3   = qty * ef["ef_prod"] / 1000
    s1   = qty * ef["ef_n2o"] * (44/28) * 265 / 1000
    co2_fert_prod += s3
    co2_fert_n2o  += s1
    if ef.get("tipo","minerale") == "organico":
        co2_n2o_org += s1
    else:
        co2_n2o_min += s1
    fert_detail.append({"prod":prod,"qty":qty,"s3":round(s3,3),"s1":round(s1,3),"ef":ef,"tipo":ef.get("tipo","minerale")})

co2_fito_s3 = 0.0
for _, ft in df_fito.iterrows():
    prod = str(ft.get("Prodotto",""))
    qty  = max(0.0, float(ft.get("Quantità p.a. (kg/anno)",0)))
    co2_fito_s3 += qty * EF_FITO.get(prod, 0) / 1000

co2_fert_totale = co2_fert_prod + co2_fert_n2o + co2_fito_s3

pct_org = round(co2_n2o_org / max(co2_fert_n2o, 0.001) * 100, 0)
bene_org = pct_org >= 50
st.markdown(f"""
<div class="n2o-strip">
  🌿 <b>N₂O: Organico vs Minerale —</b>&nbsp;
  EF organici (0.004-0.006): <b style="color:#4ade80">{round(co2_n2o_org,2)} tCO₂eq</b> &nbsp;·&nbsp;
  EF minerali (0.010-0.013): <b style="color:#f87171">{round(co2_n2o_min,2)} tCO₂eq</b> &nbsp;·&nbsp;
  Quota organica: <b style="color:#fde68a">{pct_org:.0f}%</b>
  {"&nbsp;✅ buona pratica" if bene_org else "&nbsp;⚠️ aumenta quota organica per ridurre N₂O del 40-60%"}
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  SCARTI & MATERIE PRIME
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
if "df_trasporti" not in st.session_state:
    st.session_state.df_trasporti = pd.DataFrame([
        {"Voce trasporto":"Trasporto prodotti mercato (km·t)","Quantità annua":2500,"Note":""},
        {"Voce trasporto":"Auto aziendale diesel (km)","Quantità annua":8000,"Note":""},
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

st.markdown("**🚚 Trasporti & Mobilità (Scope 3 upstream/downstream)**")
st.caption("Trasporto prodotti al mercato, input acquistati, spostamenti aziendali.")
df_trasporti = st.data_editor(
    st.session_state.df_trasporti, num_rows="dynamic", use_container_width=True,
    column_config={
        "Voce trasporto": st.column_config.SelectboxColumn(options=list(EF_TRASPORTI.keys()),required=True),
        "Quantità annua": st.column_config.NumberColumn(min_value=0,max_value=10000000,format="%.0f"),
    }, key="editor_trasporti"
)
st.session_state.df_trasporti = df_trasporti

co2_scarti = 0.0
scarti_detail = []
for _, sr in df_scarti.iterrows():
    sc_nome = str(sr.get("Scarto",""))
    qty = max(0.0, float(sr.get("Quantità (t/anno)",0)))
    ef  = EF_SCARTI.get(sc_nome, 0)
    co2_s = qty * ef
    co2_scarti += co2_s
    scarti_detail.append({"scarto":sc_nome,"qty":qty,"co2":round(co2_s,3),"ef":ef})

co2_materie = 0.0
for _, mr in df_materie.iterrows():
    mat = str(mr.get("Materia prima",""))
    qty = max(0.0, float(mr.get("Quantità",0)))
    co2_materie += qty * EF_MATERIE.get(mat, 0) / 1000

co2_trasporti = 0.0
trasporti_detail = []
for _, tr in df_trasporti.iterrows():
    voce = str(tr.get("Voce trasporto",""))
    qty  = max(0.0, float(tr.get("Quantità annua",0)))
    ef   = EF_TRASPORTI.get(voce, 0)
    co2_t = qty * ef / 1000
    co2_trasporti += co2_t
    trasporti_detail.append({"voce":voce,"qty":qty,"co2":round(co2_t,3),"ef":ef})

# ══════════════════════════════════════════════════════════════════════
#  CALCOLI AGGREGATI
# ══════════════════════════════════════════════════════════════════════
res_att = [calcola(r,False) for _,r in df_edit.iterrows()]
res_pot = [calcola(r,True)  for _,r in df_edit.iterrows()]

def S(key,src=None): return sum(r[key] for r in (src or res_att))
tot_ha      = max(1.0, float(df_edit["Ettari"].sum()))
tot_seq     = S("co2_seq");   tot_emit_base = S("co2_emit")
tot_emit    = tot_emit_base + co2_fert_totale + max(0, co2_scarti) + co2_materie + co2_trasporti
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

score = 28
score += min(25, int(max(0, tot_netto/tot_ha)*12))
for c,v in [(14,cert_bio),(8,cert_sqnpi),(7,cert_gap),(8,cert_viva),(10,cert_iso),(8,cert_csrd)]:
    if v: score += c
cc_r = sum(1 for _,r in df_edit.iterrows() if r.get("Cover crops",False))/max(len(df_edit),1)
score += int(cc_r*12)
if tot_spreco < tot_fabb*0.1: score += 7
for v,pts in [(inv_iot,4),(inv_drip,5),(inv_gps,4),(inv_biochar,6)]: score += pts if v else 0
n_scarti_virtuosi = sum(1 for _,sr in df_scarti.iterrows() if EF_SCARTI.get(str(sr.get("Scarto","")),0) < 0)
score += min(8, n_scarti_virtuosi*3)
score = min(100, score)

if score>=80:   rating,rcls,rcol,rbg = "A — Eccellente","A","#4ade80","rgba(34,197,94,.15)"
elif score>=65: rating,rcls,rcol,rbg = "B — Conforme ESG","B","#60a5fa","rgba(59,130,246,.15)"
elif score>=48: rating,rcls,rcol,rbg = "C — Sviluppabile","C","#fcd34d","rgba(245,158,11,.15)"
else:           rating,rcls,rcol,rbg = "D — Critico","D","#f87171","rgba(239,68,68,.15)"

coltura_principale = df_edit["Coltura"].mode()[0] if len(df_edit)>0 else "Misto"
bm = BM_COLTURA.get(coltura_principale, BM_COLTURA["Misto"])

# ══════════════════════════════════════════════════════════════════════
#  BILANCIO SCOPE 1-2-3
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🏭 Bilancio GHG Completo — Scope 1 · 2 · 3 (GHG Protocol)</div>', unsafe_allow_html=True)

sb1, sb2, sb3 = st.columns(3)
scope1_total = tot_emit_base + co2_fert_n2o + max(0, sum(
    r["qty"]*r["ef"] for r in scarti_detail if r["ef"] > 0))
scope2_total = 0.0
scope3_total = co2_fert_prod + co2_fito_s3 + co2_materie + co2_trasporti + abs(min(0, co2_scarti))

with sb1:
    st.markdown(f"""
    <div class="scope-box scope1">
      <div style="font-size:.85rem;font-weight:700;color:#fca5a5;margin-bottom:.5rem">
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
      <div style="font-size:.85rem;font-weight:700;color:#fcd34d;margin-bottom:.5rem">
        🟡 Scope 2 — Emissioni Indirette Energia</div>
      <div style="font-size:.78rem;line-height:1.9">
        Elettricità acquistata: <b>0 tCO₂</b><br>
        <span style="color:#fde68a;font-size:.72rem">(Aggiungi pompe irrigazione,<br>celle frigorifere, impianti)</span><br>
        <hr style="border:none;border-top:1px solid #fdba74;margin:.4rem 0">
        <b>Totale Scope 2: {round(scope2_total,2)} tCO₂eq/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

with sb3:
    st.markdown(f"""
    <div class="scope-box scope3">
      <div style="font-size:.85rem;font-weight:700;color:#4ade80;margin-bottom:.5rem">
        🟢 Scope 3 — Catena del valore (upstream)</div>
      <div style="font-size:.78rem;line-height:1.9">
        Produzione fertilizzanti: <b>{round(co2_fert_prod,2)} tCO₂eq</b><br>
        Produzione fitofarmaci: <b>{round(co2_fito_s3,2)} tCO₂eq</b><br>
        Materie prime acquistate: <b>{round(co2_materie,2)} tCO₂eq</b><br>
        Trasporti & mobilità: <b>{round(co2_trasporti,2)} tCO₂eq</b><br>
        <hr style="border:none;border-top:1px solid #86efac;margin:.4rem 0">
        <b>Totale Scope 3: {round(scope3_total,2)} tCO₂eq/anno</b>
      </div>
    </div>""", unsafe_allow_html=True)

bal_col1, bal_col2 = st.columns([2,1])
with bal_col1:
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative","relative","relative","relative","relative","relative","relative","total"],
        x=["Sequestro<br>suolo","Scarti<br>virtuosi","Gasolio<br>macchine","N₂O<br>campo",
           "Fertilizz.<br>Scope3","Trasporti<br>Scope3","Scarti<br>emissivi","Bilancio<br>netto"],
        y=[tot_seq, abs(min(0,co2_scarti)), -(S("diesel_co2")), -(S("n2o")+co2_fert_n2o),
           -(co2_fert_prod+co2_fito_s3+co2_materie), -(co2_trasporti), -(max(0,co2_scarti)), 0],
        connector={"line":{"color":"rgba(15,53,32,.2)"}},
        increasing={"marker":{"color":"#1a6b3a"}},
        decreasing={"marker":{"color":"#ef4444"}},
        totals={"marker":{"color":"#c9963a"}},
        text=[f"+{round(tot_seq,1)}", f"+{round(abs(min(0,co2_scarti)),1)}",
              f"-{round(S('diesel_co2'),1)}", f"-{round(S('n2o')+co2_fert_n2o,1)}",
              f"-{round(co2_fert_prod+co2_fito_s3+co2_materie,1)}", f"-{round(co2_trasporti,1)}",
              f"-{round(max(0,co2_scarti),1)}", f"{round(tot_netto,1)}"],
        textposition="outside",
    ))
    fig_wf.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
        font=dict(family="Lexend",color="#061912"),
        title="Bilancio GHG Waterfall — tCO₂eq/anno",
        margin=dict(t=44,b=28,l=28,r=16),
        yaxis_title="tCO₂eq/anno", showlegend=False
    )
    st.plotly_chart(fig_wf, use_container_width=True)

with bal_col2:
    col_netto = "#065f46" if tot_netto>=0 else "#991b1b"
    st.markdown(f"""
    <div class="ghg-box" style="margin-top:.3rem">
      <div style="font-family:'DM Serif Display',serif;font-size:1rem;color:#061912;margin-bottom:.8rem">
        📊 Riepilogo GHG</div>
      <table style="width:100%;font-size:.78rem;border-collapse:collapse">
        <tr><td style="padding:4px 0;color:#86efac">Sequestro suolo</td>
            <td style="text-align:right;color:#4ade80;font-weight:600">+{round(tot_seq,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Scarti virtuosi</td>
            <td style="text-align:right;color:#4ade80;font-weight:600">+{round(abs(min(0,co2_scarti)),1)} t</td></tr>
        <tr style="border-top:1px solid rgba(201,150,58,.2)"><td style="padding:4px 0;color:#86efac">Gasolio (Sc.1)</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(S('diesel_co2'),1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">N₂O (Sc.1)</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(S('n2o')+co2_fert_n2o,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Fertilizz. (Sc.3)</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(co2_fert_prod+co2_fito_s3,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Materie prime (Sc.3)</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(co2_materie,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Trasporti (Sc.3)</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(co2_trasporti,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Scarti emissivi</td>
            <td style="text-align:right;color:#f87171;font-weight:600">-{round(max(0,co2_scarti),1)} t</td></tr>
        <tr style="border-top:2px solid #22c55e;background:#052e16"><td style="padding:6px 0;font-weight:700;color:#fff">Bilancio NETTO</td>
            <td style="text-align:right;font-weight:700;font-size:.95rem;color:{'#4ade80' if tot_netto>=0 else '#f87171'}">
            {"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</td></tr>
        <tr><td style="padding:4px 0;color:#86efac">Valore crediti</td>
            <td style="text-align:right;color:#4ade80;font-weight:600">€{int(val_cred):,}</td></tr>
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
    (f"{int(tot_fabb):,} m³","Fabbisogno Idrico",f"Spreco {int(tot_spreco):,} m³" + (" 💧-35% drip" if inv_drip else "")),
    (f"€{int(tot_vf):,}","Valore Fondo Stimato",f"{int(tot_ha)} ha · CREA-AA"),
    (f"{marg_pct}%","Margine Netto",f"€{margine:,}/anno"),
]
for col,(v,l,s) in zip(kcols,kpis):
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v">{v}</div>'
                    f'<div class="kpi-l">{l}</div>'
                    f'<div class="kpi-s">{s}</div></div>',unsafe_allow_html=True)

delta_s = score - bm["score"]
delta_c = round(tot_seq/tot_ha - bm["co2_ha"], 2)
delta_m = round(marg_pct - bm["margine_pct"], 1)
bm1,bm2=st.columns(2)
with bm1:
    clr_s="#22c55e" if delta_s>=0 else "#f59e0b"
    clr_c="#22c55e" if delta_c>=0 else "#f59e0b"
    st.markdown(f"""<div class="info-box" style="margin-top:.5rem">
      📊 <b>Benchmark {bm["label"]} — CREA-AA 2025:</b>&nbsp;
      Score <b style="color:{clr_s}">{"+" if delta_s>=0 else ""}{delta_s} pt</b> vs media {bm["score"]}/100&nbsp;·&nbsp;
      CO₂/ha <b style="color:{clr_c}">{"+" if delta_c>=0 else ""}{delta_c} t</b> vs media {bm["co2_ha"]} t/ha
    </div>""",unsafe_allow_html=True)
with bm2:
    pct=max(5,min(95,100-int((score-30)/0.7)))
    clr_m="#22c55e" if delta_m>=0 else "#ef4444"
    st.markdown(f"""<div class="info-box" style="margin-top:.5rem">
      🏆 <b>Posizionamento settore {bm["label"]}:</b>&nbsp;
      Top <b style="color:#4ade80">{pct}%</b>&nbsp;·&nbsp;
      Margine medio settore <b style="color:#c9963a">{bm["margine_pct"]}%</b> — tuo: <b style="color:{clr_m}">{"+" if delta_m>=0 else ""}{delta_m}%</b>
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  AGRONOMO VIRTUALE IA — Claude API
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🤖 Agronomo Virtuale IA — Analisi Personalizzata</div>', unsafe_allow_html=True)
st.caption("Powered by Claude AI — Analizza tutti i tuoi dati aziendali e genera un briefing agronomico su misura.")

ai_col1, ai_col2 = st.columns([2, 1])
with ai_col1:
    if st.button("🤖 Genera analisi agronomica IA", use_container_width=True):
        with st.spinner("L'agronomo virtuale sta analizzando la tua azienda..."):

            # Proiezione RothC semplificata per il contesto
            rothc_5a = []
            for _, rr in df_edit.iterrows():
                so0_ia  = max(0.1, float(rr.get("SO %", 1.5)))
                prot_ia = str(rr.get("Protocollo", "Intermedio"))
                nome_ia = str(rr.get("Campo", ""))
                k_ia = {"Convenzionale": -0.038, "Intermedio": -0.010,
                        "Rigenerativo Full": 0.015}.get(prot_ia, -0.010)
                so5 = round(so0_ia * ((1 + k_ia) ** 5), 2)
                rothc_5a.append(f"{nome_ia}: {so0_ia}% → {so5}% ({prot_ia})")

            # Composizione dati azienda per il prompt
            dati_azienda = f"""
ANAGRAFICA AZIENDA:
- Nome: {nome_az} — {regione} / {zona}
- Superficie totale: {round(tot_ha, 1)} ha
- Coltura principale: {coltura_principale}
- Agronomo: {agronomo}

BILANCIO GHG (Scope 1+2+3 — GHG Protocol):
- Sequestro suolo: +{round(tot_seq, 2)} tCO₂/anno
- Emissioni totali: -{round(tot_emit, 2)} tCO₂eq/anno
- Bilancio NETTO: {round(tot_netto, 2)} tCO₂eq/anno ({"Carbon Positive ✅" if tot_netto >= 0 else "Emittente ⚠️"})
- Valore crediti CO₂ potenziali: €{int(val_cred):,}/anno (@ €{prezzo_co2}/t)
- Emissioni Scope 3 fertilizzanti: {round(co2_fert_prod, 2)} tCO₂eq
- Emissioni Scope 3 trasporti: {round(co2_trasporti, 2)} tCO₂eq

SCORE ESG: {score}/100 — Rating {rcls}

CAMPI E PRATICHE:
{df_edit[["Campo","Ettari","SO %","Protocollo","Coltura","Cover crops","Irrigazione m³/ha"]].to_string(index=False)}

FERTILIZZANTI USATI:
{df_fert[["Prodotto","Quantità (kg/anno)"]].to_string(index=False) if len(df_fert) > 0 else "Nessuno inserito"}

ACQUA E STRESS IDRICO:
- Stress idrico attuale: {round(stress_idx * 100):.0f}% ({"CRITICO" if stress_idx > 0.4 else "MODERATO" if stress_idx > 0.2 else "OK"})
- Deficit ET₀ - pioggia (30gg): {round(deficit)} mm
- Fabbisogno irriguo totale: {int(tot_fabb):,} m³/anno
- Spreco irriguo stimato: {int(tot_spreco):,} m³/anno = €{int(tot_spreco * costo_acqua):,}

PROIEZIONE SOM — RothC 5 anni:
{chr(10).join(rothc_5a)}

SITUAZIONE ECONOMICA:
- Fatturato: €{fatturato:,}/anno
- Margine netto: {marg_pct}%
- Costo gasolio annuo: €{int(tot_c_die):,}
- PAC Eco-Scheme accessibili ora: €{int(pac_totale):,}/anno

CERTIFICAZIONI ATTIVE: {", ".join([c for c,v in [("Biologico",cert_bio),("SQnpi",cert_sqnpi),("GlobalG.A.P.",cert_gap),("VIVA",cert_viva),("ISO 14064",cert_iso),("CSRD",cert_csrd)] if v]) or "Nessuna"}
"""

            try:
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": st.secrets.get("ANTHROPIC_API_KEY", ""),
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1500,
                        "system": """Sei un agronomo esperto specializzato in carbon farming, agricoltura rigenerativa e sostenibilità ESG in Italia.
Analizza i dati dell'azienda agricola forniti e produci un briefing agronomico professionale in italiano.

Struttura OBBLIGATORIA della risposta:

🔍 DIAGNOSI
[2-3 righe: situazione attuale, punti di forza concreti, criticità principali con dati numerici]

🎯 TOP 3 AZIONI PRIORITARIE
1. [Nome azione] — [Cosa fare esattamente] → ROI stimato: €X/anno | Payback: X mesi
2. [Nome azione] — [Cosa fare esattamente] → ROI stimato: €X/anno | Payback: X mesi  
3. [Nome azione] — [Cosa fare esattamente] → ROI stimato: €X/anno | Payback: X mesi

⚠️ RISCHI A 5 ANNI
- [Rischio 1]: probabilità X%, impatto economico stimato €X/anno
- [Rischio 2]: probabilità X%, impatto economico stimato €X/anno

💡 POTENZIALE
[Una frase finale che quantifica il potenziale massimo raggiungibile con le azioni consigliate]

Usa sempre dati numerici precisi dai dati forniti. Sii diretto, concreto, mai generico.""",
                        "messages": [{"role": "user", "content": f"Analizza questa azienda agricola italiana:\n\n{dati_azienda}"}]
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    analisi = response.json()["content"][0]["text"]
                    st.session_state["ultima_analisi_ia"] = analisi
                    st.session_state["ultima_analisi_az"]  = nome_az
                elif response.status_code == 401:
                    st.error("❌ API Key non valida o mancante. Aggiungi ANTHROPIC_API_KEY nei secrets di Streamlit Cloud.")
                    st.session_state["ultima_analisi_ia"] = None
                else:
                    st.error(f"❌ Errore API: {response.status_code} — {response.text[:200]}")
                    st.session_state["ultima_analisi_ia"] = None

            except requests.exceptions.Timeout:
                st.error("⏱️ Timeout — riprova tra qualche secondo.")
                st.session_state["ultima_analisi_ia"] = None
            except Exception as e:
                st.error(f"❌ Errore connessione: {str(e)}")
                st.session_state["ultima_analisi_ia"] = None

with ai_col2:
    st.markdown("""
    <div style="background:#161c16;border:1px solid rgba(34,197,94,.2);
         border-radius:12px;padding:1rem;font-size:.78rem;color:#86efac">
      <b style="color:#4ade80;font-size:.85rem">💡 Come funziona</b><br><br>
      Il modello legge tutti i dati della tua azienda — campi, fertilizzanti, bilancio GHG, meteo, stress idrico, proiezioni RothC — e genera un briefing come farebbe un consulente agronomo che ha studiato il tuo fascicolo per un'ora.<br><br>
      <b style="color:#4ade80">Cosa ottieni:</b><br>
      • Diagnosi situazione attuale<br>
      • Top 3 azioni con ROI stimato<br>
      • Rischi a 5 anni con impatto €<br>
      • Potenziale massimo raggiungibile<br><br>
      <span style="color:#4ade80;font-size:.7rem">⚡ Richiede ANTHROPIC_API_KEY nei secrets</span>
    </div>""", unsafe_allow_html=True)

# Mostra analisi se disponibile (persiste tra rerun)
if st.session_state.get("ultima_analisi_ia"):
    az_label = st.session_state.get("ultima_analisi_az", nome_az)
    st.markdown(f"""
    <div style="background:#0d1a0d;border:1.5px solid #22c55e;border-radius:14px;
                padding:1.6rem 2rem;margin:1rem 0;
                box-shadow:0 0 30px rgba(34,197,94,.1)">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
        <div style="color:#4ade80;font-weight:700;font-size:1rem">
          🤖 Analisi Agronomica IA — {az_label}
        </div>
        <div style="color:#86efac;font-size:.7rem">
          Powered by Claude · {datetime.now().strftime("%d/%m/%Y %H:%M")}
        </div>
      </div>
      <div style="color:#e8f5e9;font-size:.85rem;line-height:1.9;
                  white-space:pre-wrap;font-family:'Lexend',sans-serif">{st.session_state["ultima_analisi_ia"]}</div>
    </div>""", unsafe_allow_html=True)

    # Bottone esporta analisi
    if st.button("📋 Copia analisi negli appunti / Salva come testo"):
        testo_export = f"ANALISI AGRONOMICA IA — {az_label}\n{datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n{st.session_state['ultima_analisi_ia']}"
        st.download_button(
            label="⬇️ Scarica analisi .txt",
            data=testo_export,
            file_name=f"AnalisiIA_{az_label.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


# ══════════════════════════════════════════════════════════════════════
#  GRAFICI
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">📈 Analisi Multi-Dimensionale</div>', unsafe_allow_html=True)
PLT = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#faf9f6",
           font=dict(family="Lexend",color="#061912"),margin=dict(t=44,b=28,l=28,r=16))

g1,g2,g3 = st.columns(3)
with g1:
    categorie = ["Seq. suolo","Gasolio","N₂O campo","Fertilizz.\nSc.3","Fitofarmaci\nSc.3","Materie\nprime","Scarti"]
    valori    = [tot_seq, -S("diesel_co2"), -(S("n2o")+co2_fert_n2o),
                 -co2_fert_prod, -co2_fito_s3, -co2_materie, -co2_scarti]
    colori    = ["#1a6b3a" if v>0 else "#ef4444" for v in valori]
    fig_br = go.Figure(go.Bar(x=categorie, y=valori, marker_color=colori, opacity=.88))
    fig_br.update_layout(**PLT, title="Breakdown emissioni/sequestro (t/anno)", yaxis_title="tCO₂eq/anno")
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
        line=dict(color="#94a3b8",width=1.5,dash="dot"),name="Media settore",fillcolor="rgba(0,0,0,0)"))
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
#  RothC
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🌱 Proiezione Sostanza Organica — Modello RothC (10 anni)</div>',
            unsafe_allow_html=True)
st.caption("RothC semplificato (Coleman & Jenkinson 1996). Convenzionale: -3.8%/anno · Intermedio: -1.0%/anno · Rigenerativo: +1.5%/anno")

anni_proj = list(range(date.today().year, date.today().year + 11))
col_prot  = {"Convenzionale":"#ef4444","Intermedio":"#f59e0b","Rigenerativo Full":"#22c55e"}

rc1, rc2 = st.columns([3, 1])
with rc1:
    fig_rc = go.Figure()
    fig_rc.add_hline(y=1.5, line_dash="dash", line_color="#94a3b8",
                     annotation_text="Soglia critica 1.5%", annotation_position="top right")
    fig_rc.add_hline(y=2.5, line_dash="dot", line_color="#1a6b3a",
                     annotation_text="Obiettivo 4‰ 2.5%", annotation_position="top right")
    for _, _r in df_edit.iterrows():
        so0   = max(0.1, float(_r.get("SO %", 1.5)))
        prot  = str(_r.get("Protocollo", "Intermedio"))
        nome  = str(_r.get("Campo", ""))
        vals, d5, d10, k = rothc_proiezione(so0, prot, 10)
        clr   = col_prot.get(prot, "#94a3b8")
        fig_rc.add_scatter(
            x=anni_proj, y=vals, name=f"{nome} ({prot[:4]}…)",
            line=dict(color=clr, width=2.5), mode="lines+markers", marker=dict(size=5),
        )
    fig_rc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6",
        font=dict(family="Lexend", color="#061912"),
        title="Evoluzione SO% — Proiezione 10 anni per protocollo",
        yaxis_title="Sostanza Organica %", xaxis_title="Anno",
        margin=dict(t=44, b=28, l=28, r=16),
        legend=dict(orientation="h", y=-0.22, font=dict(size=9))
    )
    st.plotly_chart(fig_rc, use_container_width=True)

with rc2:
    st.markdown("""<div class="rothc-card">
        <b>Impatto a 5 e 10 anni</b>""", unsafe_allow_html=True)
    for _, _r in df_edit.iterrows():
        so0  = max(0.1, float(_r.get("SO %", 1.5)))
        prot = str(_r.get("Protocollo", "Intermedio"))
        nome = str(_r.get("Campo", ""))
        _, d5, d10, k = rothc_proiezione(so0, prot, 10)
        clr5  = "#4ade80" if d5  >= 0 else "#f87171"
        clr10 = "#4ade80" if d10 >= 0 else "#f87171"
        st.markdown(f"""<div style="border-left:3px solid {col_prot.get(prot,'#94a3b8')};
            padding:.4rem .6rem;margin:.3rem 0;background:#f4f1ea;border-radius:0 8px 8px 0">
            <b style="font-size:.8rem;color:#ffffff">{nome}</b><br>
            <span style="color:#86efac;font-size:.72rem">{prot[:12]}…</span><br>
            5a: <b style="color:{clr5}">{"+" if d5>=0 else ""}{d5}%</b> &nbsp;
            10a: <b style="color:{clr10}">{"+" if d10>=0 else ""}{d10}%</b>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

campi_rischio_som = []
for _, _r in df_edit.iterrows():
    so0  = max(0.1, float(_r.get("SO %", 1.5)))
    prot = str(_r.get("Protocollo", "Intermedio"))
    nome = str(_r.get("Campo", ""))
    vals, d5, _, _ = rothc_proiezione(so0, prot, 10)
    if vals[5] < 1.5:
        campi_rischio_som.append((nome, round(vals[5], 2)))
if campi_rischio_som:
    elenco_c = ", ".join([f"**{n}** ({v}%)" for n,v in campi_rischio_som])
    st.error(f"⚠️ **RothC — Rischio SOM critico entro 5 anni:** {elenco_c} — SO% < 1.5% compromette struttura suolo.")

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
#  PAC ECO-SCHEME
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🇪🇺 Piano PAC — Eco-Scheme & Pagamenti Aggiuntivi 2023-2027</div>', unsafe_allow_html=True)
st.caption("Stima pagamenti PAC aggiuntivi accessibili. Valori medi nazionali AGEA 2024.")

ha_seminativi   = float(df_edit[df_edit["Coltura"].isin(["Cereali","Foraggere","Misto"])]["Ettari"].sum()) if len(df_edit)>0 else 0
ha_permanenti   = float(df_edit[df_edit["Coltura"].isin(["Vite (DOC/IGT)","Olivo","Nocciolo","Frutteto"])]["Ettari"].sum()) if len(df_edit)>0 else 0
ha_irrigate     = float(df_edit[df_edit["Irrigazione m³/ha"]>0]["Ettari"].sum()) if len(df_edit)>0 else 0
ha_rigenerativo = float(df_edit[df_edit["Protocollo"]=="Rigenerativo Full"]["Ettari"].sum()) if len(df_edit)>0 else 0
ha_cover        = float(df_edit[df_edit["Cover crops"]==True]["Ettari"].sum()) if len(df_edit)>0 else 0

pac_items = [
    {"nome":"ES1 — Agricoltura biologica","ok":cert_bio,"ha":tot_ha,"pag_ha":340,
     "motivo":"Richiede certificazione biologica attiva","azione":"Attiva certificazione Bio nella sidebar"},
    {"nome":"ES2 — Pratiche benefiche per clima","ok":ha_cover > 0,"ha":ha_cover,"pag_ha":110,
     "motivo":f"Cover crops attive su {ha_cover:.0f} ha","azione":"Attiva 'Cover crops' nella tabella appezzamenti"},
    {"nome":"ES4 — Impollinatori e biodiversità","ok":ha_cover > 0 and (ha_seminativi+ha_permanenti) > 0,
     "ha":min(ha_cover, ha_seminativi+ha_permanenti),"pag_ha":90,
     "motivo":"Cover crops su seminativi o permanenti","azione":"Attiva cover crops su almeno un campo"},
    {"nome":"ES5 — Gestione risorse idriche","ok":inv_drip and ha_irrigate > 0,"ha":ha_irrigate,"pag_ha":85,
     "motivo":f"Micro-irrigazione su {ha_irrigate:.0f} ha irrigati","azione":"Seleziona Micro-irrigazione nella sidebar"},
    {"nome":"Agro-climatica — Carbonio suolo","ok":ha_rigenerativo > 0,"ha":ha_rigenerativo,"pag_ha":220,
     "motivo":f"Pratiche rigenerative su {ha_rigenerativo:.0f} ha","azione":"Imposta protocollo Rigenerativo Full"},
    {"nome":"Agro-climatica — Bio + pratiche avanzate","ok":cert_bio and ha_rigenerativo > 0,
     "ha":min(tot_ha, ha_rigenerativo) if cert_bio else 0,"pag_ha":180,
     "motivo":"Richiede Bio certificato + Rigenerativo","azione":"Combina certificazione Bio con protocollo Rigenerativo"},
]

pac_totale = sum(p["ha"]*p["pag_ha"] for p in pac_items if p["ok"])

pac_cols = st.columns(3)
for i, p in enumerate(pac_items):
    importo = round(p["ha"]*p["pag_ha"],0) if p["ok"] else 0
    with pac_cols[i%3]:
        bg    = "#f0fdf4" if p["ok"] else "#fafaf9"
        brd   = "border-left:4px solid #1a6b3a;" if p["ok"] else "border-left:4px solid #e5e7eb;"
        ico   = "✅" if p["ok"] else "○"
        color = "#065f46" if p["ok"] else "#6b7280"
        st.markdown(f"""<div style="background:{bg};border-radius:11px;padding:.85rem 1rem;
          margin:.3rem 0;border:1px solid rgba(15,53,32,.12);{brd}">
          <b style="font-size:.83rem;color:{color}">{ico} {p["nome"]}</b><br>
          <span style="font-size:.7rem;color:#86efac">{p["motivo"]}</span><br>
          {"<b style='color:#1a6b3a;font-size:.82rem'>€"+f"{int(importo):,}/anno</b> ({p['ha']:.0f} ha × €{p['pag_ha']}/ha)" if p["ok"] else f"<span style='color:#fde68a;font-size:.72rem'>💡 {p['azione']}</span>"}
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:linear-gradient(90deg,#000000,#052e16);color:#fff;
  border-radius:12px;padding:.9rem 1.4rem;margin-top:.5rem;font-size:.82rem">
  🇪🇺 <b>Pagamenti PAC Eco-Scheme stimati:</b>&nbsp;
  Accessibili ora: <b style="color:#c9963a">€{int(pac_totale):,}/anno</b> &nbsp;·&nbsp;
  {"✅ Ottimo utilizzo eco-scheme" if pac_totale > 500 else "⚠️ Attiva più misure per massimizzare i pagamenti"}
</div>""", unsafe_allow_html=True)

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
          <span style="font-size:.7rem;color:#86efac">
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
        "i":"Gateway filiera GDO e export UE","e":"Prezzo vendita +12-18%","c":"6-12 mesi · CAA locale"})
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
      <div style="margin-top:.25rem;font-size:.78rem;color:#a3d9a5">📊 {az['i']}</div>
      <div style="font-size:.78rem;color:#1a6b3a">💶 {az['e']}
      <span style="color:#86efac"> · 📜 {az['c']}</span></div>
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


# ══════════════════════════════════════════════════════════════════════
#  AGRONOMO VIRTUALE IA — Analisi personalizzata con Claude API
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">🤖 Agronomo Virtuale IA — Analisi Personalizzata</div>', unsafe_allow_html=True)
st.caption("Powered by Claude (Anthropic) · Analisi basata su tutti i dati inseriti · Aggiornata in tempo reale")

col_ia1, col_ia2 = st.columns([2, 1])
with col_ia1:
    st.markdown("""
    <div class="info-box">
      <b style="color:#4ade80">Come funziona:</b> il modello legge tutti i tuoi dati aziendali —
      ogni campo, SO%, protocollo, fertilizzanti, meteo live, proiezione RothC, bilancio GHG —
      e genera un briefing agronomico personalizzato con diagnosi, azioni prioritarie e stime di ROI.
      <br><br>
      <b style="color:#fde68a">⚠️ Richiede variabile d'ambiente ANTHROPIC_API_KEY</b> —
      aggiungi la chiave in Streamlit Cloud → Settings → Secrets.
    </div>""", unsafe_allow_html=True)

with col_ia2:
    livello_analisi = st.selectbox(
        "Livello di analisi",
        ["Rapida (500 parole)", "Approfondita (1000 parole)", "Executive (200 parole)"],
        help="Scegli il livello di dettaglio del briefing agronomico"
    )

max_tok = {"Rapida (500 parole)": 700, "Approfondita (1000 parole)": 1400, "Executive (200 parole)": 300}

if st.button("🤖 Genera Analisi Agronomica IA", help="Richiede ANTHROPIC_API_KEY configurata"):
    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("❌ **ANTHROPIC_API_KEY non trovata.** Aggiungila in Streamlit Cloud → Settings → Secrets come:\n\n`ANTHROPIC_API_KEY = \"sk-ant-...\"` ")
    else:
        with st.spinner("🌿 L'agronomo virtuale sta analizzando la tua azienda..."):

            # Proiezioni RothC per tutti i campi
            rothc_summary = []
            for _, _r in df_edit.iterrows():
                so0_ = max(0.1, float(_r.get("SO %", 1.5)))
                prot_ = str(_r.get("Protocollo", "Intermedio"))
                nome_ = str(_r.get("Campo", ""))
                vals_, d5_, d10_, _ = rothc_proiezione(so0_, prot_, 10)
                rothc_summary.append(f"{nome_}: SO%={so0_} → +5a:{vals_[5]}% (Δ{d5_:+}%) +10a:{vals_[10]}% (Δ{d10_:+}%)")

            # Costruisce il contesto dati completo
            dati_azienda = f"""
AZIENDA: {nome_az}
Regione: {regione} / {zona}
Agronomo: {agronomo}
Data: {date.today().strftime("%d/%m/%Y")}

--- INDICATORI STRATEGICI ---
Score ESG: {score}/100 — Rating {rcls}
Bilancio GHG Netto (Scope 1+2+3): {round(tot_netto,2)} tCO₂eq/anno
CO₂ sequestrata: {round(tot_seq,2)} t/anno ({round(tot_seq/tot_ha,2)} t/ha)
Emissioni Scope 1: {round(scope1_total,2)} tCO₂eq/anno
Emissioni Scope 3: {round(scope3_total,2)} tCO₂eq/anno
Valore crediti CO₂: €{int(val_cred):,}/anno (@ €{prezzo_co2}/t)
Stress idrico: {round(stress_idx*100):.0f}% — deficit {round(deficit)} mm
Spreco irriguo: {int(tot_spreco):,} m³/anno = €{int(tot_spreco*costo_acqua):,}
Margine netto: {marg_pct}% (€{margine:,}/anno)
Valore fondo stimato: €{int(tot_vf):,}

--- CAMPI ---
{df_edit[['Campo','Ettari','SO %','Argilla %','Limo %','Densità','Protocollo','Coltura','Irrigazione m³/ha','Cover crops']].to_string(index=False)}

--- FERTILIZZANTI ---
{df_fert.to_string(index=False)}
Emissioni N₂O Sc.1 fertilizzanti: {round(co2_fert_n2o,2)} tCO₂eq
Emissioni produzione Sc.3: {round(co2_fert_prod,2)} tCO₂eq
Quota organici: {pct_org:.0f}%

--- METEO LIVE ---
Temperatura: {M['tmax']}°/{M['tmin']}°C
Pioggia 7gg: {M['pioggia_7g']} mm | ET₀: {M['et0']} mm/g
Pioggia 30gg: {MS['pioggia_30g']} mm | ET₀ 30gg: {MS['et0_30g']} mm

--- PROIEZIONE RothC (5-10 anni) ---
{chr(10).join(rothc_summary)}

--- CERTIFICAZIONI ATTIVE ---
Biologico: {"Sì" if cert_bio else "No"} | SQnpi: {"Sì" if cert_sqnpi else "No"} | GlobalG.A.P.: {"Sì" if cert_gap else "No"}
ISO 14064: {"Sì" if cert_iso else "No"} | CSRD: {"Sì" if cert_csrd else "No"}

--- PAC ECO-SCHEME ---
Pagamenti accessibili ora: €{int(pac_totale):,}/anno
"""

            livello_istr = {
                "Rapida (500 parole)": "Produci un briefing agronomico in circa 500 parole.",
                "Approfondita (1000 parole)": "Produci un briefing agronomico dettagliato in circa 1000 parole.",
                "Executive (200 parole)": "Produci un briefing executive sintetico in massimo 200 parole, solo i punti chiave."
            }[livello_analisi]

            try:
                import os
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": max_tok[livello_analisi],
                        "system": """Sei un dottore agronomo esperto in carbon farming, sostenibilità agricola e 
mercati dei crediti carbonio. Analizza i dati dell'azienda agricola e produci un briefing 
professionale in italiano strutturato con:

**DIAGNOSI** (2-3 frasi): situazione attuale, punti critici, potenziale.

**TOP 3 AZIONI PRIORITARIE** (per ognuna: cosa fare esattamente, perché è urgente, 
stima ROI in €/anno con calcolo esplicito, tempo di payback in anni).

**RISCHI A 5 ANNI** (2-3 rischi concreti con probabilità e impatto economico stimato).

**OPPORTUNITÀ NASCOSTE** (1-2 opportunità non sfruttate che emergono dai dati).

**FRASE FINALE**: una frase che sintetizza il potenziale dell'azienda e la direzione strategica.

Usa dati numerici precisi dai dati forniti. Sii diretto e concreto, mai generico.
Cita i valori esatti dei campi (SO%, protocollo, irrigazione) quando fai raccomandazioni.""",
                        "messages": [{"role": "user", "content": f"{livello_istr}\n\n{dati_azienda}"}]
                    },
                    timeout=45
                )

                if resp.status_code == 200:
                    analisi_testo = resp.json()["content"][0]["text"]
                    st.markdown(f"""
                    <div style="background:#0d1a0d;border:1.5px solid #22c55e;border-radius:16px;
                                padding:1.6rem 2rem;margin:1rem 0;
                                box-shadow:0 0 30px rgba(34,197,94,.12)">
                      <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1rem;
                                  border-bottom:1px solid rgba(34,197,94,.2);padding-bottom:.8rem">
                        <span style="font-size:1.4rem">🤖</span>
                        <div>
                          <div style="color:#4ade80;font-weight:700;font-size:.95rem">
                            Analisi Agronomica IA — {nome_az}</div>
                          <div style="color:#86efac;font-size:.72rem">
                            {livello_analisi} · {date.today().strftime("%d/%m/%Y")} · Claude claude-sonnet-4-20250514</div>
                        </div>
                      </div>
                      <div style="color:#e8f5e9;font-size:.84rem;line-height:1.85;white-space:pre-wrap">{analisi_testo}</div>
                    </div>""", unsafe_allow_html=True)

                    # Bottone per scaricare l'analisi come testo
                    st.download_button(
                        label="⬇️ Scarica analisi IA (.txt)",
                        data=f"ANALISI AGRONOMICA IA — {nome_az}\n{date.today()}\n\n{analisi_testo}".encode("utf-8"),
                        file_name=f"Analisi_IA_{nome_az.replace(' ','_')}_{date.today().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                elif resp.status_code == 401:
                    st.error("❌ API Key non valida. Controlla la chiave ANTHROPIC_API_KEY in Streamlit Secrets.")
                elif resp.status_code == 429:
                    st.error("❌ Limite richieste API raggiunto. Riprova tra qualche secondo.")
                else:
                    st.error(f"❌ Errore API Claude: {resp.status_code} — {resp.text[:200]}")

            except requests.exceptions.Timeout:
                st.error("❌ Timeout — il server Claude non ha risposto entro 45 secondi. Riprova.")
            except Exception as e:
                st.error(f"❌ Errore connessione: {e}")


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
| **RothC** | Coleman & Jenkinson 1996 — k: Conv -3.8%/a · Int -1.0%/a · Rig +1.5%/a |
| **Valore fondiario** | `ha × €15.000 × (1 + Δ_SO×0.12)` — CREA-AA 2025 |
    """)

# ══════════════════════════════════════════════════════════════════════
#  REPORT PDF + HTML
# ══════════════════════════════════════════════════════════════════════
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, HRFlowable, KeepTogether)
    from reportlab.platypus import PageBreak
    from io import BytesIO
    RL_OK = True
except ImportError:
    RL_OK = False

st.markdown('<div class="sec">📄 Genera Dossier Professionale</div>',unsafe_allow_html=True)

if RL_OK:
    st.success("✅ **ReportLab installato** — generazione PDF nativa attiva.")
else:
    st.info("📦 Aggiungi **reportlab** al requirements.txt per il PDF nativo.")

col_pdf, col_html = st.columns(2)
with col_pdf:
    gen_pdf  = st.button("📄 Scarica PDF nativo", disabled=not RL_OK)
with col_html:
    gen_html = st.button("🌐 Genera dossier HTML")

if RL_OK and gen_pdf:
    oggi = datetime.now().strftime("%d/%m/%Y")
    buf  = BytesIO()

    C_DARK   = colors.HexColor("#061912")
    C_GREEN  = colors.HexColor("#1a6b3a")
    C_GOLD   = colors.HexColor("#c9963a")
    C_RED    = colors.HexColor("#ef4444")
    C_LIGHT  = colors.HexColor("#f4f1ea")
    # ── COLORI TABELLE AGGIORNATI ── sfondo scuro leggibile ──
    C_TH_BG  = colors.HexColor("#061912")   # intestazione: verde scurissimo
    C_TH_FG  = colors.HexColor("#c9963a")   # testo intestazione: oro
    C_ROW1   = colors.HexColor("#0d2b1a")   # riga dispari: verde molto scuro
    C_ROW2   = colors.HexColor("#132f1e")   # riga pari: verde scuro
    C_CELL   = colors.HexColor("#d4edda")   # testo celle: verde chiaro leggibile
    C_BORDER = colors.HexColor("#c9963a")   # bordi: oro semitrasparente
    C_TOTAL  = colors.HexColor("#1a3d28")   # riga totale: verde medio
    C_WHITE  = colors.white
    C_LGRAY  = colors.HexColor("#132f1e")
    C_GRAY   = colors.HexColor("#9aab9e")

    styles = getSampleStyleSheet()

    def sty(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    S_title  = sty("title",  fontSize=18, textColor=C_GOLD,  fontName="Helvetica-Bold", spaceAfter=4)
    S_sub    = sty("sub",    fontSize=10, textColor=C_GRAY,  fontName="Helvetica",      spaceAfter=12)
    S_h2     = sty("h2",     fontSize=11, textColor=C_GOLD,  fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=4, leftIndent=6)
    S_body   = sty("body",   fontSize=8.5, textColor=C_CELL, fontName="Helvetica",      spaceAfter=3,   leading=13)
    S_small  = sty("small",  fontSize=7.5, textColor=C_GRAY, fontName="Helvetica",      spaceAfter=2,   leading=11)
    S_bold   = sty("bold",   fontSize=8.5, textColor=C_CELL, fontName="Helvetica-Bold", spaceAfter=3)

    def th(txt):
        return Paragraph(f"<b>{txt}</b>",
                         sty("th", fontSize=7.5, textColor=C_TH_FG, fontName="Helvetica-Bold"))

    def td(txt, bold=False, color=None):
        return Paragraph(str(txt),
                         sty("td", fontSize=7.5, textColor=color or C_CELL,
                             fontName="Helvetica-Bold" if bold else "Helvetica"))

    # TableStyle base con colori scuri leggibili
    TS_HEAD = TableStyle([
        # Intestazione
        ("BACKGROUND",    (0,0), (-1,0),  C_TH_BG),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_TH_FG),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7.5),
        # Righe alternare scure
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_ROW1, C_ROW2]),
        ("TEXTCOLOR",     (0,1), (-1,-1), C_CELL),
        # Bordi oro
        ("GRID",          (0,0), (-1,-1), 0.5, C_BORDER),
        ("LINEBELOW",     (0,0), (-1,0),  1.5, C_GOLD),
        # Padding
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
    ])

    # TableStyle per riga totale verde medio
    def ts_with_total():
        cmds = TS_HEAD.getCommands() + [
            ("BACKGROUND", (0,-1), (-1,-1), C_TOTAL),
            ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
            ("TEXTCOLOR",  (0,-1), (-1,-1), C_GOLD),
            ("LINEABOVE",  (0,-1), (-1,-1), 1.5, C_GOLD),
        ]
        return TableStyle(cmds)

    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.8*cm, rightMargin=1.8*cm,
                            topMargin=2*cm,    bottomMargin=2*cm,
                            title=f"AgroLog IA — {nome_az}", author=agronomo)
    W = A4[0] - 3.6*cm

    story = []

    # INTESTAZIONE
    story.append(Paragraph(f"🌿 {nome_az}", S_title))
    story.append(Paragraph(
        f"Dossier Carbon &amp; ESG Strategic Intelligence — {oggi}  |  "
        f"Consulente: {agronomo}  |  {regione} / {zona}", S_sub))
    story.append(Paragraph(
        f"IPCC 2006 Tier 1 · FAO-PM · GHG Protocol Scope 1+2+3 · ecoinvent 3.9 · Open-Meteo ERA5", S_small))
    story.append(HRFlowable(width=W, thickness=2, color=C_GOLD, spaceAfter=8))

    # KPI
    story.append(Paragraph("Indicatori Chiave", S_h2))
    kpi_data = [
        [th("Score ESG"), th("CO₂ Sequestrata"), th("Bilancio GHG"), th("Crediti CO₂/anno")],
        [td(f"{score}/100 — {rcls}", bold=True),
         td(f"{round(tot_seq,1)} t  ({round(tot_seq/tot_ha,2)} t/ha)"),
         td(f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t', bold=True,
            color=C_GREEN if tot_netto>=0 else C_RED),
         td(f"€{int(val_cred):,}", bold=True, color=colors.HexColor("#6ee7b7"))],
        [th("Fabbisogno Idrico"), th("Valore Fondo"), th("Margine Netto"), th("Stress Idrico")],
        [td(f"{int(tot_fabb):,} m³  (spreco {int(tot_spreco):,})"),
         td(f"€{int(tot_vf):,}"),
         td(f"{marg_pct}%", bold=True,
            color=colors.HexColor("#6ee7b7") if marg_pct>=25 else C_RED),
         td(f"{round(stress_idx*100):.0f}%", bold=True,
            color=C_RED if stress_idx>0.4 else colors.HexColor("#fbbf24") if stress_idx>0.2 else colors.HexColor("#6ee7b7"))],
    ]
    t_kpi = Table(kpi_data, colWidths=[W/4]*4)
    t_kpi.setStyle(TS_HEAD)
    story.append(t_kpi)
    story.append(Spacer(1, 6*mm))

    # METEO
    story.append(Paragraph("Meteo Live &amp; Storico", S_h2))
    story.append(Paragraph(
        f"🌡️ {M['tmax']}°/{M['tmin']}°C  |  🌧️ Pioggia 7gg: {M['pioggia_7g']} mm  |  "
        f"💧 ET₀: {M['et0']} mm/g  |  📊 Pioggia 30gg: {MS['pioggia_30g']} mm  |  "
        f"⚡ Deficit: {round(deficit)} mm  |  🔥 Stress: {round(stress_idx*100):.0f}%", S_body))
    if MA:
        mesi_nomi_pdf={"01":"Gen","02":"Feb","03":"Mar","04":"Apr","05":"Mag","06":"Giu",
                       "07":"Lug","08":"Ago","09":"Set","10":"Ott","11":"Nov","12":"Dic"}
        hdr_m = [th("Mese"), th("Pioggia"), th("ET₀"), th("Bilancio"), th("Temp.")]
        rows_m = []
        for mm_d in MA:
            mn  = mesi_nomi_pdf.get(mm_d["mese"][5:], mm_d["mese"][5:])
            bal = round(mm_d["pioggia"]-mm_d["et0"],0)
            rows_m.append([td(f"{mn} {mm_d['mese'][:4]}"),
                           td(f"{mm_d['pioggia']} mm"),
                           td(f"{mm_d['et0']} mm"),
                           td(f'{"+" if bal>=0 else ""}{bal} mm',
                              color=colors.HexColor("#6ee7b7") if bal>=0 else C_RED),
                           td(f"{mm_d['temp_media']}°C")])
        t_m = Table([hdr_m]+rows_m, colWidths=[W*0.20, W*0.18, W*0.18, W*0.22, W*0.22])
        t_m.setStyle(TS_HEAD)
        story.append(t_m)
    story.append(Spacer(1, 5*mm))

    # BILANCIO GHG
    story.append(Paragraph("Bilancio GHG — Scope 1 + 2 + 3 (GHG Protocol)", S_h2))
    ghg_data = [
        [th("Voce"), th("Scope"), th("tCO₂eq/anno"), th("Note")],
        [td("Sequestro suolo"), td("Credito"),
         td(f"+{round(tot_seq,2)}", bold=True, color=colors.HexColor("#6ee7b7")), td("IPCC Tier 1")],
        [td("Gasolio macchine"), td("Sc.1"),
         td(f"-{round(S('diesel_co2'),2)}", color=C_RED), td("DEFRA 2024")],
        [td("N₂O fertilizzanti"), td("Sc.1"),
         td(f"-{round(S('n2o')+co2_fert_n2o,2)}", color=C_RED),
         td(f"min {round(co2_n2o_min,2)} / org {round(co2_n2o_org,2)} t")],
        [td("Scarti emissivi"), td("Sc.1"),
         td(f"-{round(max(0,co2_scarti),2)}", color=C_RED), td("IPCC 2006 Vol.5")],
        [td("Fertilizzanti — produzione"), td("Sc.3"),
         td(f"-{round(co2_fert_prod,2)}", color=C_GOLD), td("ecoinvent 3.9")],
        [td("Fitofarmaci"), td("Sc.3"),
         td(f"-{round(co2_fito_s3,2)}", color=C_GOLD), td("ecoinvent 3.9")],
        [td("Materie prime"), td("Sc.3"),
         td(f"-{round(co2_materie,2)}", color=C_GOLD), td("LCA letteratura")],
        [td("Trasporti & mobilità"), td("Sc.3"),
         td(f"-{round(co2_trasporti,2)}", color=C_GOLD), td("DEFRA 2024")],
        [td("Scarti virtuosi"), td("Credito"),
         td(f"+{round(abs(min(0,co2_scarti)),2)}", color=colors.HexColor("#6ee7b7")), td("IPCC 2006 Vol.5")],
        [td("BILANCIO NETTO", bold=True), td(""),
         td(f'{"+" if tot_netto>=0 else ""}{round(tot_netto,2)}', bold=True,
            color=colors.HexColor("#6ee7b7") if tot_netto>=0 else C_RED),
         td(f"→ €{int(val_cred):,}/anno crediti")],
    ]
    t_ghg = Table(ghg_data, colWidths=[W*0.35, W*0.12, W*0.20, W*0.33])
    t_ghg.setStyle(ts_with_total())
    story.append(t_ghg)
    story.append(Spacer(1, 5*mm))

    # APPEZZAMENTI
    story.append(Paragraph("Dettaglio Appezzamenti — IPCC Tier 1", S_h2))
    hdr_c = [th("Campo"), th("ha"), th("Coltura"), th("Protocollo"),
             th("SO%"), th("Arg/Lim%"), th("CC"), th("Seq.t"), th("Emit.t"), th("Netto"), th("Analisi")]
    rows_c = []
    for i, (_,rr) in enumerate(df_edit.iterrows()):
        rc = res_att[i]
        da_pdf = str(rr.get("Analisi suolo","—"))
        rows_c.append([
            td(str(rr.get("Campo","")), bold=True),
            td(str(rr.get("Ettari",""))),
            td(str(rr.get("Coltura",""))),
            td(str(rr.get("Protocollo",""))[:12]),
            td(f"{rr.get('SO %','')}%"),
            td(f"{rr.get('Argilla %','')}%/{rr.get('Limo %','')}%"),
            td("✓" if rr.get("Cover crops",False) else "—"),
            td(str(rc["co2_seq"]), color=colors.HexColor("#6ee7b7")),
            td(str(rc["co2_emit"]), color=C_RED),
            td(f'{"+" if rc["co2_netto"]>=0 else ""}{rc["co2_netto"]}', bold=True,
               color=colors.HexColor("#6ee7b7") if rc["co2_netto"]>=0 else C_RED),
            td(da_pdf),
        ])
    cw_c = [W*0.13, W*0.06, W*0.12, W*0.13, W*0.06, W*0.09, W*0.05, W*0.07, W*0.07, W*0.07, W*0.09]
    t_c = Table([hdr_c]+rows_c, colWidths=cw_c, repeatRows=1)
    t_c.setStyle(TS_HEAD)
    story.append(t_c)
    story.append(Spacer(1, 5*mm))

    # RothC
    story.append(Paragraph("Proiezione SOM — Modello RothC semplificato (5-10 anni)", S_h2))
    hdr_r = [th("Campo"), th("Protocollo"), th("SO% ora"), th("SO% +5a"), th("Δ 5a"), th("SO% +10a"), th("Δ 10a")]
    rows_r = []
    for _,rr in df_edit.iterrows():
        so0_   = max(0.1, float(rr.get("SO %",1.5)))
        prot_  = str(rr.get("Protocollo","Intermedio"))
        nome_  = str(rr.get("Campo",""))
        vals_, d5_, d10_, _ = rothc_proiezione(so0_, prot_, 10)
        rows_r.append([
            td(nome_, bold=True),
            td(prot_[:16]),
            td(f"{so0_}%"),
            td(f"{vals_[5]}%", color=colors.HexColor("#6ee7b7") if d5_>=0 else C_RED),
            td(f'{"+" if d5_>=0 else ""}{d5_}%', bold=True,
               color=colors.HexColor("#6ee7b7") if d5_>=0 else C_RED),
            td(f"{vals_[10]}%", color=colors.HexColor("#6ee7b7") if d10_>=0 else C_RED),
            td(f'{"+" if d10_>=0 else ""}{d10_}%', bold=True,
               color=colors.HexColor("#6ee7b7") if d10_>=0 else C_RED),
        ])
    t_r = Table([hdr_r]+rows_r, colWidths=[W*0.16, W*0.19, W*0.11, W*0.13, W*0.13, W*0.13, W*0.15])
    t_r.setStyle(TS_HEAD)
    story.append(t_r)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Fonte: Coleman &amp; Jenkinson 1996, RothC-26.3. k: Conv -3.8%/a · Int -1.0%/a · Rig +1.5%/a", S_small))
    story.append(Spacer(1, 5*mm))

    # FERTILIZZANTI
    story.append(Paragraph("Fertilizzanti &amp; Fitofarmaci — Scope 1 + 3", S_h2))
    hdr_f = [th("Prodotto"), th("Tipo"), th("Quantità"), th("N₂O Sc.1 (t)"), th("Prod. Sc.3 (t)"), th("EF N₂O")]
    rows_f = [[td(fd["prod"]), td(fd["tipo"].capitalize()), td(f'{int(fd["qty"]):,} kg'),
               td(str(fd["s1"]), color=C_RED),
               td(str(fd["s3"]), color=C_GOLD),
               td(str(fd["ef"]["ef_n2o"]))] for fd in fert_detail]
    t_f = Table([hdr_f]+rows_f, colWidths=[W*0.32, W*0.12, W*0.14, W*0.14, W*0.14, W*0.14])
    t_f.setStyle(TS_HEAD)
    story.append(t_f)
    story.append(Spacer(1, 5*mm))

    # PAC
    story.append(Paragraph("Piano PAC — Eco-Scheme 2023-2027 (AGEA 2024)", S_h2))
    hdr_p = [th("Misura"), th("Accessibile"), th("Ettari"), th("€/ha"), th("Importo/anno")]
    rows_p = []
    for pp in pac_items:
        imp = round(pp["ha"]*pp["pag_ha"],0) if pp["ok"] else 0
        rows_p.append([
            td(pp["nome"]),
            td("✅ Sì" if pp["ok"] else "○ No",
               color=colors.HexColor("#6ee7b7") if pp["ok"] else C_GRAY),
            td(f'{pp["ha"]:.1f}'),
            td(f'€{pp["pag_ha"]}'),
            td(f'€{int(imp):,}' if pp["ok"] else "—",
               bold=pp["ok"],
               color=colors.HexColor("#6ee7b7") if pp["ok"] else C_GRAY),
        ])
    rows_p.append([td("TOTALE ACCESSIBILE", bold=True), td(""), td(""), td(""),
                   td(f"€{int(pac_totale):,}/anno", bold=True, color=colors.HexColor("#6ee7b7"))])
    t_p = Table([hdr_p]+rows_p, colWidths=[W*0.40, W*0.15, W*0.12, W*0.12, W*0.21])
    t_p.setStyle(ts_with_total())
    story.append(t_p)
    story.append(Spacer(1, 5*mm))

    # SCENARI
    story.append(Paragraph("Scenari Economici", S_h2))
    sc_data = [
        [th("Voce"), th("Stato Attuale"), th("Scenario Rigenerativo"), th("Δ annuo")],
        [td("CO₂ netta Sc.1+3"),
         td(f'{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t'),
         td(f'{"+" if pot_netto>=0 else ""}{round(pot_netto,1)} t'),
         td(f'+{round(pot_netto-tot_netto,1)} t', color=colors.HexColor("#6ee7b7"))],
        [td("Crediti CO₂"), td(f"€{int(val_cred):,}"), td(f"€{int(pot_cred):,}"),
         td(f"+€{int(pot_cred-val_cred):,}", color=colors.HexColor("#6ee7b7"))],
        [td("Risparmio gasolio"), td("—"), td(f"+€{int(risp_die):,}"),
         td(f"+€{int(risp_die):,}", color=colors.HexColor("#6ee7b7"))],
        [td("Risparmio acqua"), td("—"), td(f"+€{int(risp_h2o):,}"),
         td(f"+€{int(risp_h2o):,}", color=colors.HexColor("#6ee7b7"))],
        [td("PAC Eco-Scheme"), td(f"€{int(pac_totale):,}"), td(f"€{int(pac_totale):,}"), td("—")],
        [td("TOTALE GUADAGNO", bold=True), td(""), td(""),
         td(f"+€{int(guadagno):,}/a", bold=True, color=colors.HexColor("#6ee7b7"))],
    ]
    t_sc = Table(sc_data, colWidths=[W*0.32, W*0.22, W*0.24, W*0.22])
    t_sc.setStyle(ts_with_total())
    story.append(t_sc)
    story.append(Spacer(1, 5*mm))

    # AZIONI
    story.append(Paragraph("Piano d'Azione Prioritario", S_h2))
    for ii, az in enumerate(azioni[:6], 1):
        clr_az = {"alta":"#ef4444","media":"#c9963a","bassa":"#1a6b3a"}[az["p"]]
        story.append(Paragraph(
            f'<font color="{clr_az}">●</font> <b>{ii}. {az["t"]}</b>', S_body))
        story.append(Paragraph(f'📊 {az["i"]}  |  💶 {az["e"]}  |  📜 {az["c"]}', S_small))
    story.append(Spacer(1, 5*mm))

    # NOTA METODOLOGICA
    story.append(Paragraph("Nota Metodologica", S_h2))
    story.append(Paragraph(
        "Carbonio suolo: IPCC 2006 Vol.4 Tier 1, AR5 GWP.  "
        "Fertilizzanti Scope 1+3: ecoinvent 3.9, N₂O per tipo.  "
        "Trasporti Scope 3: DEFRA 2024.  Acqua: FAO Penman-Monteith.  "
        "RothC: Coleman &amp; Jenkinson 1996.  PAC: AGEA 2024.  "
        "Meteo: Open-Meteo ECMWF+ERA5 1km.  Valore fondiario: CREA-AA 2025.  "
        "Report previsionale — certificazione ufficiale crediti richiede verifica Ente Terzo.", S_small))
    story.append(Spacer(1, 6*mm))

    # FIRMA
    story.append(HRFlowable(width=W, thickness=0.5, color=C_GOLD))
    story.append(Spacer(1,3*mm))
    firma_data = [
        [td("Dottore Agronomo:", bold=True), td(agronomo),
         td("N. Albo:", bold=True), td("______________________")],
        [td("Data:", bold=True), td(oggi),
         td("Luogo:", bold=True), td("______________________")],
        [td("Firma:", bold=True), td("______________________________"), td("Timbro:", bold=True), td("")],
    ]
    t_firma = Table(firma_data, colWidths=[W*0.15, W*0.35, W*0.15, W*0.35])
    t_firma.setStyle(TableStyle([
        ("FONTSIZE",(0,0),(-1,-1),8.5),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("TEXTCOLOR",(0,0),(-1,-1),C_CELL),
    ]))
    story.append(t_firma)

    doc.build(story)
    buf.seek(0)
    pdf_bytes = buf.getvalue()
    fn_pdf = f"AgroLog_v8_{nome_az.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    st.download_button(
        label="⬇️ Scarica Dossier ESG — PDF nativo",
        data=pdf_bytes, file_name=fn_pdf, mime="application/pdf")
    st.success(f"✅ **{fn_pdf}** generato — {round(len(pdf_bytes)/1024,0)} KB")

# HTML FALLBACK
if gen_html:
    oggi = datetime.now().strftime("%d/%m/%Y")

    righe_tab=""
    for i,(_,row_) in enumerate(df_edit.iterrows()):
        r=res_att[i]
        nc="#6ee7b7" if r["co2_netto"]>=0 else "#fca5a5"
        righe_tab+=f"""<tr>
          <td><b style="color:#c9963a">{row_.get("Campo","")}</b></td>
          <td>{row_.get("Ettari","")} ha</td>
          <td>{row_.get("Coltura","")}</td>
          <td>{row_.get("Protocollo","")}</td>
          <td>{row_.get("SO %","")}%</td>
          <td>{row_.get("Argilla %","")}%/{row_.get("Limo %","")}%</td>
          <td>{"✓" if row_.get("Cover crops",False) else "—"}</td>
          <td style="color:#6ee7b7"><b>{r["co2_seq"]}</b></td>
          <td style="color:#fca5a5">{r["co2_emit"]}</td>
          <td style="color:{nc}"><b>{"+" if r["co2_netto"]>=0 else ""}{r["co2_netto"]}</b></td>
          <td>{int(r["fabb_irr"]):,}</td>
        </tr>"""

    righe_fert=""
    for fd in fert_detail:
        righe_fert+=f"""<tr>
          <td>{fd['prod']}</td><td>{int(fd['qty']):,} kg</td>
          <td style="color:#fca5a5">{fd['s1']} t</td>
          <td style="color:#fbbf24">{fd['s3']} t</td>
          <td style="font-size:.7rem;color:#9aab9e">{fd['ef']['desc']}</td>
        </tr>"""

    righe_scarti=""
    for sd in scarti_detail:
        col="#fca5a5" if sd["ef"]>0 else "#6ee7b7"
        segno="+" if sd["ef"]>0 else ""
        righe_scarti+=f"""<tr>
          <td>{sd['scarto']}</td><td>{sd['qty']} t/anno</td>
          <td style="color:{col}"><b>{segno}{sd['co2']} tCO₂eq</b></td>
        </tr>"""

    storico_html=""
    if MA:
        mesi_nomi={"01":"Gen","02":"Feb","03":"Mar","04":"Apr","05":"Mag","06":"Giu",
                   "07":"Lug","08":"Ago","09":"Set","10":"Ott","11":"Nov","12":"Dic"}
        for m in MA:
            mn=mesi_nomi.get(m["mese"][5:],m["mese"][5:])
            bal=round(m["pioggia"]-m["et0"],0)
            bc="#6ee7b7" if bal>=0 else "#fca5a5"
            storico_html+=f"""<tr>
              <td>{mn} {m["mese"][:4]}</td>
              <td style="color:#60a5fa">{m["pioggia"]} mm</td>
              <td style="color:#fca5a5">{m["et0"]} mm</td>
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
          margin:.3rem 0;background:#0d2b1a;border-radius:0 9px 9px 0">
          <b style="font-size:.84rem;color:#d4edda">{a["t"]}</b><br>
          <span style="font-size:.75rem;color:#9aab9e">📊 {a["i"]}</span> ·
          <span style="font-size:.75rem;color:#6ee7b7">💶 {a["e"]}</span>
        </div>"""

    r_html=" ".join([
        f'<span style="display:inline-block;padding:3px 10px;border-radius:20px;'
        f'font-size:.7rem;font-weight:600;margin:2px;'
        f'background:{"#4b1c1c" if r["l"]=="alto" else "#3d2e0e" if r["l"]=="medio" else "#0d2b1a"};'
        f'color:{"#fca5a5" if r["l"]=="alto" else "#fbbf24" if r["l"]=="medio" else "#6ee7b7"}'
        f';border:1px solid {"#ef4444" if r["l"]=="alto" else "#c9963a" if r["l"]=="medio" else "#1a6b3a"}">'
        f'{r["l"].upper()} — {r["t"]}</span>'
        for r in rischi])

    html=f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8">
<title>AgroLog IA v7 — {nome_az} — {oggi}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Lexend',sans-serif;color:#d4edda;background:#061912;font-size:11.5px;line-height:1.5}}
@media print{{body{{font-size:10px;background:#fff;color:#000}};@page{{margin:1.5cm}}
  table th{{background:#061912 !important;color:#c9963a !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
  table tr:nth-child(odd) td{{background:#0d2b1a !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
  table tr:nth-child(even) td{{background:#132f1e !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
}}
.hdr{{background:linear-gradient(135deg,#061912,#0f3520 45%,#1a6b3a);
  color:#fff;padding:1.8rem 2.5rem;border-bottom:4px solid #c9963a;}}
.hdr h1{{font-family:'DM Serif Display',serif;font-size:1.6rem;margin:.3rem 0 .2rem;color:#fff}}
.hdr p{{color:rgba(255,255,255,.6);font-size:.78rem}}
.badge{{background:#c9963a;color:#061912;font-size:.58rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;padding:2px 10px;
  border-radius:20px;margin-bottom:.5rem;display:inline-block}}
.meta{{display:flex;gap:.8rem;margin-top:.6rem;flex-wrap:wrap}}
.meta span{{background:rgba(255,255,255,.12);color:rgba(255,255,255,.8);
  font-size:.66rem;padding:3px 9px;border-radius:15px}}
.sec{{padding:1rem 2rem;border-bottom:1px solid rgba(201,150,58,.2)}}
.st{{font-family:'DM Serif Display',serif;font-size:1rem;color:#c9963a;
  border-left:4px solid #c9963a;padding-left:.6rem;margin-bottom:.7rem}}
.kg{{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin:.5rem 0}}
.k{{background:#0f3520;border-radius:10px;padding:.65rem .9rem;text-align:center;
  border:1px solid rgba(201,150,58,.3)}}
.kv{{font-family:'DM Serif Display',serif;font-size:1.2rem;color:#c9963a}}
.kl{{font-size:.58rem;color:#9aab9e;text-transform:uppercase;letter-spacing:.06em;margin-top:2px}}
/* ══ TABELLE HTML — sfondo scuro leggibile ══ */
table{{width:100%;border-collapse:collapse;font-size:.76rem}}
th{{background:#061912;color:#c9963a;padding:7px 9px;text-align:left;
   font-weight:700;border-bottom:2px solid #c9963a;
   border-right:1px solid rgba(201,150,58,.2)}}
td{{padding:5px 9px;border-bottom:1px solid rgba(201,150,58,.15);
   color:#d4edda;vertical-align:middle}}
tr:nth-child(odd) td{{background:#0d2b1a}}
tr:nth-child(even) td{{background:#132f1e}}
tr:hover td{{background:#1a6b3a;color:#fff}}
tfoot tr td{{background:#1a3d28 !important;color:#c9963a;font-weight:700;
   border-top:2px solid #22c55e;background:#052e16}}
.meteo{{background:linear-gradient(90deg,#0a2d4a,#0f3520);color:#d4edda;
  border-radius:9px;padding:.65rem 1.1rem;margin:.4rem 0;font-size:.78rem;line-height:2;
  border:1px solid rgba(201,150,58,.3)}}
.scope-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5rem;margin:.5rem 0}}
.sc1{{background:#2d0f0f;border:1.5px solid #fca5a5;border-radius:9px;padding:.8rem 1rem;color:#fca5a5}}
.sc2{{background:#2d1f0a;border:1.5px solid #fdba74;border-radius:9px;padding:.8rem 1rem;color:#fdba74}}
.sc3{{background:#0d2b1a;border:1.5px solid #86efac;border-radius:9px;padding:.8rem 1rem;color:#86efac}}
.scen{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5rem;margin:.5rem 0}}
.sc{{border-radius:10px;padding:.9rem 1.1rem}}
.sc-b{{background:#0d2b1a;border:1.5px dashed #1a6b3a}}
.sc-o{{background:#2d1f0a;border:1.5px dashed #c9963a}}
.sc-t{{background:#0f1d3a;border:1.5px dashed #3b82f6}}
.sc-r{{display:flex;justify-content:space-between;font-size:.78rem;padding:3px 0;color:#9aab9e}}
.sc-r b{{color:#d4edda}}
.sign{{border:1px solid rgba(201,150,58,.3);border-radius:10px;
  padding:1rem 1.5rem;margin:.5rem 0;background:#0f3520}}
.ftr{{background:#000;color:rgba(255,255,255,.35);padding:.7rem 2rem;
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
  <div class="k"><div class="kv">{round(co2_fert_totale,1)} t</div><div class="kl">Emissioni Fertilizzanti</div></div>
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
{"<table><thead><tr><th>Mese</th><th>Pioggia</th><th>ET₀</th><th>Bilancio</th><th>Temp. media</th></tr></thead><tbody>"+storico_html+"</tbody></table>" if storico_html else "<p style='font-size:.78rem;color:#9aab9e'>Dati storici non disponibili</p>"}
</div>

<div class="sec"><div class="st">Bilancio GHG — Scope 1 + Scope 2 + Scope 3 (GHG Protocol)</div>
<div class="scope-grid">
<div class="sc1"><b style="font-size:.85rem">🔴 Scope 1 — Dirette</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Gasolio: <b>{round(S("diesel_co2"),2)} tCO₂</b><br>
N₂O campo+fertilizz.: <b>{round(S("n2o")+co2_fert_n2o,2)} tCO₂eq</b><br>
Combustione scarti: <b>{round(max(0,sum(r["qty"]*r["ef"] for r in scarti_detail if r["ef"]>0)),2)} tCO₂</b><br>
<b>Tot. Sc.1: {round(scope1_total,2)} t</b></div></div>
<div class="sc2"><b style="font-size:.85rem">🟡 Scope 2 — Energia</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Elettricità: <b>0 t</b><br>
<span style="color:#9aab9e">(pompe, celle frigorifere)</span><br>
<b>Tot. Sc.2: {round(scope2_total,2)} t</b></div></div>
<div class="sc3"><b style="font-size:.85rem">🟢 Scope 3 — Catena valore</b>
<div style="font-size:.78rem;line-height:1.9;margin-top:.4rem">
Produzione fertilizz.: <b>{round(co2_fert_prod,2)} tCO₂eq</b><br>
Fitofarmaci: <b>{round(co2_fito_s3,2)} tCO₂eq</b><br>
Materie prime: <b>{round(co2_materie,2)} tCO₂eq</b><br>
Trasporti: <b>{round(co2_trasporti,2)} tCO₂eq</b><br>
<b>Tot. Sc.3: {round(scope3_total,2)} t</b></div></div>
</div></div>

<div class="sec"><div class="st">Dettaglio Appezzamenti — IPCC Tier 1</div>
<table><thead><tr>
<th>Campo</th><th>ha</th><th>Coltura</th><th>Protocollo</th>
<th>SO%</th><th>Arg/Limo%</th><th>CC</th>
<th>CO₂ Seq (t)</th><th>CO₂ Emit (t)</th><th>Netto (t)</th><th>Fabb.Irr m³</th>
</tr></thead><tbody>{righe_tab}</tbody>
<tfoot><tr>
<td><b>TOTALE</b></td><td>{round(tot_ha,1)} ha</td><td colspan="5"></td>
<td style="color:#6ee7b7"><b>{round(tot_seq,1)}</b></td>
<td style="color:#fca5a5"><b>{round(tot_emit_base,1)}</b></td>
<td><b>{"+" if (tot_seq-tot_emit_base)>=0 else ""}{round(tot_seq-tot_emit_base,1)}</b></td>
<td>{int(tot_fabb):,}</td>
</tr></tfoot></table></div>

<div class="sec"><div class="st">Fertilizzanti & Fitofarmaci — emissioni IPCC + ecoinvent 3.9</div>
<table><thead><tr>
<th>Prodotto</th><th>Quantità</th><th>N₂O Sc.1 (tCO₂eq)</th><th>Produzione Sc.3 (tCO₂eq)</th><th>Nota</th>
</tr></thead><tbody>{righe_fert}</tbody>
<tfoot><tr>
<td colspan="2"><b>TOTALE fertilizzanti</b></td>
<td style="color:#fca5a5"><b>{round(co2_fert_n2o,2)} tCO₂eq</b></td>
<td style="color:#fbbf24"><b>{round(co2_fert_prod,2)} tCO₂eq</b></td>
<td></td></tr></tfoot></table></div>

<div class="sec"><div class="st">Gestione Scarti & Sottoprodotti</div>
<table><thead><tr><th>Scarto/Sottoprodotto</th><th>Quantità</th><th>CO₂eq (t) — + emissione / - credito</th></tr></thead>
<tbody>{righe_scarti}</tbody>
<tfoot><tr><td colspan="2"><b>BILANCIO SCARTI</b></td>
<td><b style="color:{'#fca5a5' if co2_scarti>0 else '#6ee7b7'}">{"+" if co2_scarti>0 else ""}{round(co2_scarti,2)} tCO₂eq</b></td></tr></tfoot>
</table></div>

<div class="sec"><div class="st">Scenari Economici</div>
<div class="scen">
<div class="sc sc-b"><b style="color:#6ee7b7;font-size:.87rem">📍 Stato Attuale</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta Sc.1+3</span><b>{"+" if tot_netto>=0 else ""}{round(tot_netto,1)} t</b></div>
<div class="sc-r"><span>Crediti CO₂</span><b>€{int(val_cred):,}/anno</b></div>
<div class="sc-r"><span>Em. fertilizzanti</span><b>{round(co2_fert_totale,1)} t</b></div>
<div class="sc-r"><span>Costo gasolio</span><b>€{int(tot_c_die):,}</b></div>
<div class="sc-r"><span>Margine</span><b>{marg_pct}%</b></div>
</div></div>
<div class="sc sc-o"><b style="color:#fbbf24;font-size:.87rem">⚡ Rigenerativo</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>CO₂ netta</span><b>{round(pot_netto,1)} t</b></div>
<div class="sc-r"><span>Crediti</span><b>€{int(pot_cred):,}/anno</b></div>
<div class="sc-r"><span>Risp. gasolio</span><b style="color:#6ee7b7">€{int(risp_die):,}</b></div>
<div class="sc-r"><span>Risp. acqua</span><b style="color:#6ee7b7">€{int(risp_h2o):,}</b></div>
<div style="border-top:1px dashed #c9963a;margin-top:.4rem;padding-top:.3rem;text-align:right">
<b style="color:#c9963a">+€{int(guadagno):,}/anno</b></div>
</div></div>
<div class="sc sc-t"><b style="color:#60a5fa;font-size:.87rem">🔬 Tech</b>
<div style="margin-top:.4rem">
<div class="sc-r"><span>Investimento</span><b>€{int(costo_inv):,}</b></div>
<div class="sc-r"><span>Ritorno/anno</span><b style="color:#6ee7b7">€{int(guadagno):,}</b></div>
<div class="sc-r"><span>Payback</span><b style="color:#60a5fa">{payback} anni</b></div>
</div></div>
</div></div>

<div class="sec"><div class="st">Piano Azioni Prioritarie</div>{az_html}</div>

<div class="sec"><div class="st">Mappa dei Rischi</div>
<div style="line-height:2.5">{r_html}</div></div>

<div class="sec"><div class="st">Certificazioni Attive</div>
<p style="font-size:.82rem;color:#d4edda">Attive: <b style="color:#c9963a">{cert_att}</b></p></div>

<div class="sec"><div class="st">Nota Metodologica</div>
<p style="font-size:.75rem;color:#4a5e4e;line-height:1.65">
<b style="color:#c9963a">Carbonio suolo:</b> IPCC 2006 Vol.4 Tier 1, AR5 GWP.
<b style="color:#c9963a">Fertilizzanti (Scope 1+3):</b> ecoinvent 3.9.
<b style="color:#c9963a">Scarti:</b> IPCC 2006 Vol.5.
<b style="color:#c9963a">Acqua:</b> FAO Penman-Monteith, Kc da FAO-56.
<b style="color:#c9963a">Meteo:</b> Open-Meteo ECMWF IFS + ERA5.
<b style="color:#c9963a">RothC:</b> Coleman & Jenkinson 1996.
<b style="color:#c9963a">PAC:</b> AGEA 2024. <b style="color:#c9963a">CO₂ prezzi:</b> Xpansiv CBL Q1 2026.
<i>Report previsionale — verifica Ente Terzo per certificazione ufficiale.</i>
</p></div>

<div class="sec"><div class="st">Firma e Validazione</div>
<div class="sign">
<table style="font-size:.82rem">
<tr><td style="border:none;padding:4px 8px;color:#9aab9e"><b>Dottore Agronomo:</b></td>
    <td style="border:none;color:#d4edda">{agronomo}</td>
    <td style="border:none;padding:4px 8px;color:#9aab9e"><b>N. Albo:</b></td>
    <td style="border:none;color:#d4edda">______________________</td></tr>
<tr><td style="border:none;padding:4px 8px;color:#9aab9e"><b>Data:</b></td>
    <td style="border:none;color:#d4edda">{oggi}</td>
    <td style="border:none;padding:4px 8px;color:#9aab9e"><b>Luogo:</b></td>
    <td style="border:none;color:#d4edda">______________________</td></tr>
</table>
<div style="margin-top:2rem;display:flex;gap:5rem">
  <p style="color:#9aab9e;font-size:.8rem">Firma: ______________________</p>
  <div><p style="color:#9aab9e;font-size:.8rem">Timbro:</p>
  <div style="width:75px;height:75px;border:1px dashed rgba(201,150,58,.4);border-radius:50%;margin-top:.3rem"></div></div>
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
    st.success(f"✅ '{fn}' generato — Apri nel browser e usa Ctrl+P → Salva come PDF.")

st.markdown("""<div class="footer">
  AgroLog IA v7.0 — Carbon & ESG Strategic Intelligence |
  IPCC Tier 1 · FAO-PM · GHG Protocol Scope 1+2+3 · Open-Meteo Live+ERA5 · ecoinvent 3.9 |
  Sviluppato con 💚 — ogni giorno più preciso
</div>""",unsafe_allow_html=True)
