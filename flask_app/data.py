# Imports
import os
import numpy as np
import pandas as pd

import pickle
import tweepy
import json

from datetime import datetime,timezone
import re
import time

from utils import get_logger
from auth import api


logger = get_logger('logs', 'data.log')

# Get fully-trained XGBoostClassifier model
with open('model.pickle', 'rb') as read_file:
    xgb_model = pickle.load(read_file)

# Set up connection to Twitter API
#auth = tweepy.OAuthHandler(
#    twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
#auth.set_access_token(
#    twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

#api = tweepy.API(auth)


def get_user_features(user_id):
    '''
    Input: a Twitter handle (screen_name)
    Returns: a list of account-level information used to make a prediction 
            whether the user is a bot or not
    '''

    try:
        file_path = '/home/maira/user_data/37k/u_%s.json' % user_id
        if os.path.exists(file_path):
            #logger.info(f'skipping {file_path}')
            return
        
        data = api.rate_limit_status()
        limit = data['resources']['users']['/users/:id']
        logger.debug(limit)
        if limit['remaining'] == 1:
            secs = abs(time.time()-limit['reset'])+1
            logger.debug(f'sleeping for {secs} secs')
            time.sleep(secs)

        # Get user information from screen name
        user = api.get_user(user_id=user_id)
        json.dump(user._json, open(file_path, 'w'), indent=2)
        logger.info(f'saved {file_path}')
        return
        # account features to return for predicton
#        account_age_days = (datetime.now(timezone.utc) - user.created_at).days
#        verified = user.verified
#        geo_enabled = user.geo_enabled
#        default_profile = user.default_profile
#        default_profile_image = user.default_profile_image
#        favourites_count = user.favourites_count
#        followers_count = user.followers_count
#        friends_count = user.friends_count
#        statuses_count = user.statuses_count
#        average_tweets_per_day = np.round(statuses_count / account_age_days, 3)
#
#        # manufactured features
#        hour_created = int(user.created_at.strftime('%H'))
#        network = np.round(np.log(1 + friends_count)
#                           * np.log(1 + followers_count), 3)
#        tweet_to_followers = np.round(
#            np.log(1 + statuses_count) * np.log(1 + followers_count), 3)
#        follower_acq_rate = np.round(
#            np.log(1 + (followers_count / account_age_days)), 3)
#        friends_acq_rate = np.round(
#            np.log(1 + (friends_count / account_age_days)), 3)
#
#        # organizing list to be returned
#        account_features = [verified, hour_created, geo_enabled, default_profile, default_profile_image,
#                            favourites_count, followers_count, friends_count, statuses_count,
#                            average_tweets_per_day, network, tweet_to_followers, follower_acq_rate,
#                            friends_acq_rate]

    except Exception as e:
        if 'User has been suspended' in str(e) or 'User not found' in str(e):
            logger.warning((user_id, e))
        elif 'Rate limit exceeded' in str(e):
            logger.warning(e)
        else:
            logger.exception((user_id, e))


def bot_or_not(twitter_handle):
    '''
    Takes in a twitter handle and predicts whether or not the user is a bot
    Required: trained classification model (XGBoost) and user account-level info as features
    '''

    user_features = get_user_features(twitter_handle)

    if user_features == 'User not found':
        return 'User not found'

    else:
        # features for model
        features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
                    'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
                    'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']

        # creates df for model.predict() format
        user_df = pd.DataFrame(np.matrix(user_features), columns=features)

        prediction = xgb_model.predict(user_df)[0]

        return "Bot" if prediction == 1 else "Not a bot"


def bot_proba(twitter_handle):
    '''
    Takes in a twitter handle and provides probabily of whether or not the user is a bot
    Required: trained classification model (XGBoost) and user account-level info from get_user_features
    '''
    user_features = get_user_features(twitter_handle)

    if user_features == 'User not found':
        return 'User not found'
    else:
        user = np.matrix(user_features)
        proba = np.round(xgb_model.predict_proba(user)[:, 1][0]*100, 2)
        return proba

if __name__=="__main__":
    import csv, time
    with open('twitter_human_bots_dataset.csv') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for counter, row in enumerate(reader):
            #if counter % 10 == 0:
                #time.sleep(3)                
            get_user_features(row[0])
            
