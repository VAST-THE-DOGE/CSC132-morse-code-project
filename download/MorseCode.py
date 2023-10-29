#imports
from time import sleep, time
from tkinter import *
from os import _exit, system
from pygame import mixer
##################################################################
#Settings
ADMIN = True
FULLSCREEN = True
DEBUG = False
SHUTDOWN = False
SEND_SPEED = 0.2 #in seconds# the tested min is 0.1 or so
MAX_SEND_TIME = 30 #in seconds# it uses the formula "(length of list to send) multiplied by (SEND_SPEED)" I would use a number that is half as much as you want the max to be
RECORD_IDLE_TIME = 5 #in seconds#
RECORD_OFF_TIME = 0.001 #in seconds#
EXTRA_EFFECTS = True
PRINT_RECORDING_TIME = True
#GPIO Stuff
SENSOR = 0 #GPIO IN PIN
RED_LED = 0 #GPIO OUT PIN 1
IR_LED = 0 #GPIO OUT PIN 2
#sound file for Extra Effects
mixer.init()
sound = mixer.Sound("beep.wav")
###################################################################
try: #try to enable the gpio to see if you are on the RPi or not
    if DEBUG: print("--setupGPIO--"), print("--START--")
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(IR_LED, GPIO.OUT)
    if DEBUG: print("--END--"), print("--setupGPIO--")
    GPIO_ACTIVE = True
except: #do this if gpio setup fails.
    GPIO_ACTIVE = False
    if DEBUG: print("--!!FAILED_TO_SETUP!!--"), print("--setupGPIO--")

#Translation lists. keep the values to translate in the same index! the values "^", "-", ".", "/", and " " are translated in the ENGtoMC and MCtoENG functions.
N_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "0","1","2","3","4","5","6","7","8","9",'&',"'",'@',')','(',':',',','=','!','+','"','?',';','$']
MC_ALPHABET = ['. - ', '- . . . ', '- . - . ', '- . . ', '. ', '. . - . ', '- - . ', '. . . . ', '. . ', '. - - - ', '- . - ', '. - . . ', '- - ', '- . ', '- - - ', '. - - . ', '- - . - ', '. - . ', '. . . ', '- ', '. . - ', '. . . - ', '. - - ', '- . . - ', '- . - - ', '- - . ', '- - - - - ','. - - - - ','. . - - - ','. . . - - ','. . . . - ','. . . . . ','- . . . . ','- - . . . ','- - - . . ','- - - - . ','. - . . . ',". - - - - . ",'. - - . - . ','- . - - . - ','- . - - . ','- . - - . ','- - . . - - ','- . . . - ','- . - . - - ','. - . - . ','. - . . - . ','. . - - . . ','- . - . - . ','. . . - . . - ']

#gui setup
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
        width //= 8 #set this up for columns 
        height //= 9 #set this up for rows

        for row in range(9*height): #setup the rows and columns
            Grid.rowconfigure(self, row, weight=1)
        for col in range(8*width):
            Grid.columnconfigure(self, col, weight=1)
        self.config(bg="light grey")
        self.pack(fill=BOTH, expand=1)
        #bunch of gui stuff.
        #exit button
        self.eb = Button(self, text="X", bg="red", command=lambda: end(), font=("TexGyreAdventor", 30))
        self.eb.grid(row=0*height, column=9*width, sticky=E+W+N+S, padx=5, pady=5)
        #translate button
        self.tb = Button(self,  text="Send", bg="green", font=("TexGyreAdventor", 45), command=lambda: self.send(self.uiw.get()))
        self.tb.grid(row=1*height, column=8*width, sticky=E+W+N+S, padx=5, pady=5)
        #record button
        self.rb = Button(self,  text="Record", bg="orange", command=lambda: self.recordEND(MCtoENG(TIMEtoMC(self.record()))), font=("TexGyreAdventor", 45))
        self.rb.grid(row=3*height, column=7*width, rowspan=2*height, columnspan=2*width, sticky=E+W+N+S, padx=5, pady=5)
        #user input window
        self.uiw = Entry(self, bg="white", font=("TexGyreAdventor", 45))
        self.uiw.grid(row=1*height, column=1*width, columnspan=6*width, sticky=E+W+N+S, padx=5, pady=5)
        #output window
        self.OWtext = StringVar()
        self.ow = Label(self, textvariable=self.OWtext, anchor=N+W, bg="white", height=1, font=("TexGyreAdventor", 25))
        self.ow.grid(row=3*height, column=1*width, rowspan=2*height, columnspan=5*width, sticky=E+W+N+S, padx=5, pady=5)
        self.OWtext.set('Type "c/help" without the quotation marks in the translation area \nand click send for a list of commands')
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

    def send(self, sendInfo): #sendding function that is called with the "send" button.
        if DEBUG: print("----send----"), print("----START----")
        #test to see if "c/" was used and if so consider the input as a command instead of something to send.
        if ((sendInfo.lower()).split("/"))[0] == "c": self.command(((sendInfo.lower()).split("/")))
        else: #if a command was not used.
            newSendInfo = ENGtoMC(sendInfo)
            if GPIO_ACTIVE:
                newSendInfo = newSendInfo.split()
                if (len(newSendInfo) * SEND_SPEED) < MAX_SEND_TIME: #guess how long it would take to send and make sure it is not a crazy number.
                    if DEBUG: print("---GPIO_IS_ON---")
                    self.OWtext.set("translating: " + sendInfo + "\n sending: " + newSendInfo)
                    if DEBUG: print(newSendInfo)
                    SEND_SPEED_3, SEND_SPEED_2, SEND_SPEED_4 = (3 * SEND_SPEED), (2 * SEND_SPEED), (4 * SEND_SPEED)
                    for value in newSendInfo:
        #A dot lasts for one second.
        #A dash lasts for three seconds. 
        #The space between dots and dashes that are part of the same letter is one second.
        #The space between different letters is three seconds.
        #The space between different words is seven seconds.
                        if value == ".":
                            if EXTRA_EFFECTS: sound.play(-1)
                            GPIO.output(RED_LED, True), GPIO.output(IR_LED, True)
                            sleep(SEND_SPEED)
                            if EXTRA_EFFECTS: sound.stop()
                            GPIO.output(RED_LED, False), GPIO.output(IR_LED, False)
                            sleep(SEND_SPEED)
                        elif value == "-":
                            if EXTRA_EFFECTS: sound.play(-1)
                            GPIO.output(RED_LED, True), GPIO.output(IR_LED, True)
                            sleep(SEND_SPEED_3)
                            if EXTRA_EFFECTS: sound.stop()
                            GPIO.output(RED_LED, False), GPIO.output(IR_LED, False)
                            sleep(SEND_SPEED)
                        elif value == "/": #end of - or . is 1 second + 2 = 3
                            sleep(SEND_SPEED_2)
                        elif value == "^": #end of - or . is 1 second + 4 + 2 seconds from the / after = 7
                            sleep(SEND_SPEED_4)
                        else:
                            if DEBUG: print("--UNKNOWN_INPUT--"), print("'{}' WILL NOT SEND!".format(value))
            else:
                if DEBUG: print("---!!!GPIO_IS_OFF!!!---")
                self.OWtext.set("translating: " + sendInfo + "\n sending: " + newSendInfo + "\n GPIO IS OFF! THIS WILL NOT SEND!!!")
        if DEBUG: print("----END----"), print("----send----")

    def record(self):
        if DEBUG: print("----record----"), print("----START----")
        if GPIO_ACTIVE:
            if DEBUG: print("---GPIO_IS_ON---")
            times = []
            StartTime = time()
            #wait until there is IR light detected
            while not GPIO.input(SENSOR):
                if time() - StartTime >= RECORD_IDLE_TIME: return [0]
            #start recording
            while True:
                #get ON/OFF time
                if GPIO.input(SENSOR): Time = self.recordON()
                else: Time = self.recordOFF()
                #if time == idle time: return the string and end recording
                if Time == -RECORD_IDLE_TIME: return times
                #else: find the time difference and find the next symbol
                times.append(Time)
             
        else:
            if DEBUG: print("---!!!GPIO_IS_OFF!!!---")
            self.OWtext.set(("GPIO IS OFF! RECORDING IS OFFLINE!!!"))
            return "GPIO IS OFF! RECORDING IS OFFLINE!!!"

    def recordON(self):
        StartTime = time()
        if EXTRA_EFFECTS: sound.play(-1), GPIO.output(RED_LED, True), GPIO.output(IR_LED, True)
        while True:
            if PRINT_RECORDING_TIME: self.OWtext.set("ON:", round(time() - StartTime, 3))
            if not GPIO.input(SENSOR):
                startOFF = time()
                while not GPIO.input(SENSOR):
                    if time() - startOFF > RECORD_OFF_TIME: return ((time() - StartTime) - RECORD_OFF_TIME)
    def recordOFF(self):
        StartTime = time()
        if EXTRA_EFFECTS: sound.stop(), GPIO.output(RED_LED, False), GPIO.output(IR_LED, False)
        while not GPIO.input(SENSOR):
            if PRINT_RECORDING_TIME: self.OWtext.set("OFF:", round(time() - StartTime, 3))
            if time() - StartTime >= RECORD_IDLE_TIME: return -RECORD_IDLE_TIME
        return -((time() - StartTime) + RECORD_OFF_TIME)
    
    def recordEND(self, string):
        self.OWtext.set(("STRING: {}".format(MCtoENG(string))))
        self.ow.config(text=(string)), sound.stop(), GPIO.output(RED_LED, False), GPIO.output(IR_LED, False)
        if DEBUG: print("----END----"), print("----record----")

    def command(self, line):
        global ADMIN
        if line[1] == "help": out = '"c/fullscreen/[True or False]","c/quit",\n"c/debug/[True or False]","c/sendspeed/[number > 0]",\n"c/idletime/[number > 0]","c/sendspeed/[number > 0]",\n"c/offtime/[number > 0]"'
        elif line[1] == "fullscreen":
            if ADMIN == True:
                try:
                    window.attributes("-fullscreen", (line[2].replace("[","")).replace("]",""))
                    out = "Set fullscreen to {}".format((line[2].replace("[","")).replace("]",""))
                except: out = "!!!Error Getting True/False Value!!!"
            else: out = "!admin command was not executed!"
        elif line[1] == "quit":
            if ADMIN == True:
                out = "Quiting the Program"
                _exit(0)
        elif line[1] == "debug":
            if ADMIN == True:
                try:
                    global DEBUG
                    DEBUG = ((line[2].replace("[","")).replace("]",""))
                    out = "Set debug to {}".format(DEBUG)
                except: out = "!!!Error Getting True/False Value!!!"
            else: out = "!admin command was not executed!"
        elif line[1] == "admin":
            try:
                ADMIN = ((line[2].replace("[","")).replace("]",""))
                out = "Set admin to {}".format(ADMIN)
            except: out = "!!!Error Getting True/False Value!!!"
        elif line[1] == "sendspeed":
            try:
                global SEND_SPEED
                value = float((line[2].replace("[","")).replace("]",""))
                if value > 0:
                    SEND_SPEED = value
                    out = "Set send speed to {}".format(value)
                else: out = "!!{} is NOT above 0!!".format(value)
            except: out = "!!!Error Getting Float or Integer Value!!!"
        elif line[1] == "idletime":
            try:
                global RECORD_IDLE_TIME
                value = float((line[2].replace("[","")).replace("]",""))
                if value > 0:
                    RECORD_IDLE_TIME = value
                    out = "Set recording idle time to {}".format(value)
                else: out = "!!{} is NOT above 0!!".format(value)
            except: out = "!!!Error Getting Float or Integer Value!!!"
        elif line[1] == "offtime":
            if ADMIN == True:
                try:
                    global RECORD_OFF_TIME
                    value = float((line[2].replace("[","")).replace("]",""))
                    if value > 0:
                        RECORD_OFF_TIME = value
                        out = "Set recording off time to {}".format(value)
                    else: out = "!!{} is NOT above 0!!".format(value)
                except: out = "!!!Error Getting Float or Integer Value!!!"
            else: out = "!admin command was not executed!"
        else: out = '!!Invalid Command!! Use "c/help"'
        print(out)
        self.OWtext.set(out)

def TIMEtoMC(times):
    if DEBUG: print("times:", times)
    string = ""
    SendSpeed = SEND_SPEED
    for index in range(0, len(times), 2):
        if times[index] > 0:
            if DEBUG: print("record speed input:", times[index], times[index + 1])
            SendSpeed = recordSpeedFind(times[index], times[index + 1])
            if SendSpeed != None: print("FOUND:", SendSpeed); break #if the string is not ""
    for value in times:
        string += recordSymbolFind(value, SendSpeed)
    return string

def recordSpeedFind(CurrentTime, Time):
    TimeDif = CurrentTime / Time
    if  TimeDif > -0.23809523809523809 and TimeDif <= 0:#.to// #-0.14285714285714285
        return (Time * -1)
    elif  TimeDif > -0.38095238095238094 and TimeDif <= -0.23809523809523809: #.to/ -0.33333333333333333
        return CurrentTime
    elif  TimeDif > -0.714285714285714275 and TimeDif <= -0.38095238095238094:#-to// #-0.42857142857142855
        return -Time
    elif  TimeDif > -2 and TimeDif <= -0.714285714285714275: #.to# or -to/ -1.0 ######
        return None
    elif  TimeDif > -4 and TimeDif <= -2:#-to# -3.0
        return -Time
    else: #error
        print("!!!finding_error!!!")
        return None

def recordSymbolFind(Time, SendSpeed):
    Time /= SendSpeed
    if Time > 2 and Time <= 5: #3 -
        return "- "
    elif Time > 0 and Time <= 2: #1 .
        return ". "
    elif Time > -2 and Time <= 0: #-1 None
        return ""
    elif Time > -5 and Time <= -2: #-3 /
        return "/ "
    elif Time > -10 and Time <= -5: #-7 ^ / 
        return "/ ^ / "
    else: #error
        print("!!!setting_error!!!")
        return "? / "

def ENGtoMC(string):
    if DEBUG: print("--ENGtoMC--"), print("--START--")
    string = string.lower() #set all to lowercase to keep it the same.
    #remove or change symbols that will create errors, the rest will be ignored.
    string = ((((string.replace("^", "")).replace("/", "*/*")).replace(".", "*.*")).replace(" ", "^ / ")).replace("-", "- . . . . - / ")
    string = (string.replace("*/*", "- . . - . / ")).replace("*.*", ". - . - . - / ")
    #end of removing
    for index in range(0 ,len(N_ALPHABET)): #replace the letters.
        string = string.replace(N_ALPHABET[index], (MC_ALPHABET[index] + "/ "))
    if DEBUG: print("--END--"), print("--ENGtoMC--")
    return string

def MCtoENG(string):
    if DEBUG: print("--MCtoENG--"), print("--START--")
    try:
        letters = string.split("/ ") #make the string into a list
        for index in range(0 ,len(letters)):
            try:
                replaceWithIndex = MC_ALPHABET.index(letters[index]) #find the MC index of the letter
                letters[index] = N_ALPHABET[replaceWithIndex] #replace the letter using this index with the normal alphabet
            except: pass
        string = (((("".join(letters)).replace(". - . - . - ", ".")).replace("- . . - . ", "/")).replace("- . . . . - ", "-")).replace("^ ", " ") #make the list into a string
    except:
        pass
    if DEBUG: print("--END--"), print("--MCtoENG--")
    return string

def end():
    if DEBUG: print("-----END-----"), print("-----main-----")
    window.attributes("-fullscreen", False)
    if GPIO_ACTIVE and SHUTDOWN: system("sudo shutdown -h now")
    _exit(0)

if DEBUG: print("-----main-----"), print("-----START-----")
window = Tk()
window.title("Morse Code Translator")

p = MainGUI(window)
window.mainloop()
if DEBUG: print("-----END-----"), print("-----main-----")

