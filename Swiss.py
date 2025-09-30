#!/usr/bin/env python3
import requests
import random
import os
import sys

TEAM_ID = "darkonswiss-dos"

# Read token from environment variable
API_TOKEN = os.getenv("KEY")
if not API_TOKEN:
    sys.exit("Error: API token not found. Please set KEY environment variable.")

# Tournament options
OPTIONS = [
    {"name": "DOS Blitz",  "clock": {"limit": 180,  "increment": 0}, "nbRounds": 11},   # 3+0
    {"name": "DOS Rapid", "clock": {"limit": 600,  "increment": 0}, "nbRounds": 9},    # 10+0
    {"name": "DOS Bullet","clock": {"limit": 60,   "increment": 0}, "nbRounds": 20},   # 1+0
    {"name": "DOS Bullet Increment","clock": {"limit": 120,  "increment": 1}, "nbRounds": 15},   # 2+1
    {"name": "DOS Classical","clock": {"limit": 1800, "increment": 0}, "nbRounds": 5},
]

def read_description():
    path = os.path.join(os.path.dirname(__file__), "description.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Welcome to our Swiss tournament!"

def create_swiss():
    option = random.choice(OPTIONS)
    description = read_description()
    daysInAdvance: 1
    payload = {
        "name": option["name"],
        "clock.limit": option["clock"]["limit"],
        "clock.increment": option["clock"]["increment"],
        "nbRounds": option["nbRounds"],
        "rated": "true",
        "description": description,
    }

    url = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    print(f"Creating tournament: {payload['name']} "
          f"({payload['clock.limit']//60}+{payload['clock.increment']}, "
          f"{payload['nbRounds']} rounds)")

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        data = r.json()
        print("✅ Tournament created!")
        print("ID:", data.get("id"))
        print("Name:", data.get("name"))
        print("Starts at:", data.get("startsAt"))
        print("Rounds:", data.get("nbRounds"))
        print("URL:", f"https://lichess.org/swiss/{data.get('id')}")
    else:
        print("❌ Error:", r.status_code, r.text)

if __name__ == "__main__":
    create_swiss()
