#settings
FULLSCREEN = True
DEBUG = False


from tkinter import *
class MainGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        if FULLSCREEN:
            parent.attributes("-fullscreen", True)
        self.setupGUI()
    def setupGUI(self):
        for row in range(9): #setup the rows and columns
            Grid.rowconfigure(self, row, weight=1)
        for col in range(7):
            Grid.columnconfigure(self, col, weight=1)
        self.pack(fill=BOTH, expand=1)

        #exit button
        self.eb = Button(self, anchor=N, text="X", bg="red", font=("TexGyreAdventor", 45))
        self.eb.grid(row=0, column=9, sticky=E+W+N+S)
        #translate button
        self.tb = Button(self, anchor=N, text="Translate", bg="grey", font=("TexGyreAdventor", 45))
        self.tb.grid(row=1, column=8, sticky=E+W+N+S)
        #record button
        self.rb = Button(self, anchor=N, text="Record", bg="red", font=("TexGyreAdventor", 45))
        self.rb.grid(row=3, column=7, rowspan=2, columnspan=2, sticky=E+W+N+S)
        #user input window
        self.uiw = Entry(self, bg="white", font=("TexGyreAdventor", 45))
        self.uiw.grid(row=1, column=1, columnspan=6, sticky=E+W+N+S)
        #output window
        self.ow = Label(self, text="W.I.P.", anchor=N, bg="white", height=1, font=("TexGyreAdventor", 30))
        self.ow.grid(row=3, column=1, rowspan=2, columnspan=5, sticky=E+W+N+S)

        ###############
        #quick buttons#
        ###############

        self.qb1 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb1.grid(row=6, column=1, sticky=E+W+N+S)
        self.qb2 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb2.grid(row=6, column=2, sticky=E+W+N+S)
        self.qb3 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb3.grid(row=6, column=3, sticky=E+W+N+S)
        self.qb4 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb4.grid(row=6, column=4, sticky=E+W+N+S)
        self.qb5 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb5.grid(row=6, column=5, sticky=E+W+N+S)
        self.qb6 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb6.grid(row=6, column=6, sticky=E+W+N+S)
        self.qb7 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb7.grid(row=6, column=7, sticky=E+W+N+S)
        self.qb8 = Button(self, anchor=N, text="-", bg="grey", font=("TexGyreAdventor", 45))
        self.qb8.grid(row=6, column=8, sticky=E+W+N+S)

        #details
        #self.bg1 = Label(self, bg="black")
        #self.bg1.grid(row=1, column=9, rowspan=8, sticky=E+W+N+S)
        #self.bg2 = Label(self, bg="black")
        #self.bg2.grid(row=0, column=0, columnspan=9, sticky=E+W+N+S)

window = Tk()
p = MainGUI(window)
window.mainloop()
