import os
import json
import requests
from xml.sax.saxutils import escape

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
        "current": mmr["current"]["tier"]["name"],
        "rr": mmr["current"]["rr"],
        "elo": mmr["current"]["elo"],
        "last_change": mmr["current"]["last_change"]
    }
}

# ---------------- WRITE JSON ----------------
with open("valorant.json", "w") as f:
    json.dump(output, f, indent=2)

# ---------------- GENERATE SVG ----------------
name = escape(output["player"]["name"])
tag = escape(output["player"]["tag"])
level = output["player"]["level"]
region = output["player"]["region"].upper()

rank = escape(output["rank"]["current"])
rr = output["rank"]["rr"]
elo = output["rank"]["elo"]
change = output["rank"]["last_change"]

change_color = "#4caf50" if change >= 0 else "#ff5252"
change_symbol = "▲" if change >= 0 else "▼"

svg = f"""
<svg width="420" height="200" viewBox="0 0 420 200"
     xmlns="http://www.w3.org/2000/svg">

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f1923"/>
      <stop offset="100%" stop-color="#1c252e"/>
    </linearGradient>
  </defs>

  <rect width="420" height="200" rx="16" fill="url(#bg)"/>
  <rect width="420" height="6" fill="#ff4655"/>

  <text x="24" y="42" font-size="24"
        font-family="Segoe UI, Arial"
        fill="#ff4655" font-weight="bold">
    {name}
  </text>

  <text x="130" y="42" font-size="14"
        font-family="Segoe UI, Arial"
        fill="#9faec0">
    #{tag}
  </text>

  <text x="24" y="70" font-size="14"
        font-family="Segoe UI, Arial"
        fill="#ffffff">
    Level: <tspan fill="#9faec0">{level}</tspan>
  </text>

  <text x="140" y="70" font-size="14"
        font-family="Segoe UI, Arial"
        fill="#ffffff">
    Region: <tspan fill="#9faec0">{region}</tspan>
  </text>

  <rect x="24" y="90" width="372" height="86" rx="12" fill="#121a23"/>

  <text x="40" y="120" font-size="20"
        font-family="Segoe UI, Arial"
        fill="#f5c542" font-weight="bold">
    {rank}
  </text>

  <text x="40" y="148" font-size="14"
        font-family="Segoe UI, Arial"
        fill="#ffffff">
    RR: <tspan fill="#9faec0">{rr}</tspan>
  </text>

  <text x="140" y="148" font-size="14"
        font-family="Segoe UI, Arial"
        fill="#ffffff">
    ELO: <tspan fill="#9faec0">{elo}</tspan>
  </text>

  <text x="260" y="148" font-size="14"
        font-family="Segoe UI, Arial"
        fill="{change_color}">
    {change_symbol} {change}
  </text>

</svg>
"""

with open("valorant-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Valorant JSON and SVG card generated")
