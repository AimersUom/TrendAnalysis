import mysql.connector
from nltk.tokenize import word_tokenize

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="trend_analysis"
)

mycursor = mydb.cursor()

sql = "SELECT content from news_data "

mycursor.execute(sql)

rows = mycursor.fetchall()

key_word_list = ['trade', 'street']
tf_count_array_content=[]
for row in rows:
    #print(row)
    #counting total words
    total_word_amount = 0
    for w in row:
        tokenized_doc = word_tokenize(w)
        for word in tokenized_doc:
            total_word_amount = total_word_amount + 1
        print(total_word_amount)

    #counting key word amount
    key_word_list = ['trade','credit']
    def countTerm(key_word_list, row):

        return
    countTerm = 0
    for k in key_word_list:
        for w in row:
            tokenized_para = word_tokenize(w)
            #print(tokenized_para)
            for one_word in tokenized_para:
                print(tokenized_para)
                if k == one_word:
                    countTerm = countTerm + 1
        print( countTerm)

    tf_value = countTerm/total_word_amount
    tf_count_array_content.append(tf_value)
    print(tf_count_array_content)