import time
from time import sleep
import requests
import json
import pandas as pd
from datetime import datetime

from docutils.nodes import header
from intake.source.cache import display


def getMatchDetailsPro (matchs):
    """Methode pour recuperer les details d'un matche par son Id"""

    matchFiltre = []

    for match in matchs:

            if("picks_bans" in match):
                selected_fields = {"match_id": match["match_id"],
                               "radiant_win": match["radiant_win"],
                               "radiant_picks_ids": [entry["hero_id"] for entry in match['picks_bans'] if
                                                   entry['is_pick'] and entry['team'] == 0],
                               "dire_picks_ids": [entry["hero_id"] for entry in match['picks_bans'] if
                                                   entry['is_pick'] and entry['team'] == 1],
                               "radiant_bans_ids": [entry["hero_id"] for entry in match['picks_bans'] if
                                                  not entry['is_pick'] and entry['team'] == 0],
                               "dire_bans_ids": [entry["hero_id"] for entry in match['picks_bans'] if
                                                  not entry['is_pick'] and entry['team'] == 1],
                                # "league_id":match['leagueid'],
                                "version":match['version'],
                                # "cluster":match['cluster'],
                                # "lobby_type":match['lobby_type'],
                                # "game_mode":match['game_mode']
                                }
            print(selected_fields)
            matchFiltre.append(selected_fields)

    return pd.DataFrame(matchFiltre)

def openJson(path):

    with open (path) as json_file:
        data = json.load(json_file)

    return data

def saveDataFrameToJson (matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"SauvgardeProMatchsFiltre.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)


def main():
    print("debut programme")
    pathData = r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMatchsLigneParLigne_2025-04-23.json"
    matchsProDetails = []

    with open(pathData, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    details = getMatchDetailsPro(data)
    if details is not None:
        saveDataFrameToJson(details)
        print(details)
    else:
        print("No matchs found or api limit request")

if __name__ == '__main__':
    main()