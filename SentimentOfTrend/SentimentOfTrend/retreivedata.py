import emoji
import regex
import sys
import mysql.connector
import re

def retrievedata(key):
    word=key
    imgcount=[]
    emojicountnew=[]
    for keyword in word:
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
        xo=0

        #IMAGE count
        num=0
        xo=0
        for row in data :
            if (row[3]!='no'):
                num=num+1
            else:
                xo=0
        #print("image count: ",num)
        imagecount=num
        imgcount.append(imagecount)


        def split_count(text):

            emoji_list = []
            data = regex.findall(r'\X', text)
            for word in data:
                if any(char in emoji.UNICODE_EMOJI for char in word):
                    emoji_list.append(word)
            return emoji_list

        #EMOJI count
        txt=0
        emojicount=0
        for row in data :
            line = [row[2]]

            counter = split_count(line[0])
            finalemoji = (' '.join(emoji for emoji in counter))
            if (finalemoji == ""):
                txt=0
            else:
                emojicount=emojicount+1

        #print("Emoji count: ",emojicount)
        emojicountnew.append(emojicount)
        #print(emojicountnew)
        # close the cursor object
        cursor.close ()
        # close the connection
        connection.close ()

    imagecountnew=0
    for k in imgcount:
        imagecountnew=imagecountnew+k

    emojicnt=0
    for h in emojicountnew:
        emojicnt=emojicnt+h

    #print(imagecountnew,emojicnt)
    return imagecountnew,emojicnt

