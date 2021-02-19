import requests, time, os, math, threading
from datetime import datetime, timedelta, timezone, time as dt_time
from dateutil import parser
from dotenv import load_dotenv
from team import Team
from image import build_image
from twitter import TwitterClient
from sms import SMSClient
from db import DatabaseConnector
from prediction import Prediction
from utils import headers

twitter_client = TwitterClient()
sms_client = SMSClient()
db_connector = DatabaseConnector()

load_dotenv()
dirname = os.path.dirname(__file__)
LEAGUE_ID = os.getenv("LEAGUE_ID")
LEAGUE_ID_PREV = os.getenv("LEAGUE_ID_PREV")

def get_utc_timestamp():
    return int(datetime.utcnow().timestamp())

def current_utc_day():
    return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) 

def seconds_to(time):
    return int((time - datetime.utcnow()).total_seconds())

def get_league_averages(league_results):
    home_goals, away_goals = 0.0, 0.0
    for result in league_results:
        home_goals += result['goalsHomeTeam']
        away_goals += result['goalsAwayTeam']

    return { 
        'home_goals': home_goals / len(league_results), 
        'away_goals': away_goals / len(league_results) 
    }

def get_results_for_league(league_id):
    results = requests.request(
        "GET", 
        "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}".format(league_id=league_id), 
        headers=headers
    ).json()['api']['fixtures']

    return results

def get_fixtures_by_day(league_id, day):
    route = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}/{date}".format(league_id=league_id, date=day)
    fixtures = requests.request(
        "GET", 
        route,
        headers=headers
    ).json()['api']['fixtures']

    return fixtures

def predict_goals(attack, defense, average):
    rel_atk = attack / average
    rel_def = defense / average
    return average * rel_atk * rel_def

def make_prediction(fixture):  
    home_team = Team(fixture['homeTeam']['team_id'], fixture['homeTeam']['team_name'], fixture['homeTeam']['logo'])
    away_team = Team(fixture['awayTeam']['team_id'], fixture['awayTeam']['team_name'], fixture['awayTeam']['logo'])

    home_goals = predict_goals(home_team.home_atk, away_team.away_def, league_averages['home_goals'])
    away_goals = predict_goals(away_team.away_atk, home_team.home_def, league_averages['away_goals'])

    pred_home_goals, home_poisson = expected_value(home_goals)
    pred_away_goals, away_poisson = expected_value(away_goals)

    kickoff = datetime.strptime(fixture['event_date'], "%Y-%m-%dT%H:%M:%S+00:00")

    db_connector.post_prediction_to_db(home_team, away_team, pred_home_goals, pred_away_goals, home_poisson, away_poisson, kickoff)

    return Prediction(home_team, away_team, pred_home_goals, pred_away_goals, home_poisson, away_poisson, kickoff)

def tweet_prediction(prediction):
    delay = (prediction.kickoff - timedelta(minutes=30) - datetime.utcnow()).total_seconds()
    time.sleep(max(delay, 0))
    build_image(prediction.home_team, prediction.away_team, prediction.home_poisson, prediction.away_poisson)
    media = twitter_client.upload_image(os.path.join(dirname, 'img/prediction.png'))
    twitter_client.tweet(prediction.to_tweet_string(), media)

def poisson(mu, x):
    return ((2.71828**(-1*mu))*(mu**x))/(math.factorial(x))

def expected_value(mu):
    poisson_list = []
    for i in range(0, 6):
        P = poisson(mu, i)
        poisson_list.append(P)
    return (poisson_list.index(max(poisson_list)), poisson_list)

today = datetime.utcnow().strftime("%Y-%m-%d")
league_results = get_results_for_league(LEAGUE_ID_PREV)
league_averages = get_league_averages(league_results)
fixtures = get_fixtures_by_day(LEAGUE_ID, today)

print(str(today))
predictions = []
for fixture in fixtures:
    predictions.append(make_prediction(fixture))

if len(predictions) > 0:
    sms = str(today) + ":"
    for prediction in predictions:
        prediction_sms = prediction.to_sms_string()
        sms += "\n" + prediction_sms
        print(prediction_sms)
    sms_client.broadcast_sms(sms)

    for prediction in predictions:
        tweet_prediction(prediction)
