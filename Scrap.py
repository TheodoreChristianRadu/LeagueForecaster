import os
import requests
from urllib.parse import quote

key = os.getenv('key')
name = quote("Sir Forty")
tag = "EUW"

url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={key}"
# url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={key}"

print(requests.get(url).json())
