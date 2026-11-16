import time
import yaml
from pathlib import Path
from litellm import completion
from litellm.exceptions import ServiceUnavailableError, RateLimitError


def carica_config():
    percorso_configurato = Path(__file__).parent / "api_keys.yaml"
    with open(percorso_configurato, "r", encoding="utf-8") as f:
        configurato = yaml.safe_load(f)
        
    print("Scegli quale modello utilizzare:")
    print("1) Google (gemini/gemini-3.8-flash)")
    print("2) OpenAI (openai/gpt-5.6-terra)")
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


def richiesta_stream(api_key, model, prompt, max_tentativi=3):
    tentativo = 0
    attesa = 2

    while tentativo < max_tentativi:
        try:
            print("\nRisposta: ", end="", flush=True)
            
            # LiteLLM gestisce la chiamata in streaming per tutti i provider
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                api_key=api_key,
                stream=True
            )
            
            for chunk in response:
                delta = chunk.choices[0].delta
                contenuto = getattr(delta, "content", None)
                if contenuto:
                    print(contenuto, end="", flush=True)
            print("\n")
            return
            
        except (ServiceUnavailableError, RateLimitError):
            tentativo += 1
            if tentativo < max_tentativi:
                print(f"\n[Server sovraccarico o limite raggiunto. Riprovo tra {attesa}s... ({tentativo}/{max_tentativi})]")
                time.sleep(attesa)
                attesa *= 2
            else:
                print(f"\nErrore: Impossibile ottenere risposta dopo {max_tentativi} tentativi.")
        except Exception as e:
            print(f"\nErrore imprevisto: {e}")
            break


if __name__ == "__main__":
    api_key, model, nome_provider = carica_config()
    print(f"\nAvviato con successo: {nome_provider} ({model})")

    while True:
        print("Inserisci il prompt (o 'exit' per uscire):")
        prompt = input()

        if prompt.lower() == "exit":
            print("Uscita dal programma.")
            break

        richiesta_stream(api_key, model, prompt)
        api_key, model, nome_provider = carica_config()