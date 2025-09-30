#!/usr/bin/env python3
import requests
import os
import sys
import random
from datetime import datetime, timedelta
import pytz

TEAM_ID = "darkonswiss-dos"

# Token aus ENV
API_TOKEN = os.getenv("KEY")
if not API_TOKEN:
    sys.exit("Error: API token not found. Please set KEY environment variable.")

# Turnieroptionen mit klaren Namen
OPTIONS = [
    # Bullet
    {"name": "DOS Bullet Swiss",          "clock": {"limit": 60,   "increment": 0},  "nbRounds": 20},  # 1+0
    {"name": "DOS Bullet Increment Swiss","clock": {"limit": 120,  "increment": 1},  "nbRounds": 15},  # 2+1

    # Blitz
    {"name": "DOS Blitz Swiss",           "clock": {"limit": 180,  "increment": 0},  "nbRounds": 13},  # 3+0
    {"name": "DOS Blitz Increment Swiss", "clock": {"limit": 180,  "increment": 2},  "nbRounds": 13},  # 3+2
    {"name": "DOS Blitz Swiss",           "clock": {"limit": 300,  "increment": 0},  "nbRounds": 11},  # 5+0
    {"name": "DOS Blitz Increment Swiss", "clock": {"limit": 300,  "increment": 3},  "nbRounds": 11},  # 5+3

    # Rapid
    {"name": "DOS Rapid Swiss",           "clock": {"limit": 600,  "increment": 0},  "nbRounds": 9},   # 10+0
    {"name": "DOS Rapid Increment Swiss", "clock": {"limit": 600,  "increment": 5},  "nbRounds": 9},   # 10+5
    {"name": "DOS Rapid Swiss",           "clock": {"limit": 900,  "increment": 0},  "nbRounds": 9},   # 15+0
    {"name": "DOS Rapid Increment Swiss", "clock": {"limit": 900,  "increment": 10}, "nbRounds": 9},   # 15+10

    # Classical
    {"name": "DOS Classical Swiss",       "clock": {"limit": 1800, "increment": 0},  "nbRounds": 5},   # 30+0
    {"name": "DOS Classical Increment Swiss",
                                          "clock": {"limit": 1200, "increment": 10}, "nbRounds": 5},   # 20+10
]

def utc_millis_tomorrow_this_hour():
    """Berechne Startzeit: Morgen, gleiche Stunde wie jetzt (UTC)"""
    utc = pytz.utc
    now = datetime.now(utc)
    start = datetime(now.year, now.month, now.day, now.hour, 0, tzinfo=utc) + timedelta(days=1)
    return int(start.timestamp() * 1000), start

def create_swiss():
    option = random.choice(OPTIONS)
    startDate, start_dt = utc_millis_tomorrow_this_hour()

    payload = {
    "name": f"{option['name']} {start_dt.strftime('%b%d-%Hh')}",
    "clock.limit": option["clock"]["limit"],
    "clock.increment": option["clock"]["increment"],
    "nbRounds": option["nbRounds"],
    "rated": "true",
    "description": "Daily Swiss (created 1 day in advance)",
    "startDate": startDate
}

    url = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    print(f"➡️ Creating: {payload['name']} "
          f"({payload['clock.limit']//60}+{payload['clock.increment']}, "
          f"{payload['nbRounds']}R, Start {start_dt} UTC)")

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        data = r.json()
        print("✅ Tournament created!")
        print("URL:", f"https://lichess.org/swiss/{data.get('id')}")
    else:
        print("❌ Error:", r.status_code, r.text)

if __name__ == "__main__":
    create_swiss()
