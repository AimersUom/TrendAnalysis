import tkinter
from tkinter import filedialog
from tkinter import *


# View start
root = Tk()
root.title("Sentiment Analysis of trend")
root.geometry("600x320")


# to label
scenario = Label(root, text = "Insert a keyword :", font = "verdana 14")
scenario.grid(row=3, padx=20, pady=(10,0))

# to input text
textBox = Text(root, height = 1, width = 30)
textBox.grid(row=4, padx=20, pady=(5, 10))
root.grid_columnconfigure(0, weight=1)

# input function
inputValue = ""
def retrieve_input():
    global x
    inputValue = textBox.get("1.0", "end-1c")
    #print(inputValue)
    x = inputValue
    return inputValue
# submit button
buttonCommit = Button(root,  bg = '#3e8ccc', foreground="white", font = "verdana 16 bold", text = "Submit", padx=40, pady=20, command = lambda: retrieve_input() )
buttonCommit.grid(row=6, padx=20, pady=(10,30))


mainloop()