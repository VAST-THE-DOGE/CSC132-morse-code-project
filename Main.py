#imports
from time import sleep
from time import time
from tkinter import *
import sys
import os
#Settings
FULLSCREEN = True
DEBUG = True
SHUTDOWN = False
SEND_SPEED = 0.1
#get the system color
#wip
COLOR = True #True = light mode; False = dark mode
if COLOR:
    pass
else:
    pass
#GPIO Stuff
SENSOR = 0 #GPIO PIN OF THE SENSOR
RED_LED = 0 #GPIO PIN OF THE RED LED
IR_LED = 0 #GPIO PIN OF THE IR LED


try:
    if DEBUG: print("--setupGPIO--"), print("--START--")
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(IR_LED, GPIO.OUT)
    if DEBUG: print("--END--"), print("--setupGPIO--")
    GPIO_ACTIVE = True
except:
    GPIO_ACTIVE = False
    if DEBUG: print("--!!FAILED_TO_SETUP!!--"), print("--setupGPIO--")

#KEEP THIS THE SAME!
N_ALPHABET = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
MC_ALPHABET = ['^ ', '. - ', '- . . . ', '- . - . ', '- . . ', '. ', '. . - . ', '- - . ', '. . . . ', '. . ', '. - - - ', '- . - ', '. - . . ', '- - ', '- . ', '- - - ', '. - - . ', '- - . - ', '. - . ', '. . . ', '- ', '. . - ', '. . . - ', '. - - ', '- . . - ', '- . - - ', '- - . ']

if GPIO_ACTIVE:
    if DEBUG: print("--setupGPIO--"), print("--START--")
    from time import sleep
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(IR_LED, GPIO.OUT)
    if DEBUG: print("--END--"), print("--setupGPIO--")

class MainGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        if FULLSCREEN: parent.attributes("-fullscreen", True)
        self.setupGUI()
    def setupGUI(self):
        if DEBUG: print("--setupGUI--"), print("--START--")
        self.update_idletasks() # update the window state
        width = self.winfo_screenwidth() # get the window width
        height = self.winfo_screenheight() # get the window height
        print(width)
        print(height)
        width //= 8
        height //= 9

        for row in range(9*height): #setup the rows and columns
            Grid.rowconfigure(self, row, weight=1)
        for col in range(8*width):
            Grid.columnconfigure(self, col, weight=1)
        self.config(bg="light grey")
        self.pack(fill=BOTH, expand=1)
        
        #exit button
        self.eb = Button(self, text="X", bg="red", command=lambda: end(GPIO_ACTIVE), font=("TexGyreAdventor", 30))
        self.eb.grid(row=0*height, column=9*width, sticky=E+W+N+S, padx=5, pady=5)
        #translate button
        self.tb = Button(self,  text="Send", bg="green", font=("TexGyreAdventor", 45), command=lambda: self.send(self.uiw.get()))
        self.tb.grid(row=1*height, column=8*width, sticky=E+W+N+S, padx=5, pady=5)
        #record button
        self.rb = Button(self,  text="Record", bg="orange", font=("TexGyreAdventor", 45))
        self.rb.grid(row=3*height, column=7*width, rowspan=2*height, columnspan=2*width, sticky=E+W+N+S, padx=5, pady=5)
        #user input window
        self.uiw = Entry(self, bg="white", font=("TexGyreAdventor", 45))
        self.uiw.grid(row=1*height, column=1*width, columnspan=6*width, sticky=E+W+N+S, padx=5, pady=5)
        #output window
        self.ow = Label(self, text="W.I.P.", anchor=N+W, bg="white", height=1, font=("TexGyreAdventor", 30))
        self.ow.grid(row=3*height, column=1*width, rowspan=2*height, columnspan=5*width, sticky=E+W+N+S, padx=5, pady=5)

        ###############
        #quick buttons#
        ###############

        self.qb1 = Button(self, text="SOS", bg="grey", font=("TexGyreAdventor", 45), command=lambda: self.send("SOS"))
        self.qb1.grid(row=7*height, column=1*width, sticky=E+W+N+S, padx=5, pady=5)
        self.qb2 = Button(self, text="YES", bg="grey", font=("TexGyreAdventor", 45), command=lambda: self.send("YES"))
        self.qb2.grid(row=7*height, column=2*width, sticky=E+W+N+S, padx=5, pady=5)
        self.qb3 = Button(self, text="NO", bg="grey", font=("TexGyreAdventor", 45), command=lambda: self.send("NO"))
        self.qb3.grid(row=7*height, column=3*width, sticky=E+W+N+S, padx=5, pady=5)
        self.qb4 = Button(self, text="HELLO", bg="grey", font=("TexGyreAdventor", 45), command=lambda: self.send("HELLO"))
        self.qb4.grid(row=7*height, column=4*width, sticky=E+W+N+S, padx=5, pady=5)
        self.qb5 = Button(self, text="GOODBYE", bg="grey", font=("TexGyreAdventor", 45), command=lambda: self.send("GOODBYE"))
        self.qb5.grid(row=7*height, column=5*width, sticky=E+W+N+S, padx=5, pady=5)
        if DEBUG: print("--END--"), print("--setupGUI--")

    def send(self, sendInfo):
        if DEBUG: print("----send----"), print("----START----")
        newSendInfo = ENGtoMC(sendInfo)
        if GPIO_ACTIVE:
            if DEBUG: print("---GPIO_IS_ON---")
            self.ow.config(text=("translating: " + sendInfo + "\n sending: " + newSendInfo))
            newSendInfo = newSendInfo.split()
            if DEBUG: print(newSendInfo)
            for value in newSendInfo: #############################################################
#A dot lasts for one second.
#A dash lasts for three seconds. 
#The space between dots and dashes that are part of the same letter is one second.
#The space between different letters is three seconds.
#The space between different words is seven seconds.
                if value == ".":
                    GPIO.output(RED_LED, True)
                    GPIO.output(IR_LED, True)
                    sleep(SEND_SPEED)
                    GPIO.output(RED_LED, False)
                    GPIO.output(IR_LED, False)
                    sleep(SEND_SPEED)
                elif value == "-":
                    GPIO.output(RED_LED, True)
                    GPIO.output(IR_LED, True)
                    sleep(3 * SEND_SPEED)
                    GPIO.output(RED_LED, False)
                    GPIO.output(IR_LED, False)
                    sleep(SEND_SPEED)
                elif value == "/": #end of - or . is 1 second + 2 = 3
                    sleep(2 * SEND_SPEED)
                elif value == "^": #end of - or . is 1 second + 4 + 2 seconds from the / after = 7
                    sleep(4 * SEND_SPEED)
                else:
                    if DEBUG: print("--UNKNOWN_INPUT--"), print("'{}' WILL NOT SEND!")
        else:
            if DEBUG: print("---!!!GPIO_IS_OFF!!!---")
            self.ow.config(text=("translating: " + sendInfo + "\n sending: " + newSendInfo + "\n GPIO IS OFF! THIS WILL NOT SEND!!!"))
        if DEBUG: print("----END----"), print("----send----")

def ENGtoMC(string):
    if DEBUG: print("--ENGtoMC--"), print("--START--")
    backupString = string #create a backup
    string = string.lower() #set all to lowercase to keep it the same.
    #remove symbols that will create errors, the rest will be ignored.
    string = string.replace("^", "") #seperator for words!
    string = string.replace("/", "") #seperator for letters!
    string = string.replace(".", "") #part of morse code!
    string = string.replace("-", "") #part of morse code!
    #end of removing
    if string == "": return backupString #this is if the user types morse code already
    else:
        del backupString
        for index in range(0 ,len(N_ALPHABET)): #replace the letters.
            if DEBUG: print("replace '{}' with '{}'".format(N_ALPHABET[index], (MC_ALPHABET[index] + "/ ")))
            string = string.replace(N_ALPHABET[index], (MC_ALPHABET[index] + "/ "))
    if DEBUG: print("--END--"), print("--ENGtoMC--")
    return string

def MCtoENG(string):
    if DEBUG: print("--MCtoENG--"), print("--START--")
    letters = string.split("/") #make the string into a list
    for index in range(0 ,len(letters)):
        replaceWithIndex = MC_ALPHABET.index(letters[index]) #find the MC index of the letter
        letters[index] = N_ALPHABET[replaceWithIndex] #replace the letter using this index with the normal alphabet
        if DEBUG: print("replace '{}' with '{}'".format((letters[index] + "/ "), N_ALPHABET[replaceWithIndex]))
    string = "".join(letters) #make the list into a string
    if DEBUG: print("--END--"), print("--MCtoENG--")
    return string

def Record():
    if DEBUG: print("WIP")

def end(GPIO_ACTIVE):
    window.attributes("-fullscreen", False)
    if GPIO_ACTIVE and SHUTDOWN: os.system ("sudo shutdown -h now")
    #sys.exit(0)
    os._exit(0)

if DEBUG: print("-----main-----"), print("-----START-----")
window = Tk()
window.title("Morse COde Translator")

p = MainGUI(window)
window.mainloop()
if DEBUG: print("-----END-----"), print("-----main-----")
