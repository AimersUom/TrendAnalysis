import codecs
import mysql.connector
import requests
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.corpus import stopwords
import string
from textblob import TextBlob
from textblob import Word
from datetime import datetime
import dateutil.parser
import enchant
import sys
import csv
import nltk
from nltk.stem import WordNetLemmatizer

csv.field_size_limit(sys.maxsize)
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

types_of_encoding = ["utf-8"]
stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)
d = enchant.Dict("en_US")

for encoding_type in types_of_encoding:
    with codecs.open('F:/4th year project/all-the-news (2)/article12017.csv',"r", encoding = "cp1252", errors ='replace') as csvFile:
        with open('F:/4th year project/all-the-news (2)/preprocessed2017new.csv', 'w',encoding = encoding_type) as filecsv:
            reader = csv.reader(csvFile)
            for row in reader:
                if ((row[2] != "" or row[2] is not None) or (row[8] != "" or row[8] is not None)):
                    oneRow=[]
                    aid = 0
                    id = 0
                    title = ""
                    publication = ""
                    author = ""
                    date = ""
                    year = ""
                    month = 0
                    content = ""
                    url = ""
                    if (row[0] is 'aid'):
                        continue
                    if (row[0] is not None and row[0] != ""):
                        aid= row[0]
                    if (row[1] is not None and row[1] != ""):
                        id = row[1]
                    if (row[7] is not None and row[7] != ""):
                        month = row[7]
                    if (row[5] is not None and row[5] != ""):
                        date = row[5]
                    if (row[6] is not None and row[6] != ""):
                        year = row[6]
                    if (row[4] is not None and row[4] != ""):
                        author = row[4]
                    if (row[3] is not None and row[3] != ""):
                        publication = row[3]
                    invalidChars = set(string.punctuation.replace("_", ""))
                    if (row[2] != "" or row[2] is not None):
                        tokenized_title = word_tokenize(row[2])
                        for word in tokenized_title:
                            if not(any(char in invalidChars for char in word)):
                            #dictionary_word = str(TextBlob(word).correct()) #this is for spelling correction if there is a spelling mistake
                                stemmed_word = ps.stem(word)
                                if word not in stop_words and d.check(word):
                                    if word not in punctuations:
                                        word_lowercase = word.lower()
                                        word_lematized= lemmatizer.lemmatize(word_lowercase, pos='v')
                                        title = title + " " + word_lematized

                    if (row[8] != "" or row[8] is not None):
                        tokenized_content = word_tokenize(row[8])
                        for word in tokenized_content:
                            if not(any(char in invalidChars for char in word)):
                                stemmed_word_content = ps.stem(word)
                                if word not in stop_words and d.check(word):
                                    if word not in punctuations:
                                        word_lowercase_content = word.lower()
                                        word_lematized_content = lemmatizer.lemmatize(word_lowercase_content, pos='v')
                                        content = content + " " + word_lematized_content
                    # dictionary_word = str(TextBlob(word).correct())
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="root",
                        database="trend_analysis"
                    )

                    mycursor = mydb.cursor()

                    sql = "INSERT INTO news2017(aid,id,title,publication,date,year,month,content)" \
                          " VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
                    val = (aid, id, title, publication,date,year,month,content)
                    print(aid, id, title, publication,date,year,month,content)
                    mycursor.execute(sql, val)

                    mydb.commit()
                    print("successfully inserted")

                    #print(oneRow)
                    #writer = csv.writer(filecsv)
                    #writer.writerow(oneRow)
                    #print("successfully inserted")
    filecsv.close()
    csvFile.close()
    print("end of insert")