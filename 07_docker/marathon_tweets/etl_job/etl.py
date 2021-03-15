import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re
import logging

s = SentimentIntensityAnalyzer()

# Establish connection to MongoDB server
client = pymongo.MongoClient("mongodb")

# Give mongo a chance to open up
time.sleep(15)

# Select the database within the MongoDB server
db = client.tweets

# Select the collection of docs within MongoDB server
collection = db.collections.tweets

psw = os.getenv('POSTGRES_PASSWORD')

logging.critical(psw)

uri = f'postgres://postgres:{psw}@postgresdb:5432/postgres'

pg = create_engine(uri, echo=True)

pg.execute('''
  CREATE TABLE IF NOT EXISTS tweets (
  stamp VARCHAR(150), 
  text VARCHAR(500),
  followers NUMERIC, 
  sentiment NUMERIC
);
''')

entries = collection.find()
for e in entries:
  stamp = e['created_at']
  text = re.sub("[^\w\s]", "", e['text'])
  followers = e['followers_count']
  sentiment = s.polarity_scores(text)
  score = sentiment['compound']
  query = "INSERT INTO tweets VALUES (%s, %s, %s, %s, %s);"
  pg.execute(query, (stamp, text, followers, score))



 
