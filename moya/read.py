from time import sleep
import sys
from mfrc522 import SimpleMFRC522
#from rfid_read_exception import RfidReadException

import RPi.GPIO as GPIO
reader = SimpleMFRC522()


def read():
    try:
        GPIO.cleanup()       
        print("Hold a tag near the reader")
        id, text = reader.read_no_block()
        print("ID: %s\nText: %s" % (id,text))
        lis = [id, text]
        sleep(1)
    except Exception as e:
        GPIO.cleanup() 
        print('예외가 발생했습니다.', e)
#        raise RfidReadException()
    finally:
        GPIO.cleanup()
        return lis
