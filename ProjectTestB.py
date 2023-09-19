#recieve
from time import time
import RPi.GPIO as GPIO
SENSOR = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
  if GPIO.input(SENSOR) == True:
    StartTime = time()
    while GPIO.input(SENSOR) == True:
      pass
    EndTime = time()
    TimeOn = EndTime - StartTime
