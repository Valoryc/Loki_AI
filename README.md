# 🤖 Loki_AI

> Un assistente conversazionale CLI multi-provider in Python con risposte in streaming, gestione intelligente degli errori e salvataggio automatico su SQLite.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/Powered%20by-LiteLLM-orange.svg)](https://docs.litellm.ai/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)

## 📋 Panoramica del Progetto

**Loki_AI** è un'applicazione a riga di comando (CLI) progettata per interagire con diversi Large Language Models (LLM) da un'unica interfaccia unificata[cite: 6, 7]. Permette all'utente di scegliere all'avvio quale modello utilizzare, ricevendo risposte fluide in tempo reale e archiviando ogni conversazione in locale.

### ✨ Funzionalità Principali
* **Architettura Multi-Provider:** Supporto nativo per **Google Gemini** (`gemini-3.8-flash`), **OpenAI** (`gpt-4o-mini`) e **Anthropic Claude** (`claude-sonnet-4-6`) tramite la libreria `LiteLLM`.
* **Streaming in Tempo Reale:** Visualizzazione progressiva della risposta token dopo token direttamente nel terminale, riducendo la latenza percepita.
* **Persistenza Dati con SQLite:** Creazione automatica del database `cronologia_chat.db` per salvare timestamp, modello utilizzato, prompt e risposta completa di ogni interazione.
* **Resilienza e Backoff Esponenziale:** Sistema automatico di *retry* (fino a 3 tentativi con attesa crescente) in caso di sovraccarico dei server (`ServiceUnavailableError`) o raggiungimento dei limiti di richieste (`RateLimitError`).

---

## 🛠️ Stack Tecnologico

* **Linguaggio:** Python 3[cite: 6]
* **Orchestrazione LLM:** [LiteLLM](https://github.com/BerriAI/litellm)[cite: 6]
* **Database:** SQLite3 (libreria standard Python)[cite: 6]
* **Configurazione:** PyYAML (`.yaml`)[cite: 6]

---

## 🚀 Installazione e Configurazione

1. **Clona il repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[tuo-username]/Loki_AI.git
   cd Loki_AI

   Crea e attiva un ambiente virtuale:

### 1 Crea e attiva un ambiente virtuale:

python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

### 2 Installa le dipendenze necessarie:

pip install litellm pyyaml

### 3 Configura le chiavi API:
Crea un file chiamato api_keys.yaml nella cartella principale del progetto (allo stesso livello di PCTO.py) seguendo questa struttura[cite:3,6]:

Google:
  api_key: "LA_TUA_CHIAVE_GEMINI"
  model: "gemini/gemini-3.8-flash"

OpenAI:
  api_key: "LA_TUA_CHIAVE_OPENAI"
  model: "openai/gpt-4o-mini"

Claude:
  api_key: "LA_TUA_CHIAVE_ANTHROPIC"
  model: "anthropic/claude-sonnet-4-6"

##💻 Utilizzo

Avvia lo script principale dal terminale[cite: 6]:

python PCTO.py


All'avvio ti verrà chiesto di selezionare il provider desiderato[cite: 6]:PlaintextScegli quale modello utilizzare:
1) Google (gemini/gemini-3.8-flash)
2) OpenAI (openai/gpt-4o-mini)
3) Claude (anthropic/claude-sonnet-4-6)
Inserisci il numero corrispondente (1, 2 o 3):

Digita il tuo prompt e premi Invio per ricevere la risposta in streaming[cite: 6].
Ogni scambio viene salvato automaticamente nella tabella messaggi del file cronologia_chat.db.
Digita exit per chiudere il programma[cite: 6].

##🗺️ Sviluppi Futuri
Aggiunta della memoria conversazionale (invio dello storico dei messaggi al modello per mantenere il contesto).

Comando dedicato per consultare o esportare la cronologia salvata su SQLite[cite: 6].

Sviluppo di un'interfaccia grafica web (es. con Streamlit o Chainlit).

##🤝 Contatti
Progetto sviluppato da [Tuo Nome e Cognome] – Se hai suggerimenti o vuoi confrontarti sul codice, contattami pure!

LinkedIn: [www.linkedin.com/in/valentina-avitabile]
