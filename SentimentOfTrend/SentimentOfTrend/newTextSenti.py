#calculate the overall sentiment score of text
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing
from textblob import TextBlob
import re
import string
from nltk.tokenize import word_tokenize
# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from nltk.corpus import stopwords

ttc=0
def textscore(key):

    negsentiScore = 0
    neusentiScore = 0
    possentiScore = 0
    negtweetCount = 0
    neutweetCount = 0
    postweetCount = 0
    totalWordcount= 0
    wordCount=[]
    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)
    words=key
    sentiscore=[]
    for keyword in words:
        #print(keyword)

        param1 = '%' + keyword + '%'
        # open a database connection
        # be sure to change the host IP address, username, password and database name to match your own
        connection = mysql.connector.connect(host="localhost", user="root", passwd="root1234", db="trend_analysis")
        # prepare a cursor object using cursor() method
        cursor = connection.cursor()
        # execute the SQL query using execute() method.
        cursor.execute("select * from senti_database where tweetText like %s", (param1,))
        # fetch all of the rows from the query
        data = cursor.fetchall()
        text33 = " "
        for row in data:
            # print(row[2])

            ha = row[2]

            #preprocess the tweet text
            def clean_tweet(tweet):
                pretext = ""
                invalidChars = set(string.punctuation.replace("_", ""))
                tokenized_title = word_tokenize(tweet)
                for word in tokenized_title:
                    if (not (any(char in invalidChars for char in word))):
                        if word not in stop_words:
                            if word not in punctuations:
                                pretext = pretext + " " + word
                xo = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", pretext).split())
                return xo



            #calculate the sentiment score of the text
            def analize_sentiment(tweet):
                analysis = TextBlob(clean_tweet(tweet))
                sentiScore = analysis.sentiment.polarity
                return sentiScore


            # print(analize_sentiment(ha))
            cleanTweet = clean_tweet(ha)
            tweetsentiScore = analize_sentiment(cleanTweet)
            tweetlength = len(cleanTweet.split())
            # print(tweetsentiScore)
            totalWordcount = totalWordcount + tweetlength
            wordCount.append(totalWordcount)
            if tweetsentiScore < 0:
                negsentiScore = negsentiScore + tweetsentiScore
                negtweetCount = negtweetCount + 1
                # print("negative")
            elif tweetsentiScore == 0:
                neusentiScore = neusentiScore + tweetsentiScore
                neutweetCount = neutweetCount + 1
                # print("neutral")
            elif tweetsentiScore > 0:
                possentiScore = possentiScore + tweetsentiScore
                postweetCount = postweetCount + 1
                # print("positive")


        def printAll():
            print("Total positive Text Sentiment Score: ", possentiScore)
            print("Total neutral Text Sentiment Score: ", neusentiScore)
            print("Total negative Text Sentiment Score: ", negsentiScore)
            print()

            print("Positive Tweet count: ", postweetCount)
            print("Neutral Tweet count: ", neutweetCount)
            print("Negative Tweet count: ", negtweetCount)
            print("Total word count: ", totalWordcount)
            print()
            return 'successful'


        totaltweetcount = postweetCount + negtweetCount + neutweetCount

        #calculate the overall text sentiment score for each word in the list key
        if (totaltweetcount > 0):
            overallnew = (possentiScore + neusentiScore + negsentiScore) / (totaltweetcount)
            overall = round(overallnew, 4)
            sentiscore.append(overall)
        else:
            print("No tweets available")
            overall = 0

        # print(printAll())
        print()
        # close the cursor object
        cursor.close()
        # close the connection
        connection.close()
        # exit the program


    countnew=0
    for count in wordCount:
        countnew=countnew+count

    global ttc
    ttc=countnew
    items=len(sentiscore)

    overall2=0
    for score in sentiscore:
        overall2=overall2+score

    # calculate the overall Text sentiment score of the trend
    if (totaltweetcount > 0):
        overall2=(overall2/items)
        overall2=round(overall2,4)
        print("Overall Text sentiment score of the Trend:", overall2)
    return overall2

