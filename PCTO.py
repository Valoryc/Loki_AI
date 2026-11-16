import os
import time
import sqlite3
import yaml
from pathlib import Path
from litellm import completion
from litellm.exceptions import ServiceUnavailableError, RateLimitError


def inizializza_db():
    """Crea il database SQLite e la tabella se non esistono già"""
    conn = sqlite3.connect("cronologia_chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messaggi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            modello TEXT,
            prompt TEXT,
            risposta TEXT
        )
    """)
    conn.commit()
    conn.close()


def salva_messaggio(modello, prompt, risposta):
    """Salva una nuova interazione nel database"""
    conn = sqlite3.connect("cronologia_chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messaggi (modello, prompt, risposta) 
        VALUES (?, ?, ?)
    """, (modello, prompt, risposta))
    conn.commit()
    conn.close()


def carica_config():
    percorso_configurato = Path(__file__).parent / "api_keys.yaml"
    with open(percorso_configurato, "r", encoding="utf-8") as f:
        configurato = yaml.safe_load(f)
        
    print("Scegli quale modello utilizzare:")
    print("1) Google (gemini/gemini-3.8-flash)")
    print("2) OpenAI (openai/gpt-4o-mini)")
    print("3) Claude (anthropic/claude-sonnet-4-6)")
    
    scelta = input("Inserisci il numero corrispondente (1, 2 o 3): ").strip()
    
    if scelta == "1":
        dati = configurato["Google"]
        nome = "Google"
    elif scelta == "2":
        dati = configurato["OpenAI"]
        nome = "OpenAI"
    elif scelta == "3":
        dati = configurato["Claude"]
        nome = "Claude"
    else:
        print("Scelta non valida, uso di default Google.")
        dati = configurato["Google"]
        nome = "Google"
        
    return dati["api_key"], dati["model"], nome


def richiesta_stream(api_key, model, nome_provider, prompt, max_tentativi=3):
    # Passa la chiave corretta nelle variabili di ambiente richieste da LiteLLM
    if nome_provider == "Google":
        os.environ["GEMINI_API_KEY"] = api_key
    elif nome_provider == "OpenAI":
        os.environ["OPENAI_API_KEY"] = api_key
    elif nome_provider == "Claude":
        os.environ["ANTHROPIC_API_KEY"] = api_key

    tentativo = 0
    attesa = 2
    risposta_completa = ""

    while tentativo < max_tentativi:
        try:
            print("\nRisposta: ", end="", flush=True)
            
            # LiteLLM userà la chiave correttamente impostata nell'ambiente
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            for chunk in response:
                delta = chunk.choices[0].delta
                contenuto = getattr(delta, "content", None)
                if contenuto:
                    print(contenuto, end="", flush=True)
                    risposta_completa += contenuto
                    
            print("\n")
            
            # Salva automaticamente nel database SQLite
            salva_messaggio(model, prompt, risposta_completa)
            return
            
        except (ServiceUnavailableError, RateLimitError) as e:
            tentativo += 1
            if tentativo < max_tentativi:
                print(f"\n[Server sovraccarico o limite raggiunto. Riprovo tra {attesa}s... ({tentativo}/{max_tentativi})]")
                time.sleep(attesa)
                attesa *= 2
            else:
                print(f"\nErrore: Impossibile ottenere risposta dopo {max_tentativi} tentativi. Dettaglio: {e}")
        except Exception as e:
            print(f"\nErrore imprevisto: {e}")
            break


if __name__ == "__main__":
    # Inizializza il database SQLite all'avvio
    inizializza_db()
    
    api_key, model, nome_provider = carica_config()
    print(f"\nAvviato con successo: {nome_provider} ({model}) - Database SQLite attivo!")

    while True:
        print("\nInserisci il prompt (o 'exit' per uscire):")
        prompt = input()

        if prompt.lower() == "exit":
            print("Uscita dal programma.")
            break

        richiesta_stream(api_key, model, nome_provider, prompt)