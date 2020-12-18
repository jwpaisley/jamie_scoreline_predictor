from team import Team

class Prediction:
    def __init__(self, home_team, away_team, pred_home_goals, pred_away_goals, home_poisson, away_poisson):
        self.home_team = home_team
        self.away_team = away_team
        self.pred_home_goals = pred_home_goals
        self.pred_away_goals = pred_away_goals
        self.home_poisson = home_poisson
        self.away_poisson = away_poisson

    def to_tweet_string(self):
        return 'Prediction: {} {}, {} {} #{}{} #PremierLeague'.format(
            self.home_team.name, 
            self.pred_home_goals, 
            self.away_team.name, 
            self.pred_away_goals,
            Team.shorthand[self.home_team.name],
            Team.shorthand[self.away_team.name]
        )

    def to_sms_string(self):
        return '{} {}, {} {}'.format(
            self.home_team.name, 
            self.pred_home_goals, 
            self.away_team.name, 
            self.pred_away_goals,
            Team.shorthand[self.home_team.name],
            Team.shorthand[self.away_team.name]
        )
    