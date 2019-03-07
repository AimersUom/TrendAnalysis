
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import Word
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
import codecs

# from stemming.porter2 import stem
stopwords = "prep/StopWords.txt"
stopwords = [l.strip() for l in codecs.open(stopwords, "r",encoding='utf-16', errors='ignore')]
suffixes = "prep/Suffixes-413.txt"
suffixes = [l.strip() for l in codecs.open(suffixes, "r",encoding='utf-8', errors='ignore')]
clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
vect = TfidfVectorizer(stop_words=stopwords, min_df=2)
print(stopwords)
print(vect)

def ModelTrainer():
    data = pd.read_csv('F:/4th year project/variables for svm.csv', encoding="utf8")
    # data.apply(lambda x: pd.lib.infer_dtype(x.values))
    x = data.drop('impact', axis=1).tolist()
    y = data['impact'].tolist()

    Y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(x, Y, test_size=0.20, random_state=42)

    X_train = vect.fit_transform(X_train)
    X_test = vect.transform(X_test)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    c_mat = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    print("Confusion Matrix:\n", c_mat)
    print("\nAccuracy: ", acc)


def ContentClassifier(content):
    x_new = ' '.join([Word(word).lemmatize() for word in content.split()])
    X_new = vect.transform([x_new])
    new_y = clf.predict(X_new)
    return new_y

# ModelTrainer()
# data = pd.read_csv('prep/test.csv', encoding='ISO-8859-1')
# news_article = data['News'].tolist()[100]
# print(ContentClassifier(news_article))

ModelTrainer()
test = [l.strip() for l in codecs.open('prep/test.txt', "r",encoding='utf-8', errors='ignore')]
for item in test:
    print(test)
    print(ContentClassifier(item))




