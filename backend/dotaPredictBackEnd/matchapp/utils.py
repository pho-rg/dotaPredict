def extract_team_name(team_data):
    return team_data.get("team_name", "Unknown")

def extract_picks(picks):
    return [p.get("hero_id", 0) for p in picks] + [0] * (5 - len(picks))

def extract_bans(bans):
    return [b.get("hero_id", 0) for b in bans] + [0] * (7 - len(bans))

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

    return {
        "match_id": match_data["match_id"],
        "radiant_team": extract_team_name(match_data.get("radiant_team", {})),
        "dire_team": extract_team_name(match_data.get("dire_team", {})),
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
