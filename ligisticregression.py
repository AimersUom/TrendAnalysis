# Data Manupulation
#pandas-Python Data Analysis Library; takes data for manipulation like csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
import seaborn as sns

sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

data = pd.read_csv('F:/4th year project/11.csv', sep=',')
data = data.dropna()


print(data.info())
print("my info 2")
print(data.shape)
print(list(data.columns))

print(data.head())
#Data exploration
print(data['y'].unique())
print(data['y'].value_counts())

sns.countplot(x='y', data=data, palette='hls')
#plt.show()
#plt.savefig('count_plot')

count_no_sub = len(data[data['y']==0])
count_sub = len(data[data['y']==1])
pct_of_no_sub = count_no_sub/(count_no_sub+count_sub)
print("percentage of not having impact", pct_of_no_sub*100)
pct_of_sub = count_sub/(count_no_sub+count_sub)
print("percentage of having impact", pct_of_sub*100)

print(data.groupby('y').mean())

#data_final=data.columns['Tech', 'Open', 'Cons', 'Extro', 'Agree', 'Neuro']

#Over-sampling using SMOTE

X = data.loc[:, data.columns != 'y']  # filter out the independent variables
y = data.loc[:, data.columns == 'y']  # filter out the dependent variables

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_sample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])

#Check the numbers of our data

print("length of oversampled data is ",len(os_data_X))
print("Number of low impact in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of high impact",len(os_data_y[os_data_y['y']==1]))
print("Proportion of high impact data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of low impact data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))

#Recursive Feature Elimination

data_final_vars=data.columns.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)

cols=['tfintopic','tfincontent', 'noOfarticlesinmonth','noOfpublishers','timeperiod']
X=os_data_X[cols]
y=os_data_y['y']

#Implementing the model

import statsmodels.api as sm

logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

#Logistic Regression Model Fitting

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

#Predicting the train set results and calculating the accuracy

y_predtr = logreg.predict(X_train)
print('Accuracy of logistic regression classifier on train set: {:.2f}'.format(logreg.score(X_train, y_train)))

#Confusion Matrix for train data

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_train, y_predtr)
print(confusion_matrix)

#Predicting the test set results and calculating the accuracy

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

#Confusion Matrix for test data

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

#Compute precision, recall, F-measure and support

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#ROC Curve

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()

plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()




