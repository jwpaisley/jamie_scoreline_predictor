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

    def upload_image(self, file):
        media = self.api.media_upload(file)
        return media

    def tweet(self, message, media=None):
        if media: self.api.update_status(message, media_ids=[media.media_id])
        else: self.api.update_status(message)
