from tkinter import *
class MainGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.setupGUI()
    def setupGUI(self):
        for row in range(5): #setup the rows and columns
            Grid.rowconfigure(self, row, weight=1)
        for col in range(1):
            Grid.columnconfigure(self, col, weight=1)
        self.pack(fill=BOTH, expand=1)
        self.button1 = Button(self, anchor=N, text="Translate", bg="grey", font=("TexGyreAdventor", 45))
        self.button1.grid(row=0, column=3, sticky=E+W+N+S)
        self.button2 = Button(self, anchor=N, text="Translate", bg="grey", font=("TexGyreAdventor", 45))
        self.button2.grid(row=0, column=6, sticky=E+W+N+S)
        self.uiw1 = Entry(self, bg="white", font=("TexGyreAdventor", 45))
        self.uiw1.grid(row=0, column=0, columnspan=2, sticky=E+W+N+S)
        self.uiw2 = Entry(self, bg="white", font=("TexGyreAdventor", 45))
        self.uiw2.grid(row=0, column=4, columnspan=2, sticky=E+W+N+S)

window = Tk()
p = MainGUI(window)
window.mainloop()