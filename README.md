Vizatronix Engineering PRO — Suite di Calcolo Termotecnico & Aeraustico
Vizatronix Engineering PRO è un'applicazione web-based altamente specializzata sviluppata in Python tramite il framework Streamlit. Il software fornisce agli ingegneri professionisti, progettisti termotecnici e installatori uno strumento rapido, preciso e conforme alle normative vigenti per il dimensionamento dei carichi termici (estivi/invernali) e la progettazione aeraustica avanzata delle Unità di Trattamento Aria (UTA).

La suite integra un motore di reportistica in formato PDF (FPDF2) ottimizzato per la visualizzazione cross-platform, ideale per la consultazione immediata da smartphone sul cantiere o per l'invio diretto via client di messaggistica.

🚀 Funzionalità Principali
1. ❄️ Modulo Termico PRO (Bilancio Energetico)
Analisi Analitica dei Carichi: Superamento del calcolo volumetrico forfettario a favore di un algoritmo basato su componenti fisici reali.

Dispersione delle Strutture: Calcolo basato sul livello di isolamento termico del fabbricato (Trasmittanza termica equivalente U).

Carico Solare Estivo: Algoritmo sensibile all'esposizione cardinale delle superfici vetrate (con picco d'irraggiamento per orientamenti Sud ed Est/Ovest) e alla tecnologia del vetro.

Carichi Endogeni & Apparecchiature: Computo degli apporti termici metabolici (sensibile/latente correlato all'attività) e delle potenze elettriche dissipate.

Doppio Output Standardizzato: Risultati convertiti simultaneamente in kW e BTU/h per una compatibilità universale con i cataloghi commerciali dei produttori HVAC.

🌬️ Modulo UTA Avanzato (Trattamento Aria)
Dimensionamento Multicriterio: Selezione automatica della portata d'aria di progetto applicando il principio del valore massimo fra:

Ricambi d'aria volumetrici orari (ACH).

Affollamento antropico basato sulle classi di qualità dell'aria interna Indoor Air Quality (EN 16798) (IDA 1 / IDA 2 / IDA 3).

Portate minime specifiche per destinazione d'uso (Uffici, Ristorazione, Palestre, Scuole).

Specifiche Meccaniche: Calcolo della potenza elettrica del ventilatore in funzione della prevalenza statica (Pa) e del rendimento fluidodinamico (η).

Efficientamento Energetico: Simulazione di un recuperatore di calore a flussi incrociati con calcolo immediato della potenza termica recuperata e abbattimento dei costi operativi sulla batteria.

📊 Architettura e Modello Dati
Il software è ingegnerizzato per garantire la massima stabilità in ambienti Cloud ed effimeri (es. Streamlit Community Cloud):

Prevenzione dei Crash dei Font: Utilizzo nativo dei core fonts standard PDF (Helvetica) per scongiurare disallineamenti di libreria o assenze di dipendenze del sistema operativo (OS-agnostic).

Impaginazione Dinamica: Monitoraggio in tempo reale della coordinata verticale pdf.get_y() per impedire la sovrapposizione tra testi tabellari e i grafici renderizzati da Matplotlib, gestendo l'interruzione di pagina (add_page()) in sicurezza.

Memory Clean-up: Generazione e distruzione automatica dei file grafici temporanei (.png) tramite blocchi try-except per azzerare l'occupazione del file system lato server.

🛠️ Requisiti di Sistema e Installazione
Prerequisiti
Python 3.9 o superiore

PIP (Python Package Installer)

Installazione delle Dipendenze
Clona la repository e installa i pacchetti necessari elencati nel file requirements.txt:

Bash
pip install streamlit pandas numpy matplotlib fpdf2
Avvio dell'Applicazione
Esegui il server Streamlit locale tramite il terminale:

Bash
streamlit run app.py
📄 Struttura dei Report Generati
Ogni documento PDF esportato dalla suite include:

Header Istituzionale: Intestazione grafica con schema colore personalizzato in base al tipo di modulo (Blue Navy per Termico, Verde Smeraldo per UTA).

Anagrafica Commessa: Dati completi del committente e dell'ubicazione dell'immobile.

Dati di Sintesi e Input: Tracciabilità completa dei parametri geometrici e termofisici inseriti.

Specifiche Tecniche di Output: Tabelle chiare recanti i dati di calcolo ingegneristici.

Data Viz: Grafici vettoriali integrati direttamente nel layout (Pie Chart per la ripartizione percentuale dei carichi o Bar Chart per il confronto normativo delle portate).

🔒 Licenza e Proprietà
Proprietà Riservata - Sviluppato da P.Ind. Pino Mazzitelli.
Tutti i diritti sul codice sorgente, logiche di calcolo e layout grafici sono riservati a VIZATRONIX ENGINEERING SOLUTIONS. È vietata la riproduzione e la ridistribuzione non autorizzata.
