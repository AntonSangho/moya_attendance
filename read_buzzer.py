#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=5
GPIO.setup(buzzer,GPIO.OUT)

reader = SimpleMFRC522()
try:
        id, text = reader.read()
        print(id)
        print(text)
        
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.5)

finally:
        GPIO.cleanup()
