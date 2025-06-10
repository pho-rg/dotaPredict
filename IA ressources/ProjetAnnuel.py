import time
from time import sleep
import requests
import json
import pandas as pd
from datetime import datetime


def getMatchesPro (lastMatchId = None):
    """Methode pour recuperer les 100 dernier matchs """
    base_url = "https://api.opendota.com/api/proMatches"
    if lastMatchId:
        url = f"{base_url}?less_than_match_id={lastMatchId}"
    else:
        url = base_url

    try:
        response = requests.get(url)
        response.raise_for_status()

        matchs = response.json()
        matchsId = [match['match_id'] for match in matchs]
        time.sleep(2)
        return matchsId

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des matchs: {e}")
        return None


def saveDataFrameToJson (matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"SauvgardeProMaths{datetime.now().date()}.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)

def main():
    print("debut programme")
    """Recuperation des 100 derniers matchs"""
    matchsId = getMatchesPro()
    lastMatchId = min(matchsId)

    """Recuperation des 10 000 derniers matchs"""
    while True :
        matchsIdNext = getMatchesPro(lastMatchId)
        matchsId.extend(matchsIdNext)
        lastMatchId = min(matchsIdNext)
        if len(matchsId) > 10000:
            print("end while")
            break
        print(matchsIdNext)
        print(len(matchsId))

    saveDataFrameToJson(pd.DataFrame(matchsId))

if __name__ == '__main__':
    main()