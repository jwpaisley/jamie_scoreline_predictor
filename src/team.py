import requests
import collections
import os
from dotenv import load_dotenv
from utils import headers

load_dotenv()
FIXTURES = os.getenv("FIXTURES")
FORM_MATCHES = int(os.getenv("FORM_MATCHES"))
FORM_WEIGHT = int(os.getenv("FORM_WEIGHT"))

class Team:
    premier_league_shorthand = {
        "Arsenal": "ARS",
        "Aston Villa": "AVL",
        "Brighton": "BHA",
        "Burnley": "BUR",
        "Chelsea": "CHE",
        "Crystal Palace": "CPL",
        "Everton": "EVE",
        "Fulham": "FUL",
        "Leeds": "LEE",
        "Leicester": "LEI",
        "Liverpool": "LIV",
        "Manchester City": "MCI",
        "Manchester United": "MUN",
        "Newcastle": "NEW",
        "Sheffield Utd": "SHU",
        "Southampton": "SOU",
        "Tottenham": "TOT",
        "West Brom": "WBA",
        "West Ham": "WHU",
        "Wolves": "WOL"
    }

    shorthand = collections.defaultdict(list, premier_league_shorthand)

    def __init__(self, id, name, logo_url):
        self.id = id
        self.name = name
        self.logo_url = logo_url
        self.get_recent_fixtures()
        self.calc_atk()
        self.calc_def()

    def get_recent_fixtures(self):
        route = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/{team_id}/last/{fixtures}".format(team_id=self.id, fixtures=FIXTURES)
        fixtures = requests.request(
            "GET", 
            route, 
            headers=headers
        ).json()['api']['fixtures']
        self.recent_fixtures = fixtures

    def calc_atk(self):
        home_goals, away_goals = 0.0, 0.0
        home_games, away_games = 0, 0
        for idx, fixture in enumerate(self.recent_fixtures):
            if fixture['status'] == 'Match Finished':
                if fixture['homeTeam']['team_id'] == self.id:
                    home_games += FORM_WEIGHT if idx < FORM_MATCHES else 1
                    home_goals += fixture['goalsHomeTeam'] * FORM_WEIGHT if idx < FORM_MATCHES else fixture['goalsHomeTeam']
                else:
                    away_games += FORM_WEIGHT if idx < FORM_MATCHES else 1
                    away_goals += fixture['goalsAwayTeam'] * FORM_WEIGHT if idx < FORM_MATCHES else fixture['goalsAwayTeam']

        self.home_atk = home_goals / home_games
        self.away_atk = away_goals / away_games

    def calc_def(self):
        home_goals, away_goals = 0.0, 0.0
        home_games, away_games = 0, 0
        for idx, fixture in enumerate(self.recent_fixtures):
            if fixture['status'] == 'Match Finished':
                if fixture['homeTeam']['team_id'] == self.id:
                    away_games += FORM_WEIGHT if idx < FORM_MATCHES else 1
                    away_goals += fixture['goalsAwayTeam'] * FORM_WEIGHT if idx < FORM_MATCHES else fixture['goalsAwayTeam']
                else:
                    home_games += FORM_WEIGHT if idx < FORM_MATCHES else 1
                    home_goals += fixture['goalsHomeTeam'] * FORM_WEIGHT if idx < FORM_MATCHES else fixture['goalsHomeTeam']
                
        self.home_def = home_goals / home_games
        self.away_def = away_goals / away_games
        
