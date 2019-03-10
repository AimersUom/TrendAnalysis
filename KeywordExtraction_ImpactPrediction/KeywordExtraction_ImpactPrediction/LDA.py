import Input
import codecs
import mysql.connector

from nltk.tokenize import RegexpTokenizer
from pandas import DataFrame
import mysql.connector
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models
import gensim

#connect to the tweet database
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


mycursor.execute("SELECT * from test where date between %s and %s ",(pr1,pr2,))

doc=''

df = DataFrame(mycursor.fetchall())

docs_test = df[2].tolist()
docs = ' '.join(docs_test)
doc = doc + docs
doc_set = [doc]

tokenizer = RegexpTokenizer(r'\w+')
texts = []

# loop through document list
for i in doc_set:
    tokens = tokenizer.tokenize(i)

    # add tokens to list
    texts.append(tokens)

# turn tokenized document into a id,term dictionary
#create a dictionary
dictionary = corpora.Dictionary(texts)
#print(dictionary)

# convert tokenized document into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]


#Assign the k value obtained from elbow test
k=3

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=k, id2word=dictionary, passes=5)



for i, doc in enumerate(doc_set):
    print()
    print(" --Topics in document--")
    lda_result=ldamodel.print_topics(num_topics=k, num_words=3)
    print()

for oneitem in lda_result:
    print(oneitem)
