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

URL = 'https://api.nytimes.com/svc/archive/v1/2018/1.json?api-key=ylaJ8cjozbtBK5YxsuVACAxGvDtEKRRf'

location = ""

PARAMS = {'address': location}

r = requests.get(url=URL, params= PARAMS)

data = r.json()
#print(data)
nyt_array= data['response']['docs']
#print(nyt_array)
d = enchant.Dict("en_US")
news_array=[]
id=""
organization=""
original=""
firstname=""
middlename=""
lastname=""
personorganization=""
personQualifier=""
personRank=0
personRole=""
personTitle=""
documentType=""
headlineContentKicker=""
headlineKicker=""
headlineMain=""
headlineName=""
headlinePrintHeadline=""
headlineSeo=""
headlineSub=""
KeywordMajor=""
keywordName=""
keywordRank=0
keywordValue=""
multimediaCaption=""
multimediaCredit=""
multimediaCropname=""
multimediaheight=0
multimediaLegacyXlarge=0
multimediaLegacyXlargeheight=0
multimediaXlargeWidth=0
multimediaRank=0
multimediaSubtype=0
multimediaType=""
multimediaWidth=0
namedesk=""
printpage=""
pubDate=""
score=""
snippet=""
source=""
typeofmaterial=""
wordcount=0
for news_object in nyt_array:
    id=news_object['_id']
    organization= news_object['byline']['organization']
    original = news_object['byline']['original']
    firstname= news_object['byline']['person']['firstname']
    lastname= news_object['byline']['person']['lastname']
    middlename = news_object['byline']['person']['middlename']
    #personorganization= news_object['byline']['person']['organization']
    #personQualifier = news_object['byline']['person']['qualifier']
    #personRank = news_object['byline']['person']['rank']
    #personRole = news_object['byline']['person']['role']
    #personTitle = news_object['byline']['person']['title']
    documentType = news_object['document_type']
    headlineContentKicker = original = news_object['byline']['original']

    print(news_object['_id'])
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="trend_analysis"
    )


    mycursor = mydb.cursor()
    sql1="INSERT INTO nyt(id)"\
          " VALUES (%s)"
    sql= "INSERT INTO nyt (idnyt,id,bylineorganization,bylineoriginal, bylinepersonobjectfirstname, bylinepersonobjectlastname, bylinepersonobjectmiddlename," \
          "bylinepersonobjectorganization,bylinepersonobjectqualifier,bylinepersonobjectrank,bylinepersonobjectrole,bylinepersonobjecttitle,documenttype," \
          "headlinecontentKicker,headlinekicker,headlinemain,headlinename,headlineprintheadline," \
          "headlineseo,headlinesub,keywordobjectmajor,keywordobjectname,keywordobjectrank,keywordobjectvalue," \
          "multimediaobjectcaption,multimediaobjectcredit,multimediaobjectcropname,multimediaobjectheight,multimediaobjectlegacyxlarge," \
          "multimediaobjectlegacyxlargeheight,multimediaobjectlegacyxlargewidth,multimediaobjectrank,multimediaobjectsubtype," \
          "multimediaobjecttype,multimediaobjecturl,multimediaobjectwidth,newsdesk,printpage," \
          "pubdate,score,snippet,source,typeofmaterial,wordcount)" \
          " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (0,id," "," "," "," "," "," "," ",0," "," "," "," "," "," "," "," "," "," "," "," ",0," "," "," "," ",0," ",0,0,0," "," "," ",0," ",0," ",0," "," "," ",0)

    mycursor.execute(sql,val)

    mydb.commit()

#for news_object in news_array:


    #mydb = mysql.connector.connect(
        #host = "localhost",
       # user = "root",
      #  passwd = "root",
     #   database= "trend_analysis"
    #)

    #mycursor = mydb.cursor()

    #sql = "INSERT INTO news_data (id,headline,date, publisher, content, description)"\
    #" VALUES (%s, %s, %s, %s, %s,%s)"
    #val = (0, stemmed_word_set, date_published,publisher_name,stemmed_content_word_set, stemmed_description_word_set)

    #mycursor.execute(sql,val)

   # mydb.commit()












