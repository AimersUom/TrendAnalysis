# Here TF-IDF is applied to a certain range of tweets and k means clustering is applied
from tkinter import *
import mysql.connector
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer



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


#mycursor.execute("SELECT * from test where date between '2017-05-15 00:00:00' and '2017-05-20 00:00:00' ;")
mycursor.execute("SELECT * from test where date between %s and %s ",(pr1,pr2,))


df = DataFrame(mycursor.fetchall())

#put the tuple to a list
docs_test = df[2].tolist()

#make it a string
docs=' '.join(docs_test)


cv = CountVectorizer(max_df=0.85, max_features=10000)
word_count_vector = cv.fit_transform(docs_test)

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)


feature_names = cv.get_feature_names()
tf_idf_vector = tfidf_transformer.transform(cv.transform([docs]))
#print(tf_idf_vector)


#sort the tf-idf vectors by descending order of scores
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

# use only topn items from vector
def extract_topn_from_vector(feature_names, sorted_items, topn=9):
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        #obtain feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])


    # results =(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results
    print(results)

# sort the tf-idf vectors by descending order of scores
sorted_items = sort_coo(tf_idf_vector.tocoo())

# extract only the top 10
keywords = extract_topn_from_vector(feature_names, sorted_items, 9)

print("\n===Keywords===")
for k in keywords:
    print(k, keywords[k])


#kmeans clustering

#vector
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(docs_test)

true_k = 3
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("\n Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()


for i in range(true_k):
    print("\n Cluster %d:" % i),

    for ind in order_centroids[i, :3]:
        print(' %s' % terms[ind]),
    print


# View start
root = Tk()
root.title("title")
root.geometry("600x300")

# upper label
scenario = Label(root, text = "Trends", font = "verdana 14")
scenario.grid(row=0,  padx=20, pady=10)

textBox = Text(root, height = 20, width = 40)
textBox.grid(row=1, column=0, padx=20, pady=10)
root.grid_columnconfigure(0, weight=1)

for i in range(true_k):
    #print("\n Cluster %d:" % i),
    textBox.insert(END, 'Cluster : %d \n' % i)

    for ind in order_centroids[i, :3]:
        #print(' %s' % terms[ind]),
        textBox.insert(END, 'Topic: %s \n' % terms[ind])
    print
#textBox.insert(END,'Trending topic : %s \n' % trendname)
#textBox.insert(END,'Sentiment level of the trend : %s \n' % xo)

mainloop()


