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
st.set_page_config(page_title="Vizatronix PRO", page_icon="🏗️", layout="wide")

# --- CUSTOM CSS PER MOBILE ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    iframe { border-radius: 10px; border: 1px solid #ddd; }
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
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'VIZATRONIX ENGINEERING SOLUTIONS', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Relazione Tecnica Certificata', 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generato il: {date_str} | Pagina {self.page_no()}', 0, 0, 'C')

    def section_header(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*self.theme_color)
        self.cell(0, 10, title.upper(), "B", 1, 'L')
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def technical_row(self, label, value, unit=""):
        self.set_font('Arial', 'B', 10)
        self.cell(85, 8, f"{label}:", 0, 0)
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"{value} {unit}", 0, 1)

# --- FUNZIONE VISUALIZZAZIONE PDF ---
def display_pdf(pdf_bytes):
    """Genera un iframe per visualizzare il PDF direttamente nell'app"""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- FUNZIONI GRAFICHE ---
def get_pie_chart_termico(carico_str, carico_pers):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie([carico_str, carico_pers], labels=['Struttura', 'Persone'], autopct='%1.1f%%', colors=['#1f4e79', '#ffc107'], startangle=90)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def get_bar_chart_uta(p_vol, p_pers):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(['Volumetrico', 'Persone'], [p_vol, p_pers], color=['#28a745', '#17a2b8'])
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

# --- SIDEBAR ---
st.sidebar.title("👤 Committente")
nome_c = st.sidebar.text_input("Nome", "Mario")
cognome_c = st.sidebar.text_input("Cognome", "Rossi")
indirizzo_c = st.sidebar.text_input("Indirizzo", "Milano")

menu = st.sidebar.radio("Modulo:", ["🏠 Home", "❄️ Modulo Termico", "🌬️ Modulo UTA"])

# --- MODULO HOME ---
if menu == "🏠 Home":
    st.title("🏗️ Vizatronix Engineering PRO")
    st.info("Benvenuto. Usa il menu a sinistra per i calcoli tecnici. Ora puoi visualizzare i report direttamente su smartphone prima di inviarli.")

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

    st.metric("Potenza Richiesta", f"{totale_w:,.0f} Watt")

    col_btn1, col_btn2 = st.columns(2)
    
    # Logica PDF
    pdf = VizatronixPDF(theme_color=(31, 78, 121))
    pdf.add_page()
    pdf.section_header("Dati Termici")
    pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
    pdf.technical_row("Potenza Totale", f"{totale_w:,.0f}", "W")
    pdf.technical_row("Assorbimento", f"{assorbimento_w:.0f}", "W")
    
    chart = get_pie_chart_termico(volume*35, persone*150)
    with open("t.png", "wb") as f: f.write(chart.getbuffer())
    pdf.image("t.png", x=50, y=100, w=110)
    pdf_bytes = bytes(pdf.output(dest='S'))
    os.remove("t.png")

    with col_btn1:
        st.download_button("⬇️ Scarica PDF", pdf_bytes, f"Termico_{cognome_c}.pdf", "application/pdf")
    with col_btn2:
        if st.button("👁️ Visualizza PDF"):
            display_pdf(pdf_bytes)

# --- MODULO UTA ---
elif menu == "🌬️ Modulo UTA":
    st.title("🌬️ Trattamento Aria")
    c1, c2 = st.columns(2)
    with c1:
        vol_uta = st.number_input("Volume (m3)", 10.0, 5000.0, 500.0)
        n_pers = st.number_input("Persone", 1, 500, 20)
    with c2:
        prevalenza = st.number_input("Prevalenza (Pa)", 50, 1000, 250)
        ach = st.slider("Ricambi (ACH)", 1, 15, 4)

    p_vol = vol_uta * ach
    p_pers = n_pers * 32 * 0.8
    p_progetto = max(p_vol, p_pers)
    potenza_motore = ((p_progetto / 3600) * prevalenza) / (0.65 * 1000)

    st.metric("Portata Progetto", f"{p_progetto:,.0f} m3/h")

    col_btn1, col_btn2 = st.columns(2)

    # Logica PDF UTA
    pdf = VizatronixPDF(theme_color=(40, 167, 69))
    pdf.add_page()
    pdf.section_header("Relazione Tecnica UTA")
    pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
    pdf.technical_row("Portata Aria", f"{p_progetto:,.0f}", "m3/h")
    pdf.technical_row("Potenza Motore", f"{potenza_motore:.2f}", "kW")
    
    chart = get_bar_chart_uta(p_vol, p_pers)
    with open("u.png", "wb") as f: f.write(chart.getbuffer())
    pdf.image("u.png", x=50, y=100, w=110)
    pdf_bytes = bytes(pdf.output(dest='S'))
    os.remove("u.png")

    with col_btn1:
        st.download_button("⬇️ Scarica PDF", pdf_bytes, f"UTA_{cognome_c}.pdf", "application/pdf")
    with col_btn2:
        if st.button("👁️ Visualizza PDF"):
            display_pdf(pdf_bytes)
