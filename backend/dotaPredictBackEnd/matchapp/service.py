import requests

import predictionapp.service as prediction_app_service

from django.conf import settings
from django.db import transaction

from .models import Match

# Update match table
# ended match must be flagged
# live matches must be updated (draft & status)
# changes must be saved
# this method can be both triggered by the controller (API endpoint) or a job (scheduled)
def updateLiveMatches():
    try:
        # avoid partial update retrieve in frontend
        with transaction.atomic():

            # get the list of live matches correctly structured, based on Match model
            parsed_matches = get_parsed_live_matches()
            # statistics
            created_count = 0
            updated_count = 0

            # set of pinned live matches
            live_matches_ids = set()

            for match_data in parsed_matches:
                # pin match as live
                live_matches_ids.add(match_data['match_id'])

                # create the live match, or update it if exist
                obj, created = Match.objects.update_or_create(
                    match_id=match_data["match_id"],
                    defaults={
                        "radiant_team": match_data["radiant_team"],
                        "dire_team": match_data["dire_team"],
                        "draft_in_progress": match_data["draft_in_progress"],
                        "match_status": match_data["match_status"],
                        "pro_match": match_data["pro_match"],

                        "radiant_win_chance": match_data["radiant_win_chance"],

                        "radiant_pick1": match_data["radiant_pick1"],
                        "radiant_pick2": match_data["radiant_pick2"],
                        "radiant_pick3": match_data["radiant_pick3"],
                        "radiant_pick4": match_data["radiant_pick4"],
                        "radiant_pick5": match_data["radiant_pick5"],

                        "dire_pick1": match_data["dire_pick1"],
                        "dire_pick2": match_data["dire_pick2"],
                        "dire_pick3": match_data["dire_pick3"],
                        "dire_pick4": match_data["dire_pick4"],
                        "dire_pick5": match_data["dire_pick5"],

                        "radiant_ban1": match_data["radiant_ban1"],
                        "radiant_ban2": match_data["radiant_ban2"],
                        "radiant_ban3": match_data["radiant_ban3"],
                        "radiant_ban4": match_data["radiant_ban4"],
                        "radiant_ban5": match_data["radiant_ban5"],
                        "radiant_ban6": match_data["radiant_ban6"],
                        "radiant_ban7": match_data["radiant_ban7"],

                        "dire_ban1": match_data["dire_ban1"],
                        "dire_ban2": match_data["dire_ban2"],
                        "dire_ban3": match_data["dire_ban3"],
                        "dire_ban4": match_data["dire_ban4"],
                        "dire_ban5": match_data["dire_ban5"],
                        "dire_ban6": match_data["dire_ban6"],
                        "dire_ban7": match_data["dire_ban7"],
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            # set as ended matches which haven't been updated (not in parsed_data -> not on live anymore)
            # store the value in ended count for statistics
            ended_count = Match.objects.exclude(match_id__in=live_matches_ids).update(
                draft_in_progress=False,
                match_status="match_ended"
            )


        return {
            "success": True,
            "created": created_count,
            "updated": updated_count,
            "ended": ended_count,
            "total": created_count + updated_count + ended_count
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Clean all Steam API live matches to a list of Match model
def get_parsed_live_matches():
    # get data from steam API
    raw_data = fetch_steam_live_league_games()
    # get matches structured as raw from steam
    matches = raw_data.get("result", {}).get("games", [])
    # transform raw matches data into Match model structure
    parsed_matches = [parse_match(m) for m in matches]
    # remove empty match
    return [m for m in parsed_matches if m is not None]

# Retrieve raw data from Steam API
def fetch_steam_live_league_games():
    api_key = getattr(settings, 'STEAM_API_KEY', None)
    if not api_key:
        raise ValueError("STEAM_API_KEY not configured")

    api_url = f"https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key={api_key}"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()

# Clean one match from Steam API raw object to a Match model
def parse_match(match_data):
    # Skip matches without scoreboard
    scoreboard = match_data.get("scoreboard")
    if not scoreboard:
        return None

    # retrieve raw dataa for each team
    radiant = scoreboard.get("radiant", {})
    dire = scoreboard.get("dire", {})

    # handle array of dictionnary
    radiant_picks_raw = radiant.get("picks", [])
    dire_picks_raw = dire.get("picks", [])
    radiant_bans_raw = radiant.get("bans", [])
    dire_bans_raw = dire.get("bans", [])

    # make the array of dictionnary an array of integer
    radiant_picks = extract_picks(radiant_picks_raw)
    dire_picks = extract_picks(dire_picks_raw)
    radiant_bans = extract_bans(radiant_bans_raw)
    dire_bans = extract_bans(dire_bans_raw)

    # define the status of the match based on the picks and bans of each team
    match_status = define_match_status(radiant_picks_raw, radiant_bans_raw, dire_picks_raw, dire_bans_raw)
    # define weither the draft is in progress or not
    draft_in_progress= is_draft_in_progress(dire_picks[4], radiant_picks[4])

    # set pro match to true
    pro_match = True

    # get the name of radiant team (pro match) or the name of the first radiant player (not a pro match)
    radiant_team_raw = match_data.get("radiant_team")
    if not radiant_team_raw:
        pro_match = False
        radiant_team = extract_player_name(match_data, 0)
    else:
        radiant_team = extract_team_name(radiant_team_raw)

    # get the name of dire team (pro match) or the name of the first dire player (not a pro match)
    dire_team_raw = match_data.get("dire_team")
    if not dire_team_raw:
        pro_match = False
        dire_team = extract_player_name(match_data, 1)
    else:
        dire_team = extract_team_name(dire_team_raw)

    hero_picks = [radiant_picks, dire_picks]
    default_model = prediction_app_service.get_default_model()
    default_model_id = default_model.get("id")

    if default_model and default_model_id:
        prediction = prediction_app_service.predict_match(hero_picks, int(default_model_id))
        radiant_win_chance = prediction.get("radiantWinChance", 0)
    else:
        radiant_win_chance = 0

    # structured data for one match
    return {
        "match_id": match_data["match_id"],
        "radiant_team": radiant_team,
        "dire_team": dire_team,
        "draft_in_progress": draft_in_progress,
        "match_status": match_status,
        "pro_match": pro_match,

        "radiant_win_chance": radiant_win_chance,

        "radiant_pick1": radiant_picks[0],
        "radiant_pick2": radiant_picks[1],
        "radiant_pick3": radiant_picks[2],
        "radiant_pick4": radiant_picks[3],
        "radiant_pick5": radiant_picks[4],

        "dire_pick1": dire_picks[0],
        "dire_pick2": dire_picks[1],
        "dire_pick3": dire_picks[2],
        "dire_pick4": dire_picks[3],
        "dire_pick5": dire_picks[4],

        "radiant_ban1": radiant_bans[0],
        "radiant_ban2": radiant_bans[1],
        "radiant_ban3": radiant_bans[2],
        "radiant_ban4": radiant_bans[3],
        "radiant_ban5": radiant_bans[4],
        "radiant_ban6": radiant_bans[5],
        "radiant_ban7": radiant_bans[6],

        "dire_ban1": dire_bans[0],
        "dire_ban2": dire_bans[1],
        "dire_ban3": dire_bans[2],
        "dire_ban4": dire_bans[3],
        "dire_ban5": dire_bans[4],
        "dire_ban6": dire_bans[5],
        "dire_ban7": dire_bans[6],
    }

# get the team name (pro match)
def extract_team_name(team_data):
    return team_data.get("team_name", "Unknown")

# get the name of the first player of a team (not a pro match)
# team_id define radiant or dire team
def extract_player_name(match_data, team_id):
    players = match_data.get("players", [])

    for player in players:
        # id 0 = radiant, id 1 = dire
        if player.get("team") == team_id:
            return player.get("name", "Unknown")
    return "Unknown"

# set the 5 picks - missing heroes are id 0 (draft in progress)
def extract_picks(picks):
    # for missing pick, set the id to 0
    return [p.get("hero_id", 0) for p in picks] + [0] * (5 - len(picks))

# set the 7 bans - missing heroes are id 0 (draft in progress)
def extract_bans(bans):
    # for missing ban, set the id to 0
    return [b.get("hero_id", 0) for b in bans] + [0] * (7 - len(bans))

# define weither the match is in draft in progress state or not
def is_draft_in_progress(direLastPick, radiantLastPick):
    if (radiantLastPick == 0 or direLastPick == 0):
        # at least one pick is missing to complete the draft
        return True
    else:
        # all the ten heroes have been picked
        return False

# define the match status based on picks and bans of each team
def define_match_status(radiant_picks, radiant_bans, dire_picks, dire_bans):
    if len(radiant_picks) == 0 and len(dire_picks) == 0 and len(radiant_bans) == 0 and len(dire_bans) == 0:
        # no heroes baned yet, no heroes picked yet
        return "draft_to_start"
    elif len(radiant_picks) == 5 and len(dire_picks) == 5:
        # all the ten heroes have been picked
        return "draft_finished"
    else:
        # bans or/and picks remaining
        return "draft_in_progress"

# group picks and bans into an array for a beautified json response
def transformMatchData(matchData):
    return {
        "match_id": matchData["match_id"],
        "createdAt": matchData["createdAt"],
        "radiant_team": matchData["radiant_team"],
        "dire_team": matchData["dire_team"],
        "draft_in_progress": matchData["draft_in_progress"],
        "match_status": matchData["match_status"],
        "pro_match": matchData["pro_match"],
        "radiant_win_chance": matchData["radiant_win_chance"],
        
        # regroup picks in arrays
        "radiant_picks": [
            matchData["radiant_pick1"],
            matchData["radiant_pick2"],
            matchData["radiant_pick3"],
            matchData["radiant_pick4"],
            matchData["radiant_pick5"]
        ],
        
        "dire_picks": [
            matchData["dire_pick1"],
            matchData["dire_pick2"],
            matchData["dire_pick3"],
            matchData["dire_pick4"],
            matchData["dire_pick5"]
        ],

        # regroup bans in arrays
        "radiant_bans": [
            matchData["radiant_ban1"],
            matchData["radiant_ban2"],
            matchData["radiant_ban3"],
            matchData["radiant_ban4"],
            matchData["radiant_ban5"],
            matchData["radiant_ban6"],
            matchData["radiant_ban7"]
        ],
        
        "dire_bans": [
            matchData["dire_ban1"],
            matchData["dire_ban2"],
            matchData["dire_ban3"],
            matchData["dire_ban4"],
            matchData["dire_ban5"],
            matchData["dire_ban6"],
            matchData["dire_ban7"]
        ]
    }