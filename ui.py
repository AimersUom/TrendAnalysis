from tkinter import *
import unicodedata

root = Tk()
textField = Text(root, height=10, width=50, pady=10)  # Creating the input Text field in the global level
inputText = ''  # declared input taken as a global field


class start_window(Frame):  # This  is written for creating the basic layout of the UI
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        Frame.pack(self)
        Label(self, text='Sinhala Grammar Checking System', font=('Comic Sans MS', 20), fg='blue',
              width=30).pack()  # Here defines the Topic
        Label(self, text='Enter your text here', fg="green", width=30).pack()  # and the Subtopic


if __name__ == '__main__':
    root.title("Sinhala Grammar Checking System")  # Define a name to the UI
    root.geometry("500x400")  # Define the size of the UI
    app = start_window(root)


def setLayout():  # This method is written for creating tthe complete layout of the UI
    vsb = Scrollbar(root, orient="vertical")
    vsb.place(in_=textField, relx=1.0, relheight=1.0, bordermode="outside")
    textField.configure(yscrollcommand=vsb.set)
    vsb.configure(command=textField.yview)
    textField.pack()

    button = Button(root, text='Search', fg="red", width=20,
                    command=getInput)  # Search Button bound with the getInput() method
    button.pack(padx=0, pady=10)


def getInput():  # Method for getitng the text from the Text Field
    rawText = textField.get("1.0", 'end-1c')  # get the text from the input text field
    refinedText = rawText.strip().replace("\n", " ").split(
        " ")  # remove spaces from either sides and remove the newlines as well and then add it to an arrry of words

    refinedText = [word for word in refinedText if (word != "")]  # remove empty spaces from the input

    inputText = refinedText
    processInput(inputText, rawText)  # call the method for processing input


def processInput(inputText, rawText):
    wordList = []  # A list of word with only pure characters
    removeList = ['0xdca', '0xdcf', '0xdd0', '0xdd1', '0xdd2', '0xdd3', '0xdd4', '0xdd6', '0xddc', '0xddd',
                  '0xddf']  # Here is the list to be removed
    for word in inputText:
        for letter in word:
            character = hex(ord(letter))  # Here get the unicode of each chracter
            if (hex(ord(letter)) in removeList):
                word = word.replace(letter, '')  # replace the word with no any of the above from the removeList
        wordList.append(word)
    followRules(wordList, rawText, inputText)


def followRules(wordList, rawText, inputText):
    errorWords = []
    ruleOneIgnoreList = ['කරනව',
                         'ඉරනව']  # these are the set of words that must be skipped for Rule 1 (Rule 1 not affectd)
    ruleTwoLetters = ['0xdb8', '0xdc4', '0xdb4', '0xdc0']
    wordIndex = 0
    for word in wordList:
        wordIndex += 1
        count = 0;
        for character in word:
            if (count + 1 != len(word)):
                if (hex(ord(character)) == '0xdbb'):  # Check Rule one
                    if (word in ruleOneIgnoreList):  # If in ruleOneIgnoreList then stop iteration for that word
                        continue

                    if (hex(ord(word[count + 1])) == '0xdb1'):  # if the next letter is න then dectect error
                        print(wordIndex)
                        errorWords.append(inputText[wordIndex - 1])
                        print('error1')

                elif (hex(ord(
                        character)) in ruleTwoLetters):  # check rule 2 if it is one of the characters from ruleTwoLetters
                    if (hex(ord(word[count + 1])) == '0xdb1'):  # if the next letter is න then dectect error
                        print(wordIndex)
                        errorWords.append(inputText[wordIndex - 1])
                        print('error2')

            count += 1
    print(errorWords)
    highlightInput(rawText, errorWords)


def highlightInput(rawText, errorWords):
    textField.delete('1.0', END)
    textField.insert(END, rawText)
    for word in errorWords:
        textField.tag_config(word, background='red')
        search(textField, word, word)


def search(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)


setLayout()

root.mainloop()
