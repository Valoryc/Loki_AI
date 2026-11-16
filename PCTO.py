import yaml
from google import genai
from pathlib import Path


def carica_chiavi():
    percorso_configurato = Path(__file__).parent / "api_keys.yaml"
    with open(percorso_configurato, "r") as f:
        configurato = yaml.safe_load(f)
    return configurato["Google"] ["api_key"], configurato["Google"] ["model"]


def crea_client():
    api_key, model = carica_chiavi()
    client = genai.Client(api_key=api_key)
    return client, model


def richiesta(client, model, prompt):
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    client, model = crea_client()  # Creato una volta sola

    while True:
        print("Inserisci il prompt (o 'exit' per uscire):")
        prompt = input()

        if prompt.lower() == "exit":
            print("Uscita dal programma.")
            break

        testo_generato = richiesta(client, model, prompt)
        print(testo_generato)  # Stampato ad ogni risposta