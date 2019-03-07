import mysql.connector
from nltk.tokenize import word_tokenize
import codecs
import csv
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
#ps = PorterStemmer()
total_word_amount=0
tf_count_array_headline=[]
types_of_encoding = ["utf-8"]
for encoding_type in types_of_encoding:
    with codecs.open('F:/4th year project/all-the-news (2)/keywordsnew.csv',"r", encoding = encoding_type, errors ='replace') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            impact = row[3]
            print('csv has been read')
            countTerm = 0
            keywordid = row[0]
            tokenized_keyword = word_tokenize(row[1])
            #print(tokenized_keyword)
            total_word_amount = 0
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="trend_analysis"
            )

            mycursor = mydb.cursor()

            #sql = "SELECT headline from news_data "

            if (len(tokenized_keyword)==1):
                word_lowercase = tokenized_keyword[0].strip("\'").lower()
                word1 = lemmatizer.lemmatize(word_lowercase, pos='v')
                #word1= ps.stem(tokenized_keyword[0].strip("\'"))
                mycursor.execute("SELECT * from news2017 WHERE content like '%" + word1 +"%' ")
                print(word1)
            if (len(tokenized_keyword)==2):
                word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
                word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
                word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
                word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')

                print(word1,word2)
                mycursor.execute("SELECT * from news2017 WHERE content like '%" +word1 +"%' or content like '%" +word2+"%'")
            if (len(tokenized_keyword)==3):
                word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
                word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
                word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
                word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')
                word_lowercase3 = tokenized_keyword[2].strip("\'").lower()
                word3 = lemmatizer.lemmatize(word_lowercase3, pos='v')

                #word1= ps.stem(tokenized_keyword[0].strip("\'"))
                #word2= ps.stem(tokenized_keyword[1].strip("\'"))
                #word3= ps.stem(tokenized_keyword[2].strip("\'"))
                print(word1,word2,word3)
                mycursor.execute("SELECT * from news2017 WHERE content like '%" +word1 +"%' or content like '%" +word2+"%' or content like '%" +word3+"%'")
            if (len(tokenized_keyword)==4):
                word_lowercase1 = tokenized_keyword[0].strip("\'").lower()
                word1 = lemmatizer.lemmatize(word_lowercase1, pos='v')
                word_lowercase2 = tokenized_keyword[1].strip("\'").lower()
                word2 = lemmatizer.lemmatize(word_lowercase2, pos='v')
                word_lowercase3 = tokenized_keyword[2].strip("\'").lower()
                word3 = lemmatizer.lemmatize(word_lowercase3, pos='v')
                word_lowercase4 = tokenized_keyword[3].strip("\'").lower()
                word4 = lemmatizer.lemmatize(word_lowercase4, pos='v')

                #word1= ps.stem(tokenized_keyword[0].strip("\'"))
                #word2= ps.stem(tokenized_keyword[1].strip("\'"))
                #word3= ps.stem(tokenized_keyword[2].strip("\'"))
                #word4 = ps.stem(tokenized_keyword[3].strip("\'"))
                print(word1,word2,word3)
                mycursor.execute("SELECT * from news2017 WHERE content like '%" +word1 +"%' or content like '%" +word2+"%' or content like '%" +word3+"%' or content like '%" +word4+"%'")
            rows = mycursor.fetchall()

            print('sql hasbeen read')
                #tokenized_doc = word_tokenize(oneRow[0])
                #for word in tokenized_doc:
                    #total_word_amount = total_word_amount + 1
                #print(total_word_amount)

                #counting key word amount
                #key_word_list = ['trade','credit']
            keywordlength=0
            keywordlengthTitle=0
            countTerm=0
            countTermTitle=0
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
                    word_lowercase = k.lower()
                    word_lematized = lemmatizer.lemmatize(word_lowercase, pos='v')
                    #stemmed_word = ps.stem(k)
                    keywordfound = 0
                    keywordfoundinTitle = 0
                    for w in tokenized_doc:
                        if w == word_lematized:
                            countTerm = countTerm + 1
                            keywordfound = 1

                    if keywordfound == 1:
                        keywordlength = keywordlength+1
                    keywordfound = 0

                    for w in tokenized_title:
                        if w == word_lematized:
                            countTermTitle = countTermTitle + 1
                            keywordfoundinTitle= 1

                for word in tokenized_doc:
                    total_word_amount = total_word_amount + 1
                for word in tokenized_title:
                    total_word_amount_title = total_word_amount_title + 1
                #if keywordlength == len(tokenized_keyword):

                if keywordfoundinTitle==1 and keywordlength == len(tokenized_keyword) :
                #if keywordfoundinTitle == 1:
                    countTerm = countTerm/len(tokenized_keyword)
                    print(countTermTitle,keywordlength,len(tokenized_keyword))
                    print('ready to inssert')
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="root",
                        database="trend_analysis"
                    )

                    mycursor = mydb.cursor()
                    print(keywordid, countTermTitle, total_word_amount_title, countTerm,total_word_amount,publisher,month,date,articleid,impact)
                    sql = "INSERT INTO analyzeddata (id,keywordid,frequencyintopic, topicsize, frequencyincontent, contentsize, publisher,month,date,articleid,impact)" \
                          " VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
                    val = (0, keywordid, countTermTitle, total_word_amount_title, countTerm,total_word_amount,publisher,month,date,articleid,impact)

                    mycursor.execute(sql, val)

                    mydb.commit()
        #tf_value = countTerm/total_word_amount
