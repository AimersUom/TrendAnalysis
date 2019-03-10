import pandas as pd     # To handle data
import numpy as np      # For number computing
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

#input
bankdata = pd.read_csv("newdata.csv")


X = bankdata.drop('impact', axis=1)
y = bankdata['impact']

#Create SVM classification object
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)


print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))

#trend to be tested
trend=[201,20,6,-0.041,0,-0.998]

result = svclassifier.predict([trend])
ret=result[0]
#Precision: When it predicts yes, how often is it correct?

no=str(ret)
msg="Impact level of the Trend : "+no
print (msg)
if msg == 1 :
    msg1="Impact of the trend is high"
msg1="Impact of the trend is low"

f = open('Impact.txt','w')
f.write(msg)
f.write("\n")
f.write(msg1)
f.close()
