import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import io
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Vizatronix Engineering PRO", page_icon="🏗️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #ffffff; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1f4e79; }
    </style>
    """, unsafe_allow_html=True)

# --- CLASSE PDF PROFESSIONALE ---
class VizatronixPDF(FPDF):
    def __init__(self, theme_color=(31, 78, 121)):
        super().__init__()
        self.theme_color = theme_color

    def header(self):
        # Header con rettangolo colorato in base al modulo
        self.set_fill_color(*self.theme_color)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'VIZATRONIX ENGINEERING SOLUTIONS', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Relazione Tecnica di Progetto Certificata', 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generato il: {date_str} | Vizatronix Software v2.5 | Pagina {self.page_no()}', 0, 0, 'C')

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

# --- FUNZIONI GRAFICHE ---
def get_pie_chart_termico(carico_str, carico_pers):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie([carico_str, carico_pers], labels=['Struttura', 'Persone'], autopct='%1.1f%%', colors=['#1f4e79', '#ffc107'], startangle=90)
    plt.title("Ripartizione Carico Termico (W)")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def get_bar_chart_uta(portata_vol, portata_pers):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(5, 4))
    categories = ['Volume (ACH)', 'Affollamento (UNI)']
    values = [portata_vol, portata_pers]
    colors = ['#28a745' if v == max(values) else '#6c757d' for v in values]
    ax.bar(categories, values, color=colors)
    ax.set_ylabel('Portata d\'aria (m3/h)')
    plt.title("Confronto Criteri di Portata Fresh Air")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/900/900667.png", width=80)
st.sidebar.title("Vizatronix Panel")
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Dati Committente")
nome_c = st.sidebar.text_input("Nome", "Mario")
cognome_c = st.sidebar.text_input("Cognome", "Rossi")
indirizzo_c = st.sidebar.text_input("Indirizzo", "Via Roma 1, Milano")
email_c = st.sidebar.text_input("Email", "m.rossi@example.com")

# --- MENU PRINCIPALE ---
menu = st.sidebar.radio("Seleziona Calcolo:", ["🏠 Home", "❄️ Potenza Termica", "🌬️ Trattamento Aria (UTA)"])

if menu == "🏠 Home":
    st.title("🚀 Benvenuto in Vizatronix Engineering PRO")
    st.markdown("""
    ### Suite professionale per il dimensionamento rapido HVAC.
    Scegli un modulo dal menu a sinistra per iniziare la progettazione:
    - **Modulo Termico:** Calcolo dei carichi termici estivi/invernali, consumi elettrici e assorbimenti.
    - **Modulo UTA:** Dimensionamento portate d'aria normativa UNI 10339 e calcolo potenza motori ventilanti.
    """)
    st.info("I dati del committente inseriti nella barra laterale verranno riportati automaticamente nei report PDF.")

elif menu == "❄️ Potenza Termica":
    st.title("❄️ Calcolo Carico Termico & Consumi")
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Superficie Locale (m2)", 1.0, 1000.0, 45.0)
        altezza = st.number_input("Altezza Soffitto (m)", 2.0, 15.0, 3.0)
        persone = st.number_input("Numero Occupanti", 1, 500, 4)
    with col2:
        esposizione = st.selectbox("Esposizione Prevalente", ["Nord", "Sud", "Est/Ovest"])
        isolamento = st.select_slider("Qualità Isolamento", ["Scarso", "Medio", "Ottimo"], "Medio")
        unita = st.radio("Mostra Risultati in:", ["Watt", "BTU/h", "Frigorie/h"], horizontal=True)

    # Logica Calcolo
    volume = area * altezza
    k_esp = {"Nord": 25, "Est/Ovest": 35, "Sud": 45}[esposizione]
    k_iso = {"Scarso": 1.2, "Medio": 1.0, "Ottimo": 0.8}[isolamento]
    
    carico_str = volume * k_esp * k_iso
    carico_pers = persone * 150 # 150W per persona calore latente+sensibile
    totale_w = carico_str + carico_pers
    
    eer = 3.2 # Efficienza media stimata
    assorbimento_w = totale_w / eer
    ampere = assorbimento_w / 230

    # UI Metrics
    c1, c2, c3 = st.columns(3)
    if unita == "BTU/h": display_val = totale_w * 3.41
    elif unita == "Frigorie/h": display_val = totale_w * 0.86
    else: display_val = totale_w

    c1.metric("Potenza Richiesta", f"{display_val:,.0f} {unita}")
    c2.metric("Consumo Elettrico (W)", f"{assorbimento_w:.0f} W")
    c3.metric("Assorbimento Corrente", f"{ampere:.2f} A")

    st.markdown("### Analisi Carichi Energetici")
    chart_term = get_pie_chart_termico(carico_str, carico_pers)
    st.image(chart_term, width=500)

    if st.button("💾 Genera Relazione Termica Completa"):
        pdf = VizatronixPDF(theme_color=(31, 78, 121)) # Blu
        pdf.add_page()
        
        pdf.section_header("Dati Committente")
        pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
        pdf.technical_row("Indirizzo Intervento", indirizzo_c)
        pdf.ln(5)

        pdf.section_header("Dati di Input Ambiente")
        pdf.technical_row("Volume Totale", f"{volume:.2f}", "m3")
        pdf.technical_row("Esposizione Pareti", esposizione)
        pdf.technical_row("Coefficiente Isolamento", isolamento)
        pdf.ln(5)

        pdf.section_header("Risultati del Calcolo Termico")
        pdf.technical_row("Potenza Termica (W)", f"{totale_w:,.0f}", "W")
        pdf.technical_row("Potenza Termica (BTU/h)", f"{totale_w * 3.41:,.0f}", "BTU/h")
        pdf.technical_row("Consumo Elettrico Stimato", f"{assorbimento_w:,.0f}", "Watt")
        pdf.technical_row("Corrente Assorbita", f"{ampere:.2f}", "Ampere")
        pdf.ln(10)

        # Inserimento Grafico nel PDF
        with open("temp_term.png", "wb") as f: f.write(chart_term.getbuffer())
        pdf.image("temp_term.png", x=50, y=180, w=110)
        os.remove("temp_term.png")

        st.download_button("⬇️ Scarica PDF Modulo Termico", bytes(pdf.output(dest='S')), f"Vizatronix_Termico_{cognome_c}.pdf", "application/pdf")

elif menu == "🌬️ Trattamento Aria (UTA)":
    st.title("🌬️ Dimensionamento Unità Trattamento Aria (UTA)")
    
    col1, col2 = st.columns(2)
    with col1:
        vol_uta = st.number_input("Volume Locale (m3)", 10.0, 10000.0, 500.0)
        n_ricambi = st.slider("Ricambi aria orari (ACH)", 1, 15, 4)
        n_pers_uta = st.number_input("Numero Persone Presenti", 1, 1000, 20)
    with col2:
        portata_norma = st.number_input("Portata UNI per persona (m3/h)", 10, 60, 32)
        k_cont = st.slider("Coefficiente Contemporaneità", 0.5, 1.0, 0.8)
        prevalenza = st.number_input("Prevalenza Statica Totale (Pa)", 50, 2000, 300)

    # Calcoli UTA
    p_vol = vol_uta * n_ricambi
    p_pers = n_pers_uta * portata_norma * k_cont
    p_progetto = max(p_vol, p_pers)
    
    # Calcolo Motore: Potenza [kW] = (Portata[m3/s] * Prevalenza[Pa]) / (Efficienza * 1000)
    efficienza = 0.65
    potenza_motore = ((p_progetto / 3600) * prevalenza) / (efficienza * 1000)

    c1, c2, c3 = st.columns(3)
    c1.metric("Portata di Progetto", f"{p_progetto:,.0f} m3/h")
    c2.metric("Potenza Motore", f"{potenza_motore:.2f} kW")
    c3.metric("Pressione di Esercizio", f"{prevalenza} Pa")

    st.markdown("### Verifica Criteri Normativi")
    chart_uta = get_bar_chart_uta(p_vol, p_pers)
    st.image(chart_uta, width=500)

    if st.button("💾 Genera Relazione Tecnica UTA PDF"):
        pdf = VizatronixPDF(theme_color=(40, 167, 69)) # Verde
        pdf.add_page()
        
        pdf.section_header("Dati Committente")
        pdf.technical_row("Cliente", f"{nome_c} {cognome_c}")
        pdf.technical_row("Ubicazione", indirizzo_c)
        pdf.ln(5)

        pdf.section_header("Criteri di Calcolo Portata")
        pdf.technical_row("Calcolo Volumetrico (ACH)", f"{p_vol:,.0f}", "m3/h")
        pdf.technical_row("Calcolo su Affollamento", f"{p_pers:,.0f}", "m3/h")
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, f"SCELTA PROGETTUALE: {p_progetto:,.0f} m3/h", 1, 1, 'C')
        pdf.ln(5)

        pdf.section_header("Specifiche Meccaniche Ventilatore")
        pdf.technical_row("Prevalenza Totale Impianto", f"{prevalenza}", "Pa")
        pdf.technical_row("Rendimento Sistema Stimato", "65", "%")
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(40, 167, 69)
        pdf.cell(0, 10, f"POTENZA NOMINALE MOTORE: {potenza_motore:.2f} kW", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)

        # Inserimento Grafico nel PDF
        with open("temp_uta.png", "wb") as f: f.write(chart_uta.getbuffer())
        pdf.image("temp_uta.png", x=50, y=180, w=110)
        os.remove("temp_uta.png")

        st.download_button("⬇️ Scarica PDF Trattamento Aria", bytes(pdf.output(dest='S')), f"Vizatronix_UTA_{cognome_c}.pdf", "application/pdf")