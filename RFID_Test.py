from time import sleep
import sys
from mfrc522 import SimpleMFRC522
from moya.driver_rpi import rfid_read, rfid_write, buzzer_call
import RPi.GPIO as GPIO

# read = SimpleMFRC522()
reader = SimpleMFRC522()
GPIO.setwarnings(False)


try:
    while True:
        GPIO.cleanup()
        print("Hold a tag near the reader")
        # id, text = read.read()
        id, text = reader.read_no_block()
        lis = [id, text]
        print("ID: %s\nText: %s" % (lis[0], lis[1]))
        # 카드의 text값이 있는 경우 
        if lis[1]:  
           buzzer_call()
           # 인식된걸로 처리 
        else:
            sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
