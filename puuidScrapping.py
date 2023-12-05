import csv
import json
import os
import requests
from urllib.parse import quote
from time import sleep

key = os.getenv('key')

def get_summoner_puuid(summoner_name, max_retries=3, retry_delay=5):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/{quote(summoner_name)}?api_key={key}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gérer les erreurs HTTP
            data = response.json()
            return data.get("puuid", None)
        except requests.RequestException as e:
            print(f"Erreur lors de la requête pour {summoner_name}: {e}")
            print(f"Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} secondes.")
            sleep(retry_delay)

    print(f"Échec après {max_retries} tentatives. Aucune réponse valide pour {summoner_name}.")
    return None

def read_existing_log(log_file):
    existing_summoners = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            for line in log:
                if "Traitement réussi pour" in line:
                    summoner_name = line.split("pour")[1].strip()
                    existing_summoners.add(summoner_name)
    return existing_summoners

def process_csv(input_file, output_file, log_file, progress_interval=20):
    puuid_list = []
    existing_summoners = read_existing_log(log_file)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        #next(reader)  # Ignorer l'en-tête
        for i, row in enumerate(reader, 1):
            summoner_name = row[0]

            # Vérifiez si le summoner a déjà été traité
            if summoner_name in existing_summoners:
                print(f"{summoner_name} a déjà été traité. Ignoré.")
                continue

            puuid = get_summoner_puuid(summoner_name)
            if puuid:
                puuid_list.append([puuid])

                # Enregistrez le progrès dans le fichier de journalisation
                with open(log_file, 'a') as log:
                    log.write(f" Traitement réussi pour {summoner_name}\n")

                # Affichez le progrès tous les progress_interval summoners
                if i % progress_interval == 0:
                    print(f"\nTraitement réussi pour {i} summoners.\n")

                # Écrivez dans le fichier de sortie à chaque itération
                with open(output_file, mode='a', newline='') as result_csv:
                    writer = csv.writer(result_csv)
                    writer.writerows([[puuid]])
                    # Ajoutez la possibilité de faire des pauses entre les exécutions successives
                    # pour respecter les limitations de taux de l'API.
                    sleep_time = 0.5
                    sleep(sleep_time)

    print("Toutes les requêtes ont été traitées avec succès.")

if __name__ == "__main__":
    input_csv_path = 'summonerIdList.csv'
    output_csv_path = 'puuidIdList.csv'
    log_file_path = 'executionPuuid_log.txt'

    try:
        print("Début du traitement...")
        process_csv(input_csv_path, output_csv_path, log_file_path)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


