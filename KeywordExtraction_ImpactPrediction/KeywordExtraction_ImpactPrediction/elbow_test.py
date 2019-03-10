
from pandas import DataFrame
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector
pd.set_option('mode.chained_assignment', None)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="mydatabase",
    charset='utf8mb4'
    )

mycursor = mydb.cursor()

#userinput
response1 = input("Please enter date 1: ")
response2 = input("Please enter date 2: ")

#print (response1)
date1=response1
date2=response2

pr1=date1+" "+"00:00:00"
pr2=date2+" "+"00:00:00"


#mycursor.execute("SELECT * from test where date between '2017-03-01 00:00:00' and '2017-03-20 00:00:00' ;")
mycursor.execute("SELECT * from test where date between %s and %s ",(pr1,pr2,))


df = DataFrame(mycursor.fetchall())

#select the text of the tweet
data= df[2]
documents = df[2].tolist()

criteria_row_indices = df[2].index
criteria_row_indices


vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)


#sum of squared error
sse={}
for k in range(1, 5):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X)

    #x axis
    data["clusters"] = kmeans.labels_
    #print(data["clusters"])

    #y axis
    sse[k] = kmeans.inertia_  #Sum of distances of samples to their closest cluster center
    #print(sse[k])

plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()
