import csv
import json
import os
import requests
from urllib.parse import quote
from time import sleep

key = os.getenv('key')


def get_historic(puuid, max_retries=3, retry_delay=5):
    
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count=50&api_key={key}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gérer les erreurs HTTP
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête pour {puuid}: {e}")
            print(f"Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} secondes.")
            sleep(retry_delay)

    print(f"Échec après {max_retries} tentatives. Aucune réponse valide pour {puuid}.")
    return None

def read_existing_log(log_file):
    existing_summoners = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            for line in log:
                if "Traitement réussi pour" in line:
                    puuid = line.split("pour")[1].strip()
                    existing_summoners.add(puuid)
    return existing_summoners

def process_csv(input_file, output_file, log_file, progress_interval=20):
    used_puuid = read_existing_log(log_file)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader, 1):
            puuid = row[0]

            # Vérifiez si le summoner a déjà été traité
            if puuid in used_puuid:
                print(f"{puuid} a déjà été traité. Ignoré.")
                continue

            historic = get_historic(puuid) #a corriger
            if historic:

                # Enregistrez le progrès dans le fichier de journalisation
                with open(log_file, 'a') as log:
                    log.write(f" Traitement réussi pour {puuid}\n")

                # Affichez le progrès tous les progress_interval summoners
                if i % progress_interval == 0:
                    print(f"\nTraitement réussi pour {i} summoners.\n")

                # Écrivez dans le fichier de sortie à chaque itération
                with open(output_file, mode='a', newline='') as result_csv:
                    writer = csv.writer(result_csv)
                    writer.writerows([list(historic)])
                    # Ajoutez la possibilité de faire des pauses entre les exécutions successives
                    # pour respecter les limitations de taux de l'API.
                    sleep_time = 0.5
                    sleep(sleep_time)

    print("Toutes les requêtes ont été traitées avec succès.")

if __name__ == "__main__":
    input_csv_path = 'puuidIdList.csv'
    output_csv_path = 'historicList.csv'
    log_file_path = 'executionHistoric_log.txt'

    try:
        print("Début du traitement...")
        process_csv(input_csv_path, output_csv_path, log_file_path)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")