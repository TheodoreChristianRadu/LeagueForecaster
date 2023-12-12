import csv
import json
import os
import requests
from urllib.parse import quote
from time import sleep

#key = os.getenv('key')
key = f"RGAPI-e5c4e2fc-d0ae-47d0-bfd8-c57250fc3f13"


def get_match(matchId, max_retries=3, retry_delay=5):
    
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={key}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gérer les erreurs HTTP
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête pour {matchId}: {e}")
            print(f"Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} secondes.")
            sleep(retry_delay)

    print(f"Échec après {max_retries} tentatives. Aucune réponse valide pour {matchId}.")
    return None

def read_existing_log(log_file):
    existing_summoners = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            for line in log:
                if "Traitement réussi pour" in line:
                    matchId = line.split("pour")[1].strip()
                    existing_summoners.add(matchId)
    return existing_summoners

def process_csv(input_file, output_file, log_file, progress_interval=5):
    used_historic = read_existing_log(log_file)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader, 1):
            matchHistoricList = row

            # Vérifiez si le summoner a déjà été traité
            if ''.join(matchHistoricList) in used_historic:
                print(f"Déjà été traité.")
                continue
            
            matchList =[]
            for id in matchHistoricList:
                if id != '':
                    sleep_time = 0.5
                    sleep(sleep_time)
                    match = get_match(id) #a corriger
                    if match:
                        matchList.append(json.dumps(match))

            # Enregistrez le progrès dans le fichier de journalisation
            with open(log_file, 'a') as log:
                log.write(f" Traitement réussi pour {''.join(matchHistoricList)}\n")

            # Affichez le progrès tous les progress_interval summoners
            if i % progress_interval == 0:
                print(f"\nTraitement réussi pour {i} summoners.\n")

            with open(output_file, 'w') as fichier_json:
                # Utilisation de json.dump pour écrire chaque ligne dans le fichier
                json.dump(matchList, fichier_json)
                fichier_json.write('\n')


    print("Toutes les requêtes ont été traitées avec succès.")

if __name__ == "__main__":
    input_csv_path = 'historicList1.csv'
    output_csv_path = 'matchList.json'
    log_file_path = 'executionMatch_log.txt'

    try:
        print("Début du traitement...")
        process_csv(input_csv_path, output_csv_path, log_file_path)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")