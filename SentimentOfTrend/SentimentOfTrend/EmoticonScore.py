import emoji
import regex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import mysql.connector
import re
#import keywords

def emoscore(key):
    analyser = SentimentIntensityAnalyzer()
    words=key

    sentiscorenew=[]
    for keyword in words:
        #print(keyword)

        param1='%'+keyword+'%'
        # open a database connection
        connection = mysql.connector.connect (host = "localhost", user = "root", passwd = "root1234", db = "trend_analysis")
        # prepare a cursor object using cursor() method
        cursor = connection.cursor ()
        # execute the SQL query using execute() method.
        cursor.execute("select * from senti_database where tweetText like %s",(param1,))
        # fetch all of the rows from the query
        data = cursor.fetchall ()

        num=0
        xo=0
        posentiscore = 0
        neusentiScore = 0
        negsentiscore = 0
        negtweetCount = 0
        neutweetCount = 0
        postweetCount = 0
        for row in data :
            if (row[2]!=""):
                line = [row[2]]
                #Extract the emojies from the text
                def split_count(text):
                    emoji_list = []
                    data = regex.findall(r'\X', text)
                    for word in data:
                        if any(char in emoji.UNICODE_EMOJI for char in word):
                            emoji_list.append(word)

                    return emoji_list

                counter = split_count(line[0])
                finalemoji = (' '.join(emoji for emoji in counter))
                #print(finalemoji)

                #Calculate the ovarall sentiment score of the emojies
                def sentiment_analyzer_scores(sentence):
                    score = analyser.polarity_scores(sentence)
                    emoticonScore= score['compound']
                    return emoticonScore

                sentiscore = sentiment_analyzer_scores(finalemoji)
                #print("tweet sentiment: ",sentiscore)

                if (sentiscore > 0):
                    posentiscore = posentiscore + sentiscore
                    postweetCount=postweetCount+1
                elif (sentiscore == 0):
                    neusentiScore = neusentiScore + sentiscore
                    neutweetCount=neutweetCount+1
                elif (sentiscore < 0):
                    negsentiscore = neusentiScore + sentiscore
                    negtweetCount=negtweetCount+1

            #-1 to +1 scale will be displayed
        totaltweetCount=postweetCount+negtweetCount+neutweetCount

        #calculate the overall emoticon sentiment score for each word in the list key
        if(totaltweetCount>0):
            overallnew=(posentiscore+neusentiScore+negsentiscore)/(postweetCount+neutweetCount+negtweetCount)
            overall=round(overallnew,4)
            sentiscorenew.append(overall)

        else:
            print("No Emoticons available.")
            overall=0

        #print(printAllEmoticons())
        print()
        # close the cursor object
        cursor.close ()
        # close the connection
        connection.close ()
        # exit the program

    items=len(sentiscorenew)

    overall2=0
    for score in sentiscorenew:
        overall2=overall2+score

    #calculate the overall Emoticon sentiment score of the trend
    if(totaltweetCount>0):
        overall2=(overall2/items)
        overall2=round(overall2,4)
        print("Overall Emoticon sentiment score of the Trend:",overall2)
    return overall2

