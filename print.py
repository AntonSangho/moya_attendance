"""
Printe on demand with rasberrypi (https://www.hackster.io/glowascii/print-on-demand-with-raspi-d74619)
GPIO pin:

"""
# !/bin/python

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def Printtest(channel):
    print('Printing...')

    # Test printing
    os.system("echo 'This is a test.' | lp")


while 1:
    time.sleep(1)
