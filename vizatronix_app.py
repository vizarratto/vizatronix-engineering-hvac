import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import io
import os
import base64

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Pino Mazzitelli Engineering PRO", page_icon="🏗️", layout="wide")

# --- CUSTOM CSS PER MOBILE ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 1.6rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    iframe { border-radius: 10px; border: 1px solid #ddd; background: white; }
    </style>
    """, unsafe_allow_html=True)

# --- CLASSE PDF PROFESSIONALE ---
class VizatronixPDF(FPDF):
    def __init__(self, theme_color=(31, 78, 121)):
        super().__init__()
        self.theme_color = theme_color

    def header(self):
        self.set_fill_color(*self.theme_color)
        self.rect(0, 0, 210, 35, 'F')
        
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        self.set_y(8)
        self.cell(0, 8, 'VIZATRONIX ENGINEERING SOLUTIONS', 0, 1, 'C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 5, 'Relazione Tecnica Certificata di Progetto', 0, 1, 'C')
        self.set_y(40) 

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generato il: {date_str} | Pagina {self.page_no()}', 0, 0, 'C')

    def section_header(self, title):
        self.ln(4)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*self.theme_color)
        self.cell(0, 8, title.upper(), "B", 1, 'L')
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def technical_row(self, label, value, unit=""):
        self.set_font('Helvetica', 'B', 9)
        self.cell(95, 7, f"{label}:", 0, 0)
        self.set_font('Helvetica', '', 9)
        self.cell(0, 7, f"{value} {unit}", 0, 1)

# --- FUNZIONE VISUALIZZAZIONE PDF ---
def display_pdf(pdf_bytes):
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- FUNZIONI GRAFICHE ---
def get_pie_chart_termico(carico_str, carico_pers):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.pie([carico_str, carico_pers], labels=['Struttura', 'Persone'], autopct='%1.1f%%', colors=['#1f4e79', '#ffc107'], startangle=90)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf

def get_bar_chart_uta(p_vol, p_pers, p_norma):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(['Volumetrico', 'Affollamento', 'Normativa Edificio'], [p_vol, p_pers, p_norma], color=['#28a745', '#17a2b8', '#fd7e14'])
    ax.set_ylabel('Portata (m3/h)')
    plt.xticks(rotation=15)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf

# --- SIDEBAR ---
st.sidebar.title("👤 Committente")
nome_c = st.sidebar.text_input("Nome", "Mario")
cognome_c = st.sidebar.text_input("Cognome", "Rossi")
indirizzo_c = st.sidebar.text_input("Indirizzo", "Milano")
menu = st.sidebar.radio("Modulo:", ["🏠 Home", "❄️ Modulo Termico", "🌬️ Modulo UTA Avanzato"])

# --- MODULO HOME ---
if menu == "🏠 Home":
    st.title("🏗️ Vizatronix Engineering PRO")
    st.subheader("Ingegnere Pino Mazzitelli")
    st.info("Benvenuto nel pannello software professionale. Seleziona un modulo tecnico a sinistra per procedere al dimensionamento e alla generazione del report certificato.")

# --- MODULO TERMICO ---
elif menu == "❄️ Modulo Termico":
    st.title("❄️ Calcolo Carico Termico")
    c1, c2 = st.columns(2)
    with c1:
        area = st.number_input("Area (m2)", 1.0, 500.0, 40.0)
        altezza = st.number_input("Altezza (m)", 2.0, 5.0, 2.7)
    with c2:
        persone = st.number_input("Persone", 1, 50, 2)
        esposizione = st.selectbox("Esposizione", ["Nord", "Sud", "Est/Ovest"])

    volume = area * altezza
    totale_w = (volume * 35) + (persone * 150)
    assorbimento_w = totale_w / 3.2
    ampere = assorbimento_w / 230

    st.metric("Potenza Richiesta", f"{totale_w:,.0f} Watt")

    pdf = VizatronixPDF(theme_color=(31, 78, 121))
    pdf.add_page()
    
    pdf.section_header("Dati di Progetto Termico")
    pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
    pdf.technical_row("Indirizzo", indirizzo_c)
    pdf.technical_row("Volume Ambiente", f"{volume:.2f}", "m3")
    
    pdf.section_header("Risultati e Consumi")
    pdf.technical_row("Potenza Totale", f"{totale_w:,.0f}", "W")
    pdf.technical_row("Assorbimento Nominale", f"{assorbimento_w:.0f}", "W")
    pdf.technical_row("Corrente Stimata", f"{ampere:.2f}", "A")
    
    chart = get_pie_chart_termico(volume*35, persone*150)
    with open("t_chart.png", "wb") as f: f.write(chart.getbuffer())
    current_y = pdf.get_y() + 5
    pdf.image("t_chart.png", x=50, y=current_y, w=110)
    
    pdf_bytes = bytes(pdf.output())
    try: os.remove("t_chart.png")
    except: pass

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: st.download_button("⬇️ Scarica PDF", pdf_bytes, f"Termico_{cognome_c}.pdf", "application/pdf")
    with col_btn2: 
        if st.button("👁️ Visualizza PDF"): display_pdf(pdf_bytes)

# --- MODULO UTA AVANZATO ---
elif menu == "🌬️ Modulo UTA Avanzato":
    st.title("🌬️ Trattamento Aria Avanzato (UTA)")
    
    tab1, tab2 = st.tabs(["📐 Parametri Dimensionali e Normativi", "🌡️ Parametri Termici ed Efficientamento"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            vol_uta = st.number_input("Volume Ambiente (m3)", 10.0, 10000.0, 600.0)
            n_pers = st.number_input("Numero Occupanti", 1, 1000, 30)
            destinazione = st.selectbox("Destinazione d'uso (Normativa)", ["Uffici standard", "Ristoranti / Bar", "Palestre / Sport", "Aule scolastiche / Sale conferenza"])
        with col_b:
            qualita_aria = st.select_slider("Grado Qualità Aria Interna (EN 16798)", options=["IDA 3 (Moderata)", "IDA 2 (Media)", "IDA 1 (Alta)"])
            prevalenza = st.number_input("Prevalenza Statica Ventilatore (Pa)", 50, 1500, 300)
            ach = st.slider("Ricambi d'Aria Orari Generici (ACH)", 1, 15, 3)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Condizioni Climatiche di Progetto")
            t_est = st.number_input("Temperatura Esterna di Progetto (°C)", -10.0, 45.0, 35.0)
            t_int = st.number_input("Temperatura Interna Desiderata (°C)", 15.0, 30.0, 26.0)
        with col_d:
            st.subheader("Recupero Energetico")
            usa_recuperatore = st.checkbox("Includi Recuperatore di Calore a Flussi Incrociati", value=True)
            efficienza_rec = st.slider("Efficienza del Recuperatore (%)", 50, 95, 75) if usa_recuperatore else 0

    # --- LOGICA DEI CALCOLI TECNICI ---
    # 1. Calcolo Portate (m3/h)
    p_vol = vol_uta * ach
    
    # Moltiplicatore IAQ (IDA)
    coeff_ida = 30 if "IDA 3" in qualita_aria else (45 if "IDA 2" in qualita_aria else 72)
    p_pers = n_pers * coeff_ida
    
    # Filtro Destinazione d'uso normativa
    if "Uffici" in destinazione: p_norma = n_pers * 40
    elif "Ristoranti" in destinazione: p_norma = n_pers * 50
    elif "Palestre" in destinazione: p_norma = n_pers * 60
    else: p_norma = n_pers * 35 # Scuole/Sale

    p_progetto = max(p_vol, p_pers, p_norma)
    
    # 2. Calcolo Potenza Ventilatore Meccanica (kW)
    potenza_motore = ((p_progetto / 3600) * prevalenza) / (0.65 * 1000)

    # 3. Calcolo Potenza Termica Batteria (kW)
    delta_t = abs(t_est - t_int)
    # Formula: Q * densità * calore specifico * deltaT / 3600 per portarlo in kW
    potenza_termica_nominale = (p_progetto * 1.2 * 1.005 * delta_t) / 3600
    
    if usa_recuperatore:
        potenza_risparmiata = potenza_termica_nominale * (efficienza_rec / 100)
        potenza_batteria_reale = potenza_termica_nominale - potenza_risparmiata
    else:
        potenza_risparmiata = 0
        potenza_batteria_reale = potenza_termica_nominale

    # --- OUTPUT INTERFACCIA ---
    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("Portata Aria di Progetto", f"{p_progetto:,.0f} m3/h")
    res2.metric("Potenza Elettrica Ventilatore", f"{potenza_motore:.2f} kW")
    res3.metric("Carico Termico Batteria UTA", f"{potenza_batteria_reale:.2f} kW", 
              delta=f"-{potenza_risparmiata:.2f} kW (Eco)" if usa_recuperatore else None)

    # --- GENERAZIONE GENERALE PDF ---
    pdf = VizatronixPDF(theme_color=(40, 167, 69)) # Tema Verde
    pdf.add_page()
    
    pdf.section_header("Relazione Tecnica Trattamento Aria (UTA)")
    pdf.technical_row("Progettista", "Ingegnere Pino Mazzitelli")
    pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
    pdf.technical_row("Ubicazione Impianto", indirizzo_c)
    pdf.technical_row("Destinazione d'Uso Locale", destinazione)
    pdf.technical_row("Volume Totale Ambiente", f"{vol_uta}", "m3")
    
    pdf.section_header("Analisi e Dimensionamento Portate d'Aria")
    pdf.technical_row("Portata da Ricambi Volumetrici (ACH)", f"{p_vol:,.0f}", "m3/h")
    pdf.technical_row(f"Portata da Affollamento ({qualita_aria})", f"{p_pers:,.0f}", "m3/h")
    pdf.technical_row("Portata Minima da Categoria Edificio", f"{p_norma:,.0f}", "m3/h")
    pdf.technical_row("Portata Finale di Progetto (Max)", f"{p_progetto:,.0f}", "m3/h")
    
    pdf.section_header("Specifiche Meccaniche ed Aeraustiche")
    pdf.technical_row("Prevalenza Statica Richiesta", f"{prevalenza}", "Pa")
    pdf.technical_row("Potenza Elettrica Nominale Motore", f"{potenza_motore:.2f}", "kW")
    
    pdf.section_header("Bilancio Termico Aria di Rinnovo ed Efficientamento")
    pdf.technical_row("Temperatura Aria Esterna (Progetto)", f"{t_est}", "°C")
    pdf.technical_row("Temperatura Aria Interna (Comfort)", f"{t_int}", "°C")
    pdf.technical_row("Potenza Termica Nominale (Senza Recupero)", f"{potenza_termica_nominale:.2f}", "kW")
    pdf.technical_row("Recuperatore di Calore a Flussi Incrociati", "PRESENTE" if usa_recuperatore else "ASSENTE")
    if usa_recuperatore:
        pdf.technical_row("Efficienza Certificata Recuperatore", f"{efficienza_rec}", "%")
        pdf.technical_row("Potenza Termica Recuperata (Risparmio)", f"{potenza_risparmiata:.2f}", "kW")
    pdf.technical_row("Potenza Netta Richiesta alla Batteria", f"{potenza_batteria_reale:.2f}", "kW")
    
    # Generazione grafico a barre comparativo portate
    chart = get_bar_chart_uta(p_vol, p_pers, p_norma)
    with open("u_chart.png", "wb") as f: f.write(chart.getbuffer())
    current_y = pdf.get_y() + 5
    
    # Protezione cambio pagina automatica se l'immagine è troppo in basso
    if current_y > 200:
        pdf.add_page()
        current_y = 45
    pdf.image("u_chart.png", x=50, y=current_y, w=110)
    
    pdf_bytes = bytes(pdf.output())
    try: os.remove("u_chart.png")
    except: pass

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: 
        st.download_button("⬇️ Scarica Relazione UTA PDF", pdf_bytes, f"UTA_{cognome_c}.pdf", "application/pdf")
    with col_btn2: 
        if st.button("👁️ Visualizza Relazione PDF"): display_pdf(pdf_bytes)
