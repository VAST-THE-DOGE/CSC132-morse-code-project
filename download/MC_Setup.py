from tkinter import *
from os import _exit, system, remove
from time import sleep
AutoStart=False

class MainGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        for row in range(5): #setup the rows and columns
            Grid.rowconfigure(self, row, weight=1)
        for col in range(10):
            Grid.columnconfigure(self, col, weight=1)
        self.config(bg="light grey")
        self.pack(fill=BOTH, expand=1)
        self.ib = Button(self, text="Install", bg="green", command=lambda: self.install(), font=("TexGyreAdventor", 30))
        self.ib.grid(row=1, column=4, columnspan=4, sticky=E+W+N+S, padx=5, pady=5)
        self.ub = Button(self, text="uninstall", bg="red", command=lambda: self.uninstall(), font=("TexGyreAdventor", 30))
        self.ub.grid(row=3, column=4, columnspan=4, sticky=E+W+N+S, padx=5, pady=5)
        self.ab = Button(self, text="autostart", bg="grey", command=lambda: self.change(), font=("TexGyreAdventor", 20))
        self.ab.grid(row=1, column=1, columnspan=2, sticky=E+W+N+S, padx=5, pady=5)
        self.al = Label(self, text="False", bg="grey", font=("TexGyreAdventor", 20))
        self.al.grid(row=3, column=1, columnspan=2, sticky=E+W+N+S, padx=5, pady=5)
    def change(self):
        global AutoStart
        AutoStart=(not AutoStart)
        if AutoStart: self.al.config(text="True")
        else: self.al.config(text="False")
    def install(self):

        if AutoStart:
            try:
                system("sudo mv home/pi/Downloads/MorseCode.desktop /etc/xdg/autostart")
            except:
                print('failed to move "MorseCode.desktop"')
                
        try:
            system("sudo mv home/pi/Downloads/MorseCode.py /Desktop")
            system("sudo mv home/pi/Downloads/beep.wav /Desktop")
        except:
            print('failed to move "MorseCode.py"')
        out="Installed! Starting script in 5 seconds."
        self.ib.destroy()
        self.ub.destroy()
        self.ab.destroy()
        self.al.destroy()
        self.ei = Label(self, text=out, bg="gray", font=("TexGyreAdventor", 20))
        self.ei.grid(row=0, column=0, columnspan=5, rowspan=10, sticky=E+W+N+S, padx=5, pady=5)
        sleep(5)
        try:
            system("home/pi/Desktop/MorseCode.py")
            _exit(0)
        except:
            pass
        _exit(0)
    def uninstall(self):
        try:
            remove("/etc/xdg/autostart/MorseCode.desktop")
            remove("home/pi/Desktop/MorseCode.py")
            remove("home/pi/Desktop/beep.wav")
        except: print("error")

window = Tk()
window.title("Morse Code Translator")

p = MainGUI(window)
window.mainloop()
