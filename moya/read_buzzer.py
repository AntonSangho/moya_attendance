#!/usr/bin/env python
import platform

def rfid_read():
        return "rfid read--->"

def rfid_write():
        sysnm = platform.system()
        if sysnm is "Linux":
                import RPi.GPIO as GPIO
                from mfrc522 import SimpleMFRC522
                reader = SimpleMFRC522()

                try:
                        text = "test1"
                        print("Now place your tag to write")
                        reader.write(text)
                except Exception as e:
                         print("write error  %d: %s" %(e.args[0], e.args[1]))
                         raise
                finally:
                        GPIO.cleanup()
                        return "write"

def rfid_rpi_read():
        sysnm = platform.system()
        if sysnm is "Linux":
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

        return sysnm;
