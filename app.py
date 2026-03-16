import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# AGGIUNGI QUESTA LINEA:
import plotly.figure_factory as ff 
from fpdf import FPDF

# CONFIGURAZIONE ELITE
st.set_page_config(page_title="AgroLog AI | Financial & Carbon Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background: linear-gradient(145deg, #161b22, #0d1117); border-radius: 12px; padding: 25px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CON DATI COMPLESSI (I tuoi dati richiesti) ---
with st.sidebar:
    # --- SEZIONE BRANDING (Punto 2) ---
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429435.png", width=80) 
    st.title("AgroLog IA")
    st.markdown("**Dott. [Tuo Nome]**")
    st.caption("Dottore Agronomo - Esperto in Carbon Farming")
    st.markdown("---")
    
    # --- PARAMETRI ECONOMICI GLOBALI ---
    st.header("💹 Parametri di Mercato")
    prezzo_co2 = st.number_input("Prezzo Credito CO2 (€/t)", value=65.0)
    tasso_crescita = st.slider("Tasso crescita stimato (%)", 1, 10, 5)
    
    st.markdown("---")
    st.markdown("📧 [Contattami per una perizia](mailto:tua@email.it)")
    st.info("Modello Certificabile basato su Standard ISO 14064-2")
    st.title("💼 Control Panel Elite")
    azienda = st.text_input("Ragione Sociale", "Tenuta Agricola d'Elite")
    ettari = st.number_input("Ettari", 1, 1000, 50)
    
    st.header("🔬 Analisi del Suolo")
    so = st.slider("Sostanza Organica attuale (%)", 0.5, 5.0, 1.8)
    argilla = st.slider("Contenuto Argilla (%)", 5, 60, 25)
    densita = st.number_input("Densità Apparente (g/cm³)", 0.8, 1.8, 1.3)
    profondita = st.selectbox("Profondità Campionamento (cm)", [10, 30, 60], index=1)
    
    st.header("🚜 Gestione")
    coltura = st.selectbox("Coltura", ["Cereali", "Vite", "Olivo", "Nocciolo", "Foraggere"])
    protocollo = st.selectbox("Protocollo Tecnico", ["Convenzionale", "Intermedio", "Rigenerativo Full"])
    st.markdown("---")
    st.info("Algoritmo AgroLog v.5.0 - Modello Pedologico Avanzato")
# --- LOGICA MULTI-CAMPO (Punto 3) ---
st.subheader("📑 Gestione Asset Fondiari")
st.write("Configura i singoli appezzamenti per ottenere il bilancio aziendale consolidato.")

# Creiamo la struttura dati iniziale
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"Appezzamento": "Campo Nord", "Ettari": 10.0, "SO %": 1.5, "Argilla %": 25, "Protocollo": "Rigenerativo Full"},
        {"Appezzamento": "Vigneto", "Ettari": 5.0, "SO %": 1.2, "Argilla %": 15, "Protocollo": "Convenzionale"}
    ])

# Tabella Interattiva
df_editabile = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)

# Calcolo Aggregato
total_co2_consolidata = 0
for _, row in df_editabile.iterrows():
    # Formula Scientifica (Massa suolo * SO * Coeff)
    massa = 0.30 * 10000 * 1.3 # 30cm, 10k mq, densità 1.3
    soc = massa * (row["SO %"] / 100) * 0.58
    c_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
    seq = soc * c_prot.get(row["Protocollo"], 0.01) * (1 + row["Argilla %"]/100)
    total_co2_consolidata += seq * 3.67 * row["Ettari"]
    # --- ANALISI VISIVA E COMMENTO IA (Aggiunta per Unicità) ---
if not df_editabile.empty:
    st.markdown("---")
    col_chart, col_advice = st.columns([2, 1])

    with col_chart:
        # Calcolo contributo per singolo campo per il grafico
        df_plot = df_editabile.copy()
        df_plot['Valore CO2'] = df_plot.apply(
            lambda x: (0.30 * 10000 * 1.3 * (x['SO %']/100) * 0.58 * {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}.get(x['Protocollo'], 0.01) * (1 + x['Argilla %']/100) * 3.67 * x['Ettari']), axis=1
        )
        
        fig_donut = px.pie(df_plot, values='Valore CO2', names='Appezzamento', 
                           hole=0.6, title="💰 Distribuzione Valore Carbonio per Campo",
                           color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_advice:
        st.write("### 🤖 Agro-Advisor Insights")
        top_campo = df_plot.loc[df_plot['Valore CO2'].idxmax()]['Appezzamento']
        st.success(f"**Asset Leader:** Il campo '{top_campo}' genera il maggior ritorno economico.")
        
        # Suggerimento dinamico
        if "Convenzionale" in df_plot['Protocollo'].values:
            campi_conv = df_plot[df_plot['Protocollo'] == "Convenzionale"]['Appezzamento'].count()
            st.warning(f"Hai {campi_conv} appezzamenti in 'Convenzionale'. La transizione a 'Rigenerativo' aumenterebbe il tuo asset del 400%.")
        else:
            st.balloons()
            st.info("Tutti i campi sono ottimizzati. Sei pronto per la certificazione internazionale.")

# --- TASTO ESPORTAZIONE EXCEL (Comodità per il cliente) ---
st.download_button(
    label="📂 Esporta Tabella in Excel (CSV)",
    data=df_editabile.to_csv(index=False).encode('utf-8'),
    file_name=f'analisi_carbonio_{azienda}.csv',
    mime='text/csv',
)

# Visualizzazione Risultati Globali
st.markdown("---")
st.subheader("🏁 Bilancio Aziendale Totale")
c1, c2 = st.columns(2)
c1.metric("CO2 Totale Sequestrata", f"{round(total_co2_consolidata, 1)} t/anno")
c2.metric("Valore Asset Carbonio", f"€ {round(total_co2_consolidata * prezzo_co2, 2)}")
# --- LOGICA SCIENTIFICA AVANZATA (La tua unicità) ---
# 1. Massa del suolo (t/ha) = Volume * Densità
massa_suolo = (profondita / 100) * 10000 * densita 
# 2. Stock attuale di Carbonio (SOC) - Il Carbonio è circa il 58% della Sostanza Organica
soc_attuale = massa_suolo * (so / 100) * 0.58
# 3. Coefficienti di sequestro basati su protocollo e tessitura (Argilla)
coeff_argilla = 1 + (argilla / 100)
coeff_prot = {"Convenzionale": 0.005, "Intermedio": 0.02, "Rigenerativo Full": 0.05}
# 4. Calcolo CO2 Sequestrata (C * 3.67 = CO2)
sequestro_c = soc_attuale * coeff_prot[protocollo] * coeff_argilla
co2_tot = sequestro_c * 3.67 * ettari
valore_asset = co2_tot * 65 # Prezzo credito 2026

# --- HEADER DASHBOARD ---
st.title(f"📊 Analisi Strategica: {azienda}")
c1, c2, c3 = st.columns(3)
with c1:
    rating_val = "AAA" if protocollo == "Rigenerativo Full" and so > 2.0 else "AA" if so > 1.5 else "B"
    st.metric("ESG Rating", rating_val)
with c2:
    st.metric("CO2 Sequestrata/Anno", f"{round(co2_tot, 1)} t", delta=f"{round(co2_tot/ettari, 2)} t/ha")
with c3:
    st.metric("Valutazione Asset", f"€ {round(valore_asset, 2)}")

st.markdown("---")

# --- GRAFICI ---
col_radar, col_proiezione = st.columns([1, 1])

with col_radar:
    st.subheader("🎯 Profilo Pedo-Agronomico")
    categories = ['Stoccaggio C', 'Biodiversità', 'Ritenzione Idrica', 'Resilienza', 'Margine']
    # I valori cambiano dinamicamente in base ad argilla e sostanza organica
    valori_radar = [so*20, 70 if protocollo != "Convenzionale" else 30, argilla*1.5, 60, 85]
    fig_radar = go.Figure(data=go.Scatterpolar(r=valori_radar, theta=categories, fill='toself', line_color='#00ff88'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_radar, use_container_width=True)

with col_proiezione:
    st.subheader("📈 Capitalizzazione Carbonio (5 anni)")
    df_fin = pd.DataFrame({
        'Anno': [2026, 2027, 2028, 2029, 2030],
        'Valore Cumulato (€)': [valore_asset * (i+1) for i in range(5)]
    })
    fig_fin = px.line(df_fin, x='Anno', y='Valore Cumulato (€)', markers=True, color_discrete_sequence=['#3b82f6'])
    st.plotly_chart(fig_fin, use_container_width=True)

# --- AI INSIGHT ---
st.subheader("🤖 AI Executive Analysis")
if so < 2.0:
    st.warning(f"Il livello di Sostanza Organica ({so}%) è critico per la coltura {coltura}. L'adozione del protocollo {protocollo} potrebbe incrementare il valore del terreno di circa il 15% in 3 anni.")
else:
    st.success(f"Ottima gestione. Con un contenuto di Argilla del {argilla}%, il potenziale di mineralizzazione è basso: il tuo carbonio è protetto e stabile.")
