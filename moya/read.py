from time import sleep
import sys
from mfrc522 import SimpleMFRC522
#from rfid_read_exception import RfidReadException

import RPi.GPIO as GPIO
reader = SimpleMFRC522()


def read():
    try:
        id, text = reader.read_no_block()
        #id, text = reader.read_block()
        # print("ID: %s\nText: %s" % (id,text))
        lis = [id, text]
        sleep(0.5)
    except Exception as e:
        GPIO.cleanup() 
        print('예외가 발생했습니다.', e)
#        raise RfidReadException()
    finally:
        return lis
