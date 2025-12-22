import os
import json
import requests

NAME = "milut"
TAG = "aep"
REGION = "ap"
PLATFORM = "pc"

API_KEY = os.environ["HENRIK_API_KEY"]

HEADERS = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

account_url = f"https://api.henrikdev.xyz/valorant/v1/account/{NAME}/{TAG}"
mmr_url = f"https://api.henrikdev.xyz/valorant/v3/mmr/{REGION}/{PLATFORM}/{NAME}/{TAG}"

account = requests.get(account_url, headers=HEADERS).json()["data"]
mmr = requests.get(mmr_url, headers=HEADERS).json()["data"]

output = {
    "player": {
        "name": account["name"],
        "tag": account["tag"],
        "level": account.get("account_level"),
        "region": REGION
    },
    "rank": {
        "current": mmr["currenttierpatched"],
        "rr": mmr["ranking_in_tier"],
        "elo": mmr.get("elo")
    }
}

with open("valorant.json", "w") as f:
    json.dump(output, f, indent=2)

print("Valorant data generated")
