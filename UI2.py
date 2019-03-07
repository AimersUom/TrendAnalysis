from tkinter import *


def displayResult(result):
    root = Tk()

    # declared input taken as a global field

    class start_window(Frame): # This  is written for creating the basic layout of the UI
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            Frame.pack(self)
            Label(self, text = 'The social impact of the trend', font = ('TimesNewRoman',15), fg = 'blue', width=30).pack()# Here defines the Topic
            Label(self, text = result, font = ('FMBindumathi',10), fg="green", width=35).pack() # and the Subtopic


    if __name__ == '__main__':
        root.title("Results viewer")# Define a name to the UI
        root.geometry("500x300")# Define the size of the UI
        app = start_window(root)


    def setLayout(): # This method is written for creating the complete layout of the UI
        vsb = Scrollbar(root, orient="vertical")


    setLayout()




    root.mainloop()
