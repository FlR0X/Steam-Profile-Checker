import argparse
import requests
import re

# Replace 'YOUR_API_KEY' with your actual Steam API key
API_KEY = 'YOUR_API_KEY'
STEAM_API_URL = 'https://api.steampowered.com/'

def fetch_steam_data(steam_id_or_url):
    # Determine if input is a URL or a Steam ID
    if re.match(r'^https?://steamcommunity.com/id/', steam_id_or_url):
        # Extract the SteamID from the URL
        response = requests.get(steam_id_or_url)
        if response.status_code != 200:
            print("Error: Unable to access the profile URL.")
            return

        html = response.text
        match = re.search(r'var g_steamID = "(.*?)";', html)
        if match:
            steam_id = match.group(1)
        else:
            print("Error: Unable to extract SteamID from the URL.")
            return
    else:
        steam_id = steam_id_or_url

    # Fetch player summaries
    player_summary_url = f'{STEAM_API_URL}ISteamUser/GetPlayerSummaries/v2/?key={API_KEY}&steamids={steam_id}'
    response = requests.get(player_summary_url)
    if response.status_code != 200:
        print("Error: Unable to fetch player data.")
        return

    player_data = response.json()
    if 'response' not in player_data or 'players' not in player_data['response'] or len(player_data['response']['players']) == 0:
        print("Error: No data found for the given SteamID.")
        return

    player = player_data['response']['players'][0]
    print(f"SteamID: {player['steamid']}")
    print(f"Persona Name: {player['personaname']}")
    print(f"Profile URL: {player['profileurl']}")
    print(f"Avatar URL: {player['avatar']}")
    print(f"Avatar Medium URL: {player['avatarmedium']}")
    print(f"Avatar Full URL: {player['avatarfull']}")
    print(f"Real Name: {player.get('realname', 'N/A')}")
    print(f"Location: {player.get('loccountrycode', 'N/A')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch data from Steam API.')
    parser.add_argument('input', type=str, help='SteamID or Steam Profile URL')
    args = parser.parse_args()
    fetch_steam_data(args.input)
