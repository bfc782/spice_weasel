#import config
import os
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo
import time

client = pymongo.MongoClient("mongodb")
db = client.tweets

time.sleep(10)

api_key = os.getenv('TWITTER_CONSUMER_API_KEY')
api_secret = os.getenv('TWITTER_CONSUMER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

def authenticate():
    '''Function for handling Twitter Auth. Pulls Env Variables in bash_profile'''

    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):
        '''This method is what happens to every tweet as it is intercepted in real time'''

        t = json.loads(data)

        tweet = {
        'created_at': t['created_at'],
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'\n\n TWEET INCOMING: {tweet["text"]}\n\n')
        db.collections.tweets.insert_one(tweet)

    def on_error(self, status):

        if status -- 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['marathon'], languages=['en'])
