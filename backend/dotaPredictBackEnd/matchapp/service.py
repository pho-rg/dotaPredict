import requests

from django.conf import settings

# Retrieve raw data from Steam API
def fetch_steam_live_league_games():
    api_key = getattr(settings, 'STEAM_API_KEY', None)
    if not api_key:
        raise ValueError("STEAM_API_KEY not configured")
    api_url = f"https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key={api_key}"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()

# Clean all Steam API live matches to a list of Match model
def get_parsed_live_matches():
    raw_data = fetch_steam_live_league_games()
    matches = raw_data.get("result", {}).get("games", [])
    parsed_matches = [parse_match(m) for m in matches]
    return [m for m in parsed_matches if m is not None]

# Clean one match from Steam API object to a Match model
def parse_match(match_data):
    try:
        scoreboard = match_data["scoreboard"]
    except KeyError:
        return None  # Skip matches without scoreboard

    radiant = scoreboard.get("radiant", {})
    dire = scoreboard.get("dire", {})

    radiant_picks = extract_picks(radiant.get("picks", []))
    dire_picks = extract_picks(dire.get("picks", []))
    radiant_bans = extract_bans(radiant.get("bans", []))
    dire_bans = extract_bans(dire.get("bans", []))
    # Based on the captain mode where the last pick is the fifth for dire team
    draft_in_progress= is_draft_in_progress(dire_picks[4])

    return {
        "match_id": match_data["match_id"],
        "radiant_team": extract_team_name(match_data.get("radiant_team", {})),
        "dire_team": extract_team_name(match_data.get("dire_team", {})),
        "draft_in_progress": draft_in_progress,
        "radiant_win_chance": 0,
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

def extract_team_name(team_data):
    return team_data.get("team_name", "Unknown")

def extract_picks(picks):
    return [p.get("hero_id", 0) for p in picks] + [0] * (5 - len(picks))

def extract_bans(bans):
    return [b.get("hero_id", 0) for b in bans] + [0] * (7 - len(bans))

def is_draft_in_progress(lastpick):
    if (lastpick == 0):
        return True
    else:
        return False