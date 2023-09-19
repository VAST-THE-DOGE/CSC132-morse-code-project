#recieve
import RPi.GPIO as GPIO
SENSOR = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)