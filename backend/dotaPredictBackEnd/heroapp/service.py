import requests

# Retrieve raw data from Steam API
def fetch_opendota_heroes():
    api_url = "https://api.opendota.com/api/heroes"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()

# Clean all opendota API heroes to a list of Hero model
def get_parsed_heroes():
    raw_data = fetch_opendota_heroes()
    parsed_heroes = [parse_hero(h) for h in raw_data]
    return parsed_heroes

# Clean one hero from opendota API object to a Hero model
def parse_hero(hero_data):
    return {
        "hero_id": hero_data["id"],
        "name": hero_data["localized_name"]
    }