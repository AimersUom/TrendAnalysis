import mysql.connector
import codecs
import csv
import numpy as np
from datetime import datetime

types_of_encoding = ["utf-8"]
for encoding_type in types_of_encoding:
    with codecs.open('F:/4th year project/all-the-news (2)/keywordsnew.csv',"r", encoding = encoding_type, errors ='replace') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            tfintopic= 0.0
            tfincontent = 0.0
            noOfpublishers = 0
            totalnoofarticles = 0
            datearray=[]
            maxdate=0
            mindate=0
            noOfarticles = 0
            sumOfFrequencyInTopic=0
            sumOfFrequencyInContent=0
            totalInTopic = 0
            totalInContent = 0
            impact=0
            publisherarray = []
            dategap = 0
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="trend_analysis"
            )

            mycursor = mydb.cursor()

            keywordid= row[0]
            mycursor.execute("SELECT * from analyzeddata WHERE keywordid="+keywordid+"")

            rows = mycursor.fetchall()
            totalnoofarticles= len(rows)
            for rowintable in rows:
                publisherarray.append(rowintable[6])
                datearray.append(rowintable[8])
            noOfpublishers = len(set(publisherarray))
            print(set(publisherarray))
            if(len(datearray)!= 0):
                maxdate= datetime.strptime(max(datearray),'%m/%d/%Y').date()
                mindate= datetime.strptime(min(datearray),'%m/%d/%Y').date()
                print(maxdate,mindate)
                dategap= (maxdate - mindate).days

            for rowintable in rows:
                noOfarticles = int(noOfarticles+1)
                sumOfFrequencyInTopic = sumOfFrequencyInTopic+rowintable[2]
                sumOfFrequencyInContent = sumOfFrequencyInContent+rowintable[4]
                totalInTopic = totalInTopic+rowintable[3]
                totalInContent = totalInContent+rowintable[5]
                impact =int(rowintable[10])
            if(totalInTopic !=0):
                tfintopic = float(sumOfFrequencyInTopic/totalInTopic)
            if(totalInContent != 0):
                tfincontent = float((sumOfFrequencyInContent/totalInContent)*100)
            print(keywordid, tfintopic, tfincontent, noOfpublishers, impact,noOfarticles,dategap)
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="trend_analysis"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO finalvariables (id,keyword,tfintopic, tfincontent, noOfpublishers, impact, noOfarticlesinmonth,timeperiod)" \
                  " VALUES (%s, %s, %s, %s, %s,%s, %s ,%s)"
            val = (0, keywordid, tfintopic, tfincontent, noOfpublishers, impact,noOfarticles,dategap)

            mycursor.execute(sql, val)

            mydb.commit()