#import config
# %%
import os
from tweepy import OAuth1UserHandler, StreamingClient, Stream

import json
import logging
import pymongo
import time

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.twitter

time.sleep(10)

consumer_key = os.getenv('TWITTER_CONSUMER_API_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

def authenticate():
    '''Function for handling Twitter Auth. Pulls Env Variables in bash_profile'''

    auth = OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
        )

    return auth

class TwitterListener(Stream):

    def on_data(self, data):
        '''This method is what happens to every tweet as it is intercepted in real time'''

        t = json.loads(data)

        tweet = {
        'created_at': t['created_at'],
        'geo': t['geo'],
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'''\n\n 
        TWEET INCOMING: 
        {tweet["text"]} \n\n
        {tweet["geo"]}
        
        \n\n''')

        db.tweets.insert_one(dict(tweet))

    def on_error(self, status):

        if status -- 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()

    listener = TwitterListener(
        auth.consumer_key, auth.consumer_secret,
        auth.access_token, auth.access_token_secret
    )
    listener.filter(track=['commutif'], languages=['en'])

# %%
