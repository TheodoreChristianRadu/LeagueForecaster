import os
import requests

key = os.getenv('key')
name = "loubartheo"
tag = "EUW"

url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={key}"
# url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={key}"

print(requests.get(url).json())
