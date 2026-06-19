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
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
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
def get_pie_chart_termico(struttura, vetrate, persone, carichi_int):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    labels = ['Pareti/Solaio', 'Superfici Vetrate', 'Persone', 'Apparecchiature']
    valori = [struttura, vetrate, persone, carichi_int]
    # Filtra valori a zero per evitare grafici corrotti
    labels = [l for l, v in zip(labels, valori) if v > 0]
    valori = [v for v in valori if v > 0]
    
    ax.pie(valori, labels=labels, autopct='%1.1f%%', colors=['#1f4e79', '#fd7e14', '#ffc107', '#17a2b8'], startangle=90)
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
menu = st.sidebar.radio("Modulo:", ["🏠 Home", "❄️ Modulo Termico PRO", "🌬️ Modulo UTA Avanzato"])

# --- MODULO HOME ---
if menu == "🏠 Home":
    st.title("🏗️ Vizatronix Engineering PRO")
    st.subheader("Ingegnere Pino Mazzitelli")
    st.info("Seleziona un modulo tecnico dal menu a sinistra per avviare il dimensionamento termotecnico ed aeraustico.")

# --- MODULO TERMICO PRO ---
elif menu == "❄️ Modulo Termico PRO":
    st.title("❄️ Calcolo Carichi Termici Estivi ed Invernali")
    
    t_term_1, t_term_2 = st.tabs(["🏛️ Geometria e Struttura", "🔥 Carichi Interni e Climatici"])
    
    with t_term_1:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            area = st.number_input("Superficie Calpestabile (m2)", 1.0, 1000.0, 50.0)
            altezza = st.number_input("Altezza Interpiano (m)", 2.0, 6.0, 2.70)
            isolamento = st.selectbox("Livello Isolamento Strutture", ["Ottimo (Nuova costruzione / Cappotto)", "Medio (Anni 90/2000)", "Scarso (Edificio storico / Non isolato)"])
        with col_t2:
            sup_vetrata = st.number_input("Superficie Vetrata Totale (m2)", 0.0, 200.0, 6.0)
            esposizione = st.selectbox("Esposizione Prevalente Fronte Vetrato", ["Nord (Nessun raggiamento diretto)", "Sud (Forte irraggiamento)", "Est / Ovest (Raggiamento mattutino/pomeridiano)"])
            tipo_vetro = st.selectbox("Tipologia di Vetratura", ["Doppio Vetro Basso Emissivo", "Vetro Singolo", "Triplo Vetro Selettivo"])

    with t_term_2:
        col_t3, col_t4 = st.columns(2)
        with col_t3:
            destinazione_t = st.selectbox("Destinazione d'Uso del Locale", ["Residenziale / Uffici standard", "Locali Commerciali / Negozi", "Palestre / Attività Sportiva"])
            persone = st.number_input("Numero Medio di Occupanti", 0, 500, 4)
        with col_t4:
            carico_elettro = st.number_input("Potenza Apparecchiature Elettriche Accese (W)", 0, 50000, 600, step=100)
            modo_calcolo = st.radio("Seleziona Stagione di Progetto", ["Raffrescamento (Estivo)", "Riscaldamento (Invernale)"])

    # --- LOGICA DI CALCOLO STRUTTURALE ---
    volume = area * altezza
    
    # Assegnazione coefficienti di trasmittanza/dispersione (W/m2K o W/m3) equivalenti empirici professionali
    coeff_isol = 18 if "Ottimo" in isolamento else (28 if "Medio" in isolamento else 42)
    carico_struttura = volume * coeff_isol

    # Calcolo carico vetrate (Funzione dell'esposizione e del tipo di vetro)
    coeff_vetro = 1.4 if "Triplo" in tipo_vetro else (2.8 if "Doppio" in tipo_vetro else 5.7)
    coeff_esposizione = 1.0 if "Nord" in esposizione else (1.5 if "Sud" in esposizione else 1.8) # Ovest ha il picco estivo massimo
    
    if modo_calcolo == "Raffrescamento (Estivo)":
        carico_vetrate = sup_vetrata * coeff_vetro * 30 * coeff_esposizione # DeltaT estivo + irraggiamento
        # Apporto metabolico persone (Sensibile + Latente)
        coeff_pers_watt = 120 if "Residenziale" in destinazione_t else (150 if "Commerciali" in destinazione_t else 250)
        carico_persone = persone * coeff_pers_watt
        carico_impianti = carico_elettro
    else:
        # Inverno: Minori carichi interni considerati a favore di sicurezza per il picco termico
        carico_vetrate = sup_vetrata * coeff_vetro * 25 # Solo conduzione pura deltaT inverno
        carico_persone = 0 
        carico_impianti = 0

    # Totale Potenze
    potenza_w = carico_struttura + carico_vetrate + carico_persone + carico_impianti
    potenza_kw = potenza_w / 1000
    potenza_btu = potenza_kw * 3412.142

    # --- VISUALIZZAZIONE RISULTATI ---
    st.markdown("---")
    res_t1, res_t2 = st.columns(2)
    res_t1.metric(f"Potenza Richiesta ({modo_calcolo})", f"{potenza_kw:.2f} kW")
    res_t2.metric("Potenza Equivalente in BTU/h", f"{potenza_btu:,.0f} BTU/h")

    # --- GENERAZIONE PDF TERMICO ---
    pdf = VizatronixPDF(theme_color=(31, 78, 121))
    pdf.add_page()
    
    pdf.section_header("Dati di Sintesi Fabbricato")
    pdf.technical_row("Progettista", "Ingegnere Pino Mazzitelli")
    pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
    pdf.technical_row("Indirizzo Immobile", indirizzo_c)
    pdf.technical_row("Destinazione Locale", destinazione_t)
    pdf.technical_row("Volume Totale Ambiente", f"{volume:.2f}", "m3")
    pdf.technical_row("Grado Isolamento Termico", isolamento)
    
    pdf.section_header("Dettagli Superfici Vetrate ed Esposizione")
    pdf.technical_row("Superficie Vetratura Esposta", f"{sup_vetrata}", "m2")
    pdf.technical_row("Orientamento Parete Vetrata", esposizione)
    pdf.technical_row("Tecnologia Vetro Installata", tipo_vetro)

    pdf.section_header("Bilancio Energetico dei Carichi")
    pdf.technical_row("Carico da Struttura Disperdente", f"{carico_struttura/1000:.3f}", "kW")
    pdf.technical_row("Carico da Irraggiamento / Trasmittanza Vetri", f"{carico_vetrate/1000:.3f}", "kW")
    pdf.technical_row("Carico Endogeno (Occupanti)", f"{carico_persone/1000:.3f}", "kW")
    pdf.technical_row("Carico da Apparecchiature Elettriche", f"{carico_impianti/1000:.3f}", "kW")
    
    pdf.section_header("Dimensionamento Finale Impianto")
    pdf.technical_row("POTENZA TOTALE RICHIESTA (kW)", f"{potenza_kw:.2f}", "kW")
    pdf.technical_row("POTENZA TOTALE RICHIESTA (BTU/h)", f"{potenza_btu:,.0f}", "BTU/h")
    
    # Grafico a torta dei carichi termici
    chart = get_pie_chart_termico(carico_struttura, carico_vetrate, carico_persone, carico_impianti)
    with open("t_chart.png", "wb") as f: f.write(chart.getbuffer())
    current_y = pdf.get_y() + 8
    if current_y > 210:
        pdf.add_page()
        current_y = 45
    pdf.image("t_chart.png", x=50, y=current_y, w=110)
    
    pdf_bytes = bytes(pdf.output())
    try: os.remove("t_chart.png")
    except: pass

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: st.download_button("⬇️ Scarica Relazione Termica PDF", pdf_bytes, f"Termico_{cognome_c}.pdf", "application/pdf")
    with col_btn2: 
        if st.button("👁️ Visualizza Report"): display_pdf(pdf_bytes)

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

    p_vol = vol_uta * ach
    coeff_ida = 30 if "IDA 3" in qualita_aria else (45 if "IDA 2" in qualita_aria else 72)
    p_pers = n_pers * coeff_ida
    
    if "Uffici" in destinazione: p_norma = n_pers * 40
    elif "Ristoranti" in destinazione: p_norma = n_pers * 50
    elif "Palestre" in destinazione: p_norma = n_pers * 60
    else: p_norma = n_pers * 35

    p_progetto = max(p_vol, p_pers, p_norma)
    potenza_motore = ((p_progetto / 3600) * prevalenza) / (0.65 * 1000)
    delta_t = abs(t_est - t_int)
    potenza_termica_nominale = (p_progetto * 1.2 * 1.005 * delta_t) / 3600
    
    if usa_recuperatore:
        potenza_risparmiata = potenza_termica_nominale * (efficienza_rec / 100)
        potenza_batteria_reale = potenza_termica_nominale - potenza_risparmiata
    else:
        potenza_risparmiata = 0
        potenza_batteria_reale = potenza_termica_nominale

    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("Portata Aria di Progetto", f"{p_progetto:,.0f} m3/h")
    res2.metric("Potenza Elettrica Ventilatore", f"{potenza_motore:.2f} kW")
    res3.metric("Carico Termico Batteria UTA", f"{potenza_batteria_reale:.2f} kW", 
              delta=f"-{potenza_risparmiata:.2f} kW (Eco)" if usa_recuperatore else None)

    pdf = VizatronixPDF(theme_color=(40, 167, 69))
    pdf.add_page()
    
    pdf.section_header("Relazione Tecnica Trattamento Aria (UTA)")
    pdf.technical_row("Progettista", "Pino Mazzitelli")
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
    
    chart = get_bar_chart_uta(p_vol, p_pers, p_norma)
    with open("u_chart.png", "wb") as f: f.write(chart.getbuffer())
    current_y = pdf.get_y() + 5
    if current_y > 200:
        pdf.add_page()
        current_y = 45
    pdf.image("u_chart.png", x=50, y=current_y, w=110)
    
    pdf_bytes = bytes(pdf.output())
    try: os.remove("u_chart.png")
    except: pass

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: st.download_button("⬇️ Scarica Relazione UTA PDF", pdf_bytes, f"UTA_{cognome_c}.pdf", "application/pdf")
    with col_btn2: 
        if st.button("👁️ Visualizza Relazione PDF"): display_pdf(pdf_bytes)
