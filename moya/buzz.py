import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

def buzz():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    buzzer=5
    GPIO.setup(buzzer,GPIO.OUT)
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.5)
    GPIO.cleanup()

