import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

def buzz():
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        buzzer=5
        GPIO.setup(buzzer,GPIO.OUT)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.5)
    except Exception as e:
        GPIO.cleanup()
        print("buzz GPIO error  %d: %s" %(e.args[0], e.args[1]))
        raise
    finally:
        GPIO.cleanup()
    
    

