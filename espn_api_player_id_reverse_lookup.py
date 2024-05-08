import requests

def espn_api_player_id_reverse_lookup(player_name):
    TEAM_API = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
    response = requests.get(TEAM_API)

    if response.status_code == 200:
        teams_data = response.json()
        teams = teams_data["sports"][0]["leagues"][0]["teams"]

        roster = []

        # Iterate over each team
        for team in teams:
            team_id = team["team"]["id"]
            team_name = team["team"]["abbreviation"]

            # Fetch roster data for the team
            roster_url = f"{TEAM_API}/{team_id}?enable=roster"
            roster_response = requests.get(roster_url)

            if roster_response.status_code == 200:
                roster_data = roster_response.json()

                # Extract athlete information
                athletes = [
                    {
                        "id": athlete["id"],
                        "team": team_name,
                        "fullName": athlete["fullName"],
                    }
                    for athlete in roster_data["team"]["athletes"]
                ]

                # Add athlete information to the roster list
                roster.extend(athletes)

        # Search for player in the roster
        found_players = [
            {"id": player["id"], "team": player["team"]}
            for player in roster
            if player["fullName"].lower() == player_name.lower()
        ]

        if found_players:
            # Return the player ID instead of printing it
            return found_players[0]['id']  # Assuming only one player is found
        else:
            print("Player not found.")
            return None
    else:
        print("Failed to fetch NFL teams data.")
        return None










