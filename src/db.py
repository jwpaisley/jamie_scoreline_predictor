import psycopg2, os, uuid
from datetime import datetime
from dotenv import load_dotenv

class DatabaseConnector:
    def __init__(self):
        load_dotenv()
        PGDATABASE = os.getenv("PG_DATABASE")
        PGHOST = os.getenv("PGHOST")
        PGPORT = os.getenv("PGPORT")
        PGUSER = os.getenv("PGUSER")
        PGPASSWORD = os.getenv("PGPASSWORD")

        self.conn = psycopg2.connect(database=PGDATABASE, user=PGUSER, password=PGPASSWORD, host=PGHOST, port=PGPORT)

    def post_prediction_to_db(self, home_team, away_team, pred_home_goals, pred_away_goals, home_poisson, away_poisson, kickoff):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO predictions 
            (id, home_team_id, home_team_name, home_team_logo_url, home_team_predicted_score, home_team_score_odds,
            away_team_id, away_team_name, away_team_logo_url, away_team_predicted_score, away_team_score_odds, kickoff_time, match_date) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, 
        (
            str(uuid.uuid4()), home_team.id, home_team.name, home_team.logo_url, pred_home_goals, home_poisson, 
            away_team.id, away_team.name, away_team.logo_url, pred_away_goals, away_poisson, kickoff.strftime(('%H:%M:%S')), kickoff.date()
        ))
        cursor.close()
        self.conn.commit()

