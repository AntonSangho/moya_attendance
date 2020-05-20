#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import os.path 

def rfid_read():
        return "rfid read--->"

def rfid_write():
        try:
                file = '/proc/device-tree/model'
                status = '결과'
                if not os.path.isfile(file) :
                        status = '이플랫폼은 지원하지 않습니다.'
                        return False;

                with open(file, 'wb') as f:
                        sysnm = f.readline()
                        print(sysnm)
                        
                        import RPi.GPIO as GPIO
                        from mfrc522 import SimpleMFRC522
                        reader = SimpleMFRC522()
                        text = "test1"
                        print("카드 기록중....")
                        reader.write(text)
                        GPIO.cleanup()
                        status = '쓰기 완료'
        except Exception as e:
                         print("write error  %d: %s" %(e.args[0], e.args[1]))
                         #로깅작업
                         raise
        finally:
                        return status

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
