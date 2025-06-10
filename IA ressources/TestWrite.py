import time
import requests
import json
import pandas as pd
from datetime import datetime


def getMatchDetailsPro(matchsId, save_path):
    """Methode pour recuperer les details d'un matche par son Id et sauvegarder chaque match récupéré"""

    url = "https://api.opendota.com/api/matches/"

    with open(save_path, 'a', encoding='utf-8') as outfile:
        for matchId in matchsId:
            urlWithMatchId = url + f"{matchId}"
            try:
                response = requests.get(urlWithMatchId)
                response.raise_for_status()
                details = response.json()
                """if "picks_bans" in details:
                    selected_fields = {
                        "match_id": details["match_id"],
                        "radiant_win": details["radiant_win"],
                        "picks_id_team_0": [entry["hero_id"] for entry in details['picks_bans'] if entry['is_pick'] and entry['team'] == 0],
                        "picks_id_team_1": [entry["hero_id"] for entry in details['picks_bans'] if entry['is_pick'] and entry['team'] == 1],
                        "bans_id_team_0": [entry["hero_id"] for entry in details['picks_bans'] if not entry['is_pick'] and entry['team'] == 0],
                        "bans_id_team_1": [entry["hero_id"] for entry in details['picks_bans'] if not entry['is_pick'] and entry['team'] == 1],
                        "league_id": details['leagueid'],
                        "version": details['version'],
                        "cluster": details['cluster'],
                        "lobby_type": details['lobby_type'],
                        "game_mode": details['game_mode']
                    }"""
                # Sauvegarde ligne par ligne
                json.dump(details, outfile)
                outfile.write('\n')
                print(f"✔ Match {matchId} sauvegardé.")
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur lors de la récupération des détails du match {matchId}: {e}")
                continue


def openJson(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def main():
    print("Début du programme")
    pathMathesId = r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeId10000Matchs.json"
    save_path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMatchsLigneParLigne_{datetime.now().date()}.json"

    matchesId = list(openJson(pathMathesId).values())
    df = pd.DataFrame(matchesId, columns=["match_id"])
    matchsId = df.head(1900)["match_id"]
    getMatchDetailsPro(matchsId, save_path)
    print(f"Sauvegarde terminée dans {save_path}")


if __name__ == '__main__':
    main()
