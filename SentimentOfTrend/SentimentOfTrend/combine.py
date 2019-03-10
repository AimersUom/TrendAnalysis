#import interface for enter a keyword
import inputfile

#set of kewords can be appended to the list key
key=[]
keyword=inputfile.keywordnew
key.append(keyword)
print(key)

#import image,text and emoticon sentiment analysis files
import label_image
import newTextSenti
import EmoticonScore

#Get the image and emoticon counts
import retreivedata


textSenti=newTextSenti.textscore(key)
noOfwords=newTextSenti.ttc
print(noOfwords)
emoSenti=EmoticonScore.emoscore(key)
imgSenti=label_image.imagescore(key)
redata1,redata2=retreivedata.retrievedata(key)

#Assign the sentiment level according to the sentiment score
def sentimentlevelOfTrend (sentiScore):
    if (sentiScore > 0.05):
        sentiLevel = "Positive"
    elif(sentiScore > -0.05) and (sentiScore < 0.05):
        sentiLevel = "Neutral"
    elif (sentiScore < -0.05):
        sentiLevel="Negative"

    return sentiLevel

#find the overall sentiment score of the trend
def overallSentimentOfTrend (textSentiment, emoticonSentiment,imageSentiment):
    overallsenti = (0.37 * textSentiment + 0.29 * emoticonSentiment + 0.34 * imageSentiment)
    overallSentimentScore = round(overallsenti,2)

    print("Overall Sentiment Score of the trend:",overallSentimentScore)

    overallSentiment= sentimentlevelOfTrend(overallSentimentScore)

    return overallSentiment

print()
print("----------------------------------------------")
xo=overallSentimentOfTrend(textSenti,emoSenti,imgSenti)
print("Sentiment Level of the trend : ",xo)


trendname=key[0]

from tkinter import *
# View start
root = Tk()
root.title("Sentiment Analysis of trend")
root.geometry("600x300")

# upper label
scenario = Label(root, text = "Output Display", font = "verdana 14")
scenario.grid(row=0,  padx=20, pady=10)

textBox = Text(root, height = 10, width = 40)
textBox.grid(row=1, column=0, padx=20, pady=10)
root.grid_columnconfigure(0, weight=1)
textBox.insert(END,'Trending topic : %s \n' % trendname)
textBox.insert(END,'Sentiment level of the trend : %s \n' % xo)

mainloop()

#send features of trend to SVM for the predictions

download_dir = "/Users/kaumadisamarathunga/Documents/test3.csv"

csv = open(download_dir, "w")

col="txtcount,emocount,imgcount,textsenti,emosenti,imgsenti\n"
csv.write(col)
reslt=str(noOfwords)+","+str(redata2)+","+str(redata1)+","+str(textSenti)+","+str(emoSenti)+","+str(imgSenti)
csv.write(reslt)



