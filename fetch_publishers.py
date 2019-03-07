import matplotlib.pyplot as plt
import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="trend_analysis"
            )

mycursor = mydb.cursor()
mycursor.execute("SELECT tfincontent from finalvariables ")
rows = mycursor.fetchall()


plt.hist(rows,30)
plt.show()