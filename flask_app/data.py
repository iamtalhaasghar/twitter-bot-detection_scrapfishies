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
from dotenv import load_dotenv

load_dotenv()

logger = get_logger('logs', 'data.log')


def get_user_features(user_id):
    '''
    Input: a Twitter handle (screen_name)
    Returns: a list of account-level information used to make a prediction 
            whether the user is a bot or not
    '''

    try:
        file_path = '%s/u_%s.json' % (os.getenv('37_K_USERS'), user_id)
        if os.path.exists(file_path):
            #logger.info(f'skipping {file_path}')
            return
        
        # Get user information from screen name
        user = api.get_user(user_id=user_id)
        json.dump(user._json, open(file_path, 'w'), indent=2)
        logger.info(f'saved {file_path}')
        return

    except Exception as e:
        if 'User has been suspended' in str(e) or 'User not found' in str(e):
            logger.warning((user_id, e))
        elif 'Rate limit exceeded' in str(e):
            logger.warning(e)
        else:
            logger.exception((user_id, e))

if __name__=="__main__":
    import csv, time
    with open('twitter_human_bots_dataset.csv') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for counter, row in enumerate(reader):
            #if counter % 10 == 0:
                #time.sleep(3)                
            get_user_features(row[0])
            
