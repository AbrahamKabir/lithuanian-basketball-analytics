from requests import get
from pprint import PrettyPrinter

# Base URL for the FIBA API (placeholder, update with the actual URL if available)
BASE_URL = "https://www.fiba.basketball/api"
# Example endpoint for fetching today's EuroBasket data
ALL_JSON = "/eurobasket/2025/today.json"

# Pretty printer for better readability of outputs
printer = PrettyPrinter()

def fetch_data(endpoint):
    """
    Fetch data from a given API endpoint.
    
    Args:
        endpoint (str): The API endpoint to fetch data from.

    Returns:
        dict: The JSON response as a Python dictionary.
    """
    try:
        # Builds the full URL by concatenating BASE_URL and endpoint
        response = get(BASE_URL + endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse the response JSON
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

def get_links():
    """
    Fetch the 'links' section from the 'today.json' endpoint.

    Returns:
        dict: A dictionary of available links, or an empty dictionary if data is unavailable.
    """
    data = fetch_data(ALL_JSON)
    if data:
        return data.get('links', {})  # Extract the 'links' section if present
    return {}

def get_scoreboard():
    """
    Fetch and print the current EuroBasket scoreboard.
    """
    links = get_links()  # Fetch available links from the API
    scoreboard_endpoint = links.get('currentScoreboard')  # Get the scoreboard endpoint URL

    if not scoreboard_endpoint:
        print("Error: Unable to find scoreboard endpoint.")
        return

    data = fetch_data(scoreboard_endpoint)  # Fetch scoreboard data
    if not data:
        return

    games = data.get('games', [])  # Extract the list of games
    for game in games:
        # Extract game details
        home_team = game['homeTeam']
        away_team = game['awayTeam']
        clock = game['clock']  # Remaining game time
        period = game['period']  # Current period

        # Print game details in a readable format
        print("------------------------------------------")
        print(f"{home_team['name']} vs {away_team['name']}")
        print(f"{home_team['score']} - {away_team['score']}")
        print(f"{clock} - Period {period['current']}")

def get_stats():
    """
    Fetches and print EuroBasket team statistics ranked by points per game (PPG).
    """
    links = get_links()  # Fetch available links from the API
    stats_endpoint = links.get('teamStatsLeaders')  # Get the team stats endpoint URL

    if not stats_endpoint:
        print("Error: Unable to find team stats endpoint.")
        return

    data = fetch_data(stats_endpoint)  # Fetch team stats data
    if not data:
        return

    # Navigate through the nested data structure to find teams
    teams = data.get('league', {}).get('standard', {}).get('regularSeason', {}).get('teams', [])

    # Filter out placeholder
    teams = list(filter(lambda x: x.get('name') != "Team", teams))

    # Sort teams by their rank in points per game (PPG)
    teams.sort(key=lambda x: int(x['ppg']['rank']))

    # Prints team ranking
    print("EuroBasket Team Rankings by Points Per Game:\n")
    for i, team in enumerate(teams):
        name = team.get('name', 'Unknown')  # Team name
        nickname = team.get('nickname', 'Unknown')  # Team nickname
        ppg = team.get('ppg', {}).get('avg', 'N/A')  # Average points per game
        print(f"{i + 1}. {name} - {nickname} - {ppg} PPG")

def main():
    """
    Main function to execute desired functionalities: fetching stats and scoreboard.
    """
    print("Fetching EuroBasket Team Stats:\n")
    get_stats()  # Fetch and display team stats

    print("\nFetching EuroBasket Scoreboard:\n")
    get_scoreboard()  # Fetch and display the scoreboard

# Entry point of the script
if __name__ == "__main__":
    main()
