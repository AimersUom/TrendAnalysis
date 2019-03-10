import codecs
import mysql.connector
import requests
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.corpus import stopwords
import string
from datetime import datetime
import dateutil.parser
import enchant
import sys
import csv
import re



csv.field_size_limit(sys.maxsize)
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

types_of_encoding = ["utf-8"]

stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)
for encoding_type in types_of_encoding:
    with codecs.open('janweek1.csv',"r", encoding = encoding_type, errors ='replace') as csvFile:
        with open('janweek1.csv', 'w',encoding = encoding_type, newline='') as filecsv:
            reader = csv.reader(csvFile)
            for row in reader:
                oneRow=[]
                id = ""
                username = ""
                date = ""
                text = ""

                if (row[0] is not None and row[0] != ""):
                    id = row[0]
                    oneRow.append(id)

                if (row[1] is 'date'):
                    continue
                if (row[1] is not None and row[1] != ""):
                    date = row[1]
                    oneRow.append(date)

                invalidChars = set(string.punctuation.replace("_", ""))

                if (row[2] != "" or row[2] is not None):
                    tokenized_title = word_tokenize(row[2])

                    for word in tokenized_title:
                        if (not (any(char in invalidChars for char in word))):
                            lemmed_word = lemmatizer.lemmatize(word)
                            if lemmed_word not in stop_words:
                                word = word.lower()

                                if (not (any(char in invalidChars for char in word))):

                                    if word not in stop_words:
                                        if word not in punctuations:
                                            if (len(word) != 1):
                                                text= re.sub(r'word',"",text)

                                            text = text + " " + word
                                            text = re.sub(r"http\S+", "", text)
                                            ptext = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",text).split())
                                            ptext = re.sub(r"newyork", "", ptext)


                oneRow.append(ptext)

                if (row[3] is not None and row[3] != ""):
                    username= row[3]
                    oneRow.append(username)

                print(oneRow)
                writer = csv.writer(filecsv)
                writer.writerow(oneRow)

                print("successfully inserted")
    filecsv.close()
    csvFile.close()
    print("end of insert")