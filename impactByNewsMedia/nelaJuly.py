import pandas as pd     # To handle data
import numpy as np      # For number computing
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

#input
def svm_find(a,b,c,d,e):
    data = pd.read_csv("F:/4th year project/variables for svm.csv")


    X = data.drop('impact', axis=1)
    y = data['impact']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


    svclassifier = SVC(kernel='linear')
    svclassifier.fit(X_train, y_train)

    y_pred = svclassifier.predict(X_test)


    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))

    #trend to be tested
    trend=[a,b,c,d,e]

    result = svclassifier.predict([trend])
    ret=result[0]
    #Precision: When it predicts yes, how often is it correct?

    rslt=str(ret)
    msg="Impact of the Trend : "+rslt
    print (msg)
    f2 = open("result.txt", 'a')
    f2.write("result by svm :")
    f2.write(rslt)
    f2.close()
    return  rslt