#recieve
from time import time
import RPi.GPIO as GPIO
SENSOR = 0 #GPIIO PIN HERE
TimeToTest = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def find(SENSOR, TimeToTest):
    i = 0
    while i < TimeToTest:
        if GPIO.input(SENSOR) == True:
            StartTime = time()
            while GPIO.input(SENSOR) == True:
                pass
            EndTime = time()
            return EndTime - StartTime
        i += 1

print(find(SENSOR, TimeToTest))
