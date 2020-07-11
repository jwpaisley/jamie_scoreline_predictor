import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterClient:
    def __init__(self):
        self.authenticate()

    def authenticate(self):
        API_KEY = os.getenv("TWITTER_API_KEY")
        API_KEY_SECRET = os.getenv("TWITTER_API_SECRET")
        TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
        TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        self.auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        self.auth.set_access_token(TOKEN, TOKEN_SECRET)
        self.api = tweepy.API(self.auth, wait_on_rate_limit = True)

    def tweet(self, message):
        self.api.update_status(message)

