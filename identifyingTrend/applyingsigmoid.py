import math
from nltk.tokenize import word_tokenize
import mysql.connector
from nltk.stem import PorterStemmer
import codecs
import csv
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from tkinter import *
from dbcalls import nelaJuly as svmFile

ps = PorterStemmer()


lemmatizer = WordNetLemmatizer()
keyword = "solar eclipse"
tokenized_keyword = word_tokenize(keyword)
keywordfoundincsv = 0

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="trend_analysis"
)

mycursor = mydb.cursor()

if (len(tokenized_keyword) == 1):
    word_lowercase = tokenized_keyword[0].strip("\'").lower()
    word1 = lemmatizer.lemmatize(word_lowercase, pos='v')
    # word1= ps.stem(tokenized_keyword[0].strip("\'"))
    mycursor.execute("SELECT * from news2017 WHERE content like '%" + word1 + "%' ")
    print(word1)
if (len(tokenized_keyword) == 2):
    word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
    word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
    word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
    word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')

    print(word1, word2)
    mycursor.execute("SELECT * from news2017 WHERE content like '%" + word1 + "%' or content like '%" + word2 + "%'")
if (len(tokenized_keyword) == 3):
    word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
    word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
    word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
    word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')
    word_lowercase3 = tokenized_keyword[2].strip("\'").lower()
    word3 = lemmatizer.lemmatize(word_lowercase3, pos='v')

    # word1= ps.stem(tokenized_keyword[0].strip("\'"))
    # word2= ps.stem(tokenized_keyword[1].strip("\'"))
    # word3= ps.stem(tokenized_keyword[2].strip("\'"))
    print(word1, word2, word3)
    mycursor.execute(
        "SELECT * from news2017 WHERE content like '%" + word1 + "%' or content like '%" + word2 + "%' or content like '%" + word3 + "%'")
if (len(tokenized_keyword) == 4):
    word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
    word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
    word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
    word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')
    word_lowercase3 = tokenized_keyword[2].strip("\'").lower()
    word3 = lemmatizer.lemmatize(word_lowercase3, pos='v')
    word_lowercase4 = tokenized_keyword[3].strip("\'").lower()
    word4 = lemmatizer.lemmatize(word_lowercase4, pos='v')

    # word1= ps.stem(tokenized_keyword[0].strip("\'"))
    # word2= ps.stem(tokenized_keyword[1].strip("\'"))
    # word3= ps.stem(tokenized_keyword[2].strip("\'"))
    # word4 = ps.stem(tokenized_keyword[3].strip("\'"))
    print(word1, word2, word3)
    mycursor.execute(
        "SELECT * from news2017 WHERE content like '%" + word1 + "%' or content like '%" + word2 + "%' or content like '%" + word3 + "%' or content like '%" + word4 + "%'")
rows = mycursor.fetchall()
array_to_write=[]
print('sql hasbeen read')

with open('temp.csv', 'w', encoding = "utf-8") as filecsv:

    writer = csv.writer(filecsv)

    for oneRow in rows:

        keywordlength = 0
        keywordlengthTitle = 0
        publisher = oneRow[3]
        month = oneRow[6]
        date = oneRow[4]
        articleid = oneRow[8]
        countTerm = 0
        countTermTitle = 0
        total_word_amount = 0
        total_word_amount_title = 0
        tokenized_doc = word_tokenize(oneRow[7])
        tokenized_title = word_tokenize(oneRow[2])
        for k in tokenized_keyword:

            word_lowercase = k.strip("\'").lower()
            onekeyword = lemmatizer.lemmatize(word_lowercase, pos='v')
            #stemmed_word = ps.stem(k)
            keywordfound = 0
            keywordfoundinTitle = 0
            for w in tokenized_doc:
                if w == onekeyword:
                    countTerm = countTerm + 1
                    keywordfound = 1

            if keywordfound == 1:
                keywordlength = keywordlength + 1
            keywordfound = 0

            for w in tokenized_title:
                if w == onekeyword:
                    countTermTitle = countTermTitle + 1
                    keywordfoundinTitle = 1

        for word in tokenized_doc:
            total_word_amount = total_word_amount + 1
        for word in tokenized_title:
            total_word_amount_title = total_word_amount_title + 1
        if keywordlength == len(tokenized_keyword):
            countTerm = countTerm / len(tokenized_keyword)
            print(countTermTitle, keywordlength, len(tokenized_keyword))
            print('ready to insert')
            array_to_write.append(countTermTitle)
            array_to_write.append(total_word_amount_title)
            array_to_write.append(countTerm)
            array_to_write.append(total_word_amount)
            array_to_write.append(publisher)
            array_to_write.append(month)
            array_to_write.append(date)
            array_to_write.append(articleid)

            writer.writerow(array_to_write)
            array_to_write = []
filecsv.close()

tfintopic = 0.0
tfincontent = 0.0
noOfpublishers = 0
totalnoofarticles = 0
datearray = []
maxdate = 0
mindate = 0
noOfarticles = 0
sumOfFrequencyInTopic = 0.0
sumOfFrequencyInContent = 0.0
totalInTopic = 0
totalInContent = 0
impact = 0
publisherarray = []
dategap = 0

with codecs.open('temp.csv', "r", encoding = "utf-8",errors = 'replace') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        if (len(row) < 1):
            continue
        publisher=row[4]
        publisherarray.append(publisher)
        datearray.append(row[6])
        noOfarticles = int(noOfarticles+1)
        sumOfFrequencyInTopic = sumOfFrequencyInTopic+float(row[0])
        sumOfFrequencyInContent = sumOfFrequencyInContent+float(row[2])
        totalInTopic = totalInTopic+int(row[1])
        totalInContent = totalInContent+int(row[3])
    if(totalInTopic !=0):
        tfintopic = float(sumOfFrequencyInTopic/totalInTopic)
    if(totalInContent != 0):
        tfincontent = float((sumOfFrequencyInContent/totalInContent)*100)

    noOfpublishers = len(set(publisherarray))
    print(set(publisherarray))
    if (len(datearray) != 0):
        maxdate = datetime.strptime(max(datearray), '%m/%d/%Y').date()
        mindate = datetime.strptime(min(datearray), '%m/%d/%Y').date()
        print(maxdate, mindate)
        dategap = (maxdate - mindate).days
print(tfintopic, tfincontent, noOfpublishers,noOfarticles,dategap)

s= 0.0
y = (9.8021* tfintopic) + (4.8531 * tfincontent) + (0.4857* noOfpublishers) + (0.0001 * noOfarticles) + (-0.0502 * dategap)
s = 1 / (1 + math.exp(-y))
print("y= "+str(y))
print("sigmoid value="+str(s))
trend_impact= ""

if s > 0.7:
   print('high impact')
   trend_impact= "high"
   f = open("result.txt", 'a')
   f.write(keyword)
   f.write("\nhigh impact\n")
   f.close()

else:
    f2= open("result.txt", 'a')
    f2.write(keyword)
    f2.write( "\nlow impact\n")
    f2.close()
    print('low impact')
    trend_impact = "low"
#result=svmFile.svm_find(tfintopic,tfincontent,noOfpublishers,noOfarticles,dategap)
csvFile.close()

def displayResult(result):
    root = Tk()
    # declared input taken as a global field

    class start_window(Frame): # This  is written for creating the basic layout of the UI
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            Frame.pack(self)
            Label(self, text = 'The social impact of the trend is:', font = ('TimesNewRoman',15), fg = 'blue', width=30).pack()# Here defines the Topic
            Label(self, text = result, font = ('FMBindumathi',10), fg="green", width=35).pack() # and the Subtopic

    if __name__ == '__main__':
        root.title("Results viewer")# Define a name to the UI
        root.geometry("200x200")# Define the size of the UI
        app = start_window(root)

    def setLayout(): # This method is written for creating the complete layout of the UI
        vsb = Scrollbar(root, orient="vertical")

    setLayout()
    root.mainloop()
#if result==1:
    #resultInWord="high"
#else:
    resultInWord= "low"
displayResult(trend_impact)