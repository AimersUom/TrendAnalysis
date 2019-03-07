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



ps = PorterStemmer()

url_array = ['https://newsapi.org/v2/everything?domains=wsj.com,nytimes.com&from=2018-09-25&to=2017-09-25&apiKey=fe41b1f91be9425299ba345fe24170ee']

#for single_url in url_array:

URL = 'https://newsapi.org/v2/everything?sources=the-wall-street-journal&from=2018-12-04&to=2018-12-03&apiKey=acfd420b754d4d1c8c760a1c94d89fdd'

location = ""

PARAMS = {'address': location}

r = requests.get(url=URL, params= PARAMS)

data = r.json()
print(data)
news_array= data['articles']
print(news_array)
d = enchant.Dict("en_US")

for news_object in news_array:

    date_published = dateutil.parser.parse(news_object['publishedAt'])
    #print(dateutil.parser.parse(news_object['publishedAt']))

    publisher_name = news_object['source']['name']
    print(publisher_name)


    stemmed_word_set = " "
    stemmed_content_word_set = " "
    stemmed_description_word_set = " "

    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)
    tokenized_title = word_tokenize(news_object['title'])# there is another way to devide in to meaningful chunks called TreebankWordTokenizer
    print(news_object['content'])
    if (news_object['content']is not None):
        tokenized_content = word_tokenize(news_object['content'])
    else:
        tokenized_content= " ";
    tokenized_description = word_tokenize(news_object['description'])

    for word in tokenized_title:
        dictionary_word = str(TextBlob(word).correct())
        stemmed_word = ps.stem(dictionary_word)
        if stemmed_word not in stop_words:
            if stemmed_word not in punctuations:
                stemmed_word_set = stemmed_word_set + " " + stemmed_word


    for word in tokenized_content:
        dictionary_word_content = str(TextBlob(word).correct())
        stemmed_word_content = ps.stem(dictionary_word_content)
        if stemmed_word_content not in stop_words:
            if stemmed_word_content not in punctuations:
                stemmed_content_word_set = stemmed_content_word_set + " " + stemmed_word_content
                        #print(stemmed_word_set)

    for word in tokenized_description:
        dictionary_word = str(TextBlob(word).correct())
        stemmed_word = ps.stem(dictionary_word)
        if stemmed_word not in stop_words:
            if stemmed_word not in punctuations:
                stemmed_description_word_set = stemmed_word_set + " " + stemmed_word


    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "root",
        database= "trend_analysis"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO news_data (id,headline,date, publisher, content, description)"\
    " VALUES (%s, %s, %s, %s, %s,%s)"
    val = (0, stemmed_word_set, date_published,publisher_name,stemmed_content_word_set, stemmed_description_word_set)

    mycursor.execute(sql,val)

    mydb.commit()


#follwing is for retreive from db



















        #print(mycursor.rowcount, "record inserted")
  #dictionary_word = str(TextBlob(word).correct())
        #lemetized_word = Word(dictionary_word).lemmatize()
        #if lemetized_word not in stop_words:
            #if lemetized_word not in punctuations:
                #stemmed_word_set = stemmed_word_set + " " + lemetized_word