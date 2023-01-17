# a script to load data from .json to mysql db

import pymysql.cursors
from glob import glob
import json, csv, os
from dotenv import load_dotenv

load_dotenv()

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=os.getenv('MYSQL_ROOT_PASS'),
                             database='twitter_accounts',
                             cursorclass=pymysql.cursors.DictCursor)

def json_to_db():
    with connection:
        with connection.cursor() as cursor:
            for c,i in enumerate(glob('%s/*.json' % os.getenv('37_K_USERS'))):
                print(c, i)
                data = json.loads(open(i, 'r').read())
                
                user = dict() 
                user['account_id'] = data['id_str']
                user['created_at'] = data['created_at']
                user['default_profile'] = data['default_profile']
                user['default_profile_image'] = data['default_profile_image']
                user['acct_description'] = data['description']
                user['favourites_count'] = data['favourites_count']
                user['followers_count'] = data['followers_count']
                user['friends_count'] = data['friends_count']
                user['geo_enabled'] = data['geo_enabled']
                user['lang'] = data['lang']
                user['acct_location'] = data['location']
                user['profile_background_image_url'] = data['profile_background_image_url']
                user['profile_image_url'] = data['profile_image_url']
                user['screen_name'] = data['screen_name']
                user['statuses_count'] = data['statuses_count']
                user['verified'] = data['verified']
                user['average_tweets_per_day'] = -1
                user['account_age_days'] = -1
                user['account_type'] =  None
                

                # Create a new record
                sql = "INSERT INTO `human_bots` (account_id,created_at,default_profile,default_profile_image,acct_description,favourites_count,followers_count,friends_count,geo_enabled,lang,acct_location,profile_background_image_url,profile_image_url,screen_name,statuses_count,verified,average_tweets_per_day,account_age_days,account_type)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql,(user['account_id'],user['created_at'],user['default_profile'],user['default_profile_image'],user['acct_description'],user['favourites_count'],user['followers_count'],user['friends_count'],user['geo_enabled'],user['lang'],user['acct_location'],user['profile_background_image_url'],user['profile_image_url'],user['screen_name'],user['statuses_count'],user['verified'],user['average_tweets_per_day'],user['account_age_days'],user['account_type']))
                except Exception as e:
                    print(e)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

def update_account_type():
    '''
    iterate over all 37k and update their type .i.e. human or bot in mysql
    '''
    with open('twitter_human_bots_dataset.csv') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        with connection:
            with connection.cursor() as cursor:
                for counter, row in enumerate(reader):
                    print(counter, row)
                    sql = 'update human_bots set account_type=%s where account_id=%s'
                    cursor.execute(sql, (row[1], row[0])) 
            connection.commit()
if __name__=="__main__":
    #json_to_db()
    update_account_type()

