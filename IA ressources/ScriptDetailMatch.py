import time
import requests
import json
import pandas as pd
from datetime import datetime

def getMatchDetailsPro (matchsId):
    """Methode pour recuperer les details d'un matche par son Id"""

    url = f"https://api.opendota.com/api/matches/"
    apiKey = "api_key=d008b8a3-66d1-4567-998c-9b88d144c65a"
    matchDetails = []

    for matchId in matchsId:
        urlWithMatchId = url + f"{matchId}?"+ apiKey
        try:
            response = requests.get(urlWithMatchId)
            response.raise_for_status()
            details = response.json()
            if("picks_bans" in details):
                selected_fields = {"match_id": details["match_id"],
                               "radiant_win": details["radiant_win"],
                               "picks_id_team_0": [entry["hero_id"] for entry in details['picks_bans'] if
                                                   entry['is_pick'] and entry['team'] == 0],
                               "picks_id_team_1": [entry["hero_id"] for entry in details['picks_bans'] if
                                                   entry['is_pick'] and entry['team'] == 1],
                               "bans_id_team_0": [entry["hero_id"] for entry in details['picks_bans'] if
                                                  not entry['is_pick'] and entry['team'] == 0],
                               "bans_id_team_1": [entry["hero_id"] for entry in details['picks_bans'] if
                                                  not entry['is_pick'] and entry['team'] == 1],
                                "league_id":details['leagueid'],
                                "version":details['version'],
                                "cluster":details['cluster'],
                                "lobby_type":details['lobby_type'],
                                "game_mode":details['game_mode']}
            matchDetails.append(selected_fields)
            print(len(matchDetails))
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la récupération des détails du match {matchId}: {e}")
            continue

        except KeyError as ke:
            print(f"⚠️ Clé manquante dans les données du match {matchId}: {ke}")
            continue

    return pd.DataFrame(matchDetails)

def openJson(path):

    with open (path) as json_file:
        data = json.load(json_file)

    return data

def saveDataFrameToJson (matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"SauvgardeProMatchs{datetime.now().date()}.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)


def main():
    print("debut programme")
    pathMathesId = r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMaths2025_05_20.json"

    matchesId = list(openJson(pathMathesId).values())
    df = pd.DataFrame(matchesId, columns=["match_id"])
    matchsId = df.head(9000)["match_id"]
    details = getMatchDetailsPro(matchsId)
    saveDataFrameToJson(details)

if __name__ == '__main__':
    main()