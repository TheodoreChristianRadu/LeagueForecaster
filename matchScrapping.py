import csv
import json
import os
import requests
from urllib.parse import quote
from time import sleep

key = os.getenv('key')

def get_match(matchId, max_retries=2, retry_delay=1):
    
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={key}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gérer les erreurs HTTP
            unfilteredMatch= response.json()['info']
            filteredMatch = {key: value for key, value in unfilteredMatch.items() if key in ['gameDuration', 'participants']}
            return filteredMatch
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

    with open(output_file, 'a') as fichier_json:

        if used_historic == set():
            fichier_json.write('[\n')

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
                            matchList.append(match)

                # Enregistrez le progrès dans le fichier de journalisation
                with open(log_file, 'a') as log:
                    log.write(f" Traitement réussi pour {''.join(matchHistoricList)}\n")

                # Affichez le progrès tous les progress_interval summoners
                if i % progress_interval == 0:
                    print(f"\nTraitement réussi pour {i} summoners.\n")
                
                if i != 1:
                    fichier_json.write(',\n')
                # Utilisation de json.dump pour écrire chaque ligne dans le fichier
                json.dump(matchList, fichier_json, indent=4)

        fichier_json.write('\n]')
        print("Toutes les requêtes ont été traitées avec succès.")

if __name__ == "__main__":
    input_csv_path = 'historicList.csv'
    output_csv_path = 'matchList.json'
    log_file_path = 'executionMatch_log.txt'

    try:
        print(f"Début du traitement de {input_csv_path}")
        process_csv(input_csv_path, output_csv_path, log_file_path)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")