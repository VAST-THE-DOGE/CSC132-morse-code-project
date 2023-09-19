#send
import RPi.GPIO as GPIO
BUTTON = 0
RED = 0
IR = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(BUTTON) == True:
        while GPIO.input(BUTTON) == True:
            GPIO.output(RED, True)
            GPIO.output(IR, True)
    GPIO.output(RED, False)
    GPIO.output(IR, False)          
