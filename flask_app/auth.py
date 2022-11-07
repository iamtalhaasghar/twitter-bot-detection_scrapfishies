# Import the necessary Libraries

from dotenv import load_dotenv
import os
import tweepy

load_dotenv()
access_token = os.getenv('API_KEY')
access_token_scret = os.getenv('API_SECRET_KEY')
bearer_token = os.getenv('BEARER_TOKEN')

auth_bear = tweepy.OAuth2BearerHandler(bearer_token)
#auth_consume = tweepy.OAuth2AppHandler(access_token, access_token_scret)
api = tweepy.API(auth_bear, wait_on_rate_limit=True)

