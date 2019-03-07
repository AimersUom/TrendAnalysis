
import mysql.connector
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import mysql.connector

#connect to the tweet database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="trend_analysis"
)

mycursor = mydb.cursor()



#mycursor.execute("SELECT * from test where date between '2017-05-15 00:00:00' and '2017-05-20 00:00:00' ;")
mycursor.execute("SELECT * from news2017 ")


df = DataFrame(mycursor.fetchall())

#put the tuble to a list
docs_test = df[2].tolist()

#make it a string
docs=' '.join(docs_test)


cv = CountVectorizer(max_df=0.85, max_features=10000)
word_count_vector = cv.fit_transform(docs_test)

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)

#generate tf-idf vecot for k means
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(docs_test)

feature_names = cv.get_feature_names()
tf_idf_vector = tfidf_transformer.transform(cv.transform([docs]))
print(tf_idf_vector)

#sort the tf-idf vectors by descending order of scores
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=9):
    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results
    print(results)

# sort the tf-idf vectors by descending order of scores
sorted_items = sort_coo(tf_idf_vector.tocoo())

# extract only the top n; n here is 10
keywords = extract_topn_from_vector(feature_names, sorted_items, 250)

# now print the results
print("\n=====Doc=====")
###print(doc)
print("\n===Keywords===")
for k in keywords:
    print(k, keywords[k])

##################################################kmeans clustering


true_k = 45
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("\n Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()


for i in range(true_k):
    print("\n Cluster %d:" % i),
    #print('%s' % label[ind])
    for ind in order_centroids[i, :3]:
        print(' %s' % terms[ind]),
    print





