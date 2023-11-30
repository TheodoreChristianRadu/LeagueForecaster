import os
import requests
from urllib.parse import quote

key = os.getenv('key')

name = quote("loubartheo")
tag = "EUW"

url1 = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={key}"
# url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={key}"

#print(requests.get(url1).json())

puuid=requests.get(url1).json()['puuid']
gametype= '420' #cf parameter.txt
combien=10

url2 = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={gametype}&start=0&count={combien}&api_key={key}"

#print(requests.get(url2).json())
gamesId=requests.get(url2).json()
game1=gamesId[0]

url3= f"https://europe.api.riotgames.com/lol/match/v5/matches/{game1}?api_key={key}"

print(requests.get(url3).json())




