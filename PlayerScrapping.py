import csv
import json
import os
from time import sleep
import requests
from urllib.parse import quote

key = os.getenv('key')

gameType= "RANKED_SOLO_5x5"
tier=["IRON","BRONZE","SILVER","GOLD","PLATINUM","EMERALD","DIAMOND","MASTER","GRANDMASTER","CHALLENGER"]
division=["I","II","III","IV"]
nbPage=1

hightier= ["MASTER","GRANDMASTER","CHALLENGER"]


chemin_fichier_csv = 'summonerIdList.csv'
listSummonerId= []
v=0

# Utilisez la fonction open pour créer ou ouvrir le fichier CSV en mode écriture ('w')
with open(chemin_fichier_csv, mode='w', newline='') as fichier_csv:
    # Créez un objet writer à l'aide du module csv
    writer = csv.writer(fichier_csv)


    # Utilisez la méthode writerows pour insérer les données dans le fichier CSV
    for i in tier:
        if i in hightier:
            v+=1
            print(v)
            for k in range(1,6):
                sleep(3)
                url1 = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{i}/{"I"}?page={k}&api_key={key}"

                response = requests.get(url1)
                
                # Vérifiez si la requête a réussi (code d'état 200)
                if response.status_code == 200:
                    request1 = json.loads(response.text)
                    for L in request1:
                        listSummonerId.append([L.get('summonerId')])
                else:
                    print(f"Erreur de requête: {response.status_code}")
                    print(json.loads(response.text)) 
        else:
            for j in division:
                v+=1
                print(v)
                for k in range(1,6):
                    sleep(3)
                    url1 = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{i}/{j}?page={k}&api_key={key}"
                    response = requests.get(url1)
                
                    # Vérifiez si la requête a réussi (code d'état 200)
                    if response.status_code == 200:
                        request1 = json.loads(response.text)
                        for L in request1:
                            listSummonerId.append([L.get('summonerId')])
                    else:
                        print(f"Erreur de requête: {response.status_code}")
                        print(json.loads(response.text)) 
    print(len(listSummonerId))
    writer.writerows(listSummonerId)



