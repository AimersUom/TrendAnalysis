from sklearn import preprocessing
import numpy as np
import mysql.connector
import codecs
import csv
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="trend_analysis"
            )
mycursor = mydb.cursor()

mycursor.execute("SELECT * from finalvariables")
rows = mycursor.fetchall()
topic_array=[]
content_array=[]
publisher_array=[]
articleamount_array=[]
timePeriod_array=[]


topic_array1=[]
content_array1=[]
publisher_array1=[]
articleamount_array1=[]
timePeriod_array1=[]


uselessarray=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
normalized = 0.0
for onerow in rows:
    topic_array.append(onerow[2])
    content_array.append(onerow[3])
    publisher_array.append(onerow[4])
    articleamount_array.append(onerow[6])
    timePeriod_array.append(onerow[7])

minmaxdifference1 = (max(topic_array) - min(topic_array))
for item in topic_array:
    normalized = item-min(topic_array)/minmaxdifference1

    topic_array1.append(normalized)
print(topic_array1)


minmaxdifference2 = (max(content_array) - min(content_array))
for item in content_array:
    normalized = item-min(content_array)/minmaxdifference2

    content_array1.append(normalized)
print(content_array1)

minmaxdifference3 = (max(publisher_array) - min(publisher_array))
for item in publisher_array:
    normalized = item -min(publisher_array)/minmaxdifference3

    publisher_array1.append(normalized)
print(publisher_array1)

minmaxdifference4 = (float(max(articleamount_array)) - float(min(articleamount_array)))
for item in articleamount_array:
    normalized_articles = float(item)-float(min(articleamount_array))/minmaxdifference4

    articleamount_array1.append(normalized)
print(articleamount_array1)

minmaxdifference5 = (max(timePeriod_array) - min(timePeriod_array))
for item in timePeriod_array:
    normalized = item-min(timePeriod_array)/minmaxdifference5

    timePeriod_array1.append(normalized)
print(timePeriod_array1)

for item in uselessarray:
    print(item)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="trend_analysis"
    )

    mycursor2 = mydb.cursor()


    #print(keywordid, countTermTitle, total_word_amount_title, countTerm,total_word_amount,publisher,month,date,articleid,impact)
    sql1 = "INSERT INTO normalizedfinalvariables (id,tfintopic,tfincontent,noOfpublishers, impact, noOfarticlesinmonth,timeperiod)" \
                  " VALUES (%s, %s, %s, %s, %s,%s, %s )"
    val1 = (0, topic_array1[item], content_array1[item], publisher_array1[item],rows[item][5],articleamount_array1[item],timePeriod_array1[item])
    #print(topic_array1[item], content_array1[item], publisher_array1[item],rows[item][5],articleamount_array1[item],timePeriod_array1[item])
    mycursor2.execute(sql1, val1)

    mydb.commit()