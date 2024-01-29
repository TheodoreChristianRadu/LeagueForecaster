import os
import requests
from urllib.parse import quote
from time import sleep

key = os.getenv('key')
summoner_name="Drosai"

try:

    url1 = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={key}"
    response = requests.get(url1)
    response.raise_for_status()  # Gérer les erreurs HTTP
    data = response.json()
    puuid = data.get("puuid", None)
    print(puuid)

    url2 = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count=50&api_key={key}"
    response = requests.get(url2)
    response.raise_for_status()  # Gérer les erreurs HTTP
    historicList= response.json()
    print(historicList)

    matchList = []
    for i in historicList:
        url3 = f"https://europe.api.riotgames.com/lol/match/v5/matches/{i}?api_key={key}"
        response = requests.get(url3)
        response.raise_for_status()  # Gérer les erreurs HTTP
        unfilteredMatch= response.json()['info']
        filteredMatch = {key: value for key, value in unfilteredMatch.items() if key in ['gameDuration', 'participants']}
        matchList.append(filteredMatch)
    print(matchList[0])

except requests.RequestException as e:
    print(f"Erreur lors de la requête pour {summoner_name}: {e}")
except Exception as e:
    print("An error occurred:", e)

