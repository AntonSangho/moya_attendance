import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def rpi_rfid_write():
    try:
        text = "test1"
        print("Now place your tag to write")
        reader.write(text)
        print("recording card...")
    except Exception as e:
        print("write error  %d: %s" %(e.args[0], e.args[1]))
        raise
    finally:
        GPIO.cleanup()
