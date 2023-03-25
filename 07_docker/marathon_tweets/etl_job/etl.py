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
time.sleep(10)

# Select the database within the MongoDB server
db = client.twitter

# Select the collection of docs within MongoDB server
collection = db.tweets

psw = os.getenv('POSTGRES_PASSWORD')

uri = f'postgresql://postgres:{psw}@postgresdb:5432/postgres'

pg = create_engine(uri, echo=True)

pg.execute('''
  CREATE TABLE IF NOT EXISTS tweets (
  mongo_id VARCHAR(100) primary key,
  stamp VARCHAR(150), 
  text VARCHAR(500),
  place varchar(200),
  followers NUMERIC, 
  sentiment NUMERIC
);
''')
while True:

  entries = collection.find()
  for e in entries:
    mongo_id = str(e['_id'])
    # qry_exist = f"""select mongo_id from tweets
    #  where mongo_id = {mongo_id};"""
    # try:
      # pg.execute(qry_exist)
      # pass
    # except:
    stamp = e['created_at']
    text = re.sub("[^\w\s]", "", e['text'])
    place = e['place']
    followers = e['followers_count']
    sentiment = s.polarity_scores(text)
    score = sentiment['compound']
    query = """INSERT INTO tweets 
    VALUES (%s, %s, %s, %s, %s, %s)
    on conflict do nothing;"""

    pg.execute(query, (mongo_id, stamp, text, place, followers, score))
  
  time.sleep(10)

 
