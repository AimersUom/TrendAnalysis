##This is the code to extract tweets from twitter
import tweepy
import unicodecsv as csv
import time
import datetime as dt
import json
import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

import mysql.connector
from nltk.sentiment.util import *


response = raw_input("Please enter Keyword: ")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="mydatabase",
    charset='utf8mb4'
    )

mycursor = mydb.cursor()

consumer_key = "DBN9eaAdzFlhiybQn5H3ak1Mt"
consumer_secret = "6WAcArbFBaJN8p52o8oweBjporIa7WPeKYWh9vBp2myZ2WoUDZ"
access_token = "1039918002593050624-wOarrQYmhGJ9ATWGlAhdYY7yNu1Idk"
access_token_secret = "FABH2na6c9QLqiBvNcw3FmPatZr1W2qpypzKUtyRXlZ0q"

# Creating the authentiction object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)


# Open/Create a file to append data
keyword = '$'+response
csvFile1 = open('dec1112.csv','wb')
fieldnames = ['date','text','username']

#Use csv Writer
csvWriter1 = csv.DictWriter(csvFile1,fieldnames=fieldnames)

'''for tweet in tweepy.Cursor(api.search,q=keyword ,
                           lang="en").items(max_tweets):
    print (tweet.created_at, tweet.text,tweet.id)'''

tweetCriteria = got.manager.TweetCriteria().setQuerySearch( keyword ).setSince( "2017-12-11" ).setUntil("2017-12-12" ).setMaxTweets(10)
csvWriter1.writeheader()

for tweet in got.manager.TweetManager.getTweets( tweetCriteria ):
    csvWriter1.writerow({'date':tweet.date,'text': tweet.text.encode( 'utf-8' ),'username':tweet.username})
    sql = "INSERT INTO march2 (date,text,username)" \
          " VALUES (%s, %s, %s)"
    val = (tweet.date, tweet.text.encode( 'utf-8' ),tweet.username)
    mycursor.execute(sql, val)
    mydb.commit()

