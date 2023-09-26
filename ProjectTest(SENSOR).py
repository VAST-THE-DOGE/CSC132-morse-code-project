#recieve
from time import time
import RPi.GPIO as GPIO
RED = 0
SENSOR = 0
TimeToTest = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def find(SENSOR, TimeToTest):
    
    while True:
        if GPIO.input(SENSOR) == True:
            StartTime = time()
            while GPIO.input(SENSOR) == True:
                GPIO.output(RED, True)
            EndTime = time()
            return EndTime - StartTime
        

print(find(SENSOR, TimeToTest))