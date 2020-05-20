import RPi.GPIO as GPIO
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

def read():
    try:
        while True:
            print("Hold a tag near the reader")
            id, text = reader.read()
            print("ID: %s\nText: %s" % (id,text))
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise
