#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path 


def is_support_platform():
        rpi_file = '/proc/device-tree/model'
        print(rpi_file)
        return os.path.exists(rpi_file)
        

def rfid_write():
        try:
                status = 'not suppert this platform.'
                if not is_support_platform():
                        return False
                print("GPIO Cleanup")
                import RPi.GPIO as GPIO
                from mfrc522 import SimpleMFRC522
                GPIO.cleanup()
                GPIO.setwarnings(False)

                reader = SimpleMFRC522()
                text = "test1"
                print("put card....")
                reader.write(text.zfill(255, '0'))
                print("recording card...")
                GPIO.cleanup()
                status = 'complete write card'
        except Exception as e:
                         print("write error  %d: %s" %(e.args[0], e.args[1]))
                         #로깅작업
                         raise
        finally:
                        return status

def rfid_read():
        try:
                status = ['not suppert this platform.']
                if not is_support_platform():
                        return False
                
                import RPi.GPIO as GPIO
                from mfrc522 import SimpleMFRC522
                from time import sleep

                #GPIO 셋팅
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                buzzer=5
                GPIO.setup(buzzer,GPIO.OUT)
                GPIO.output(buzzer,GPIO.HIGH)
                sleep(0.5)
                GPIO.output(buzzer,GPIO.LOW)
                sleep(0.5)
                ## 읽기 작업 rfid
                reader = SimpleMFRC522()
                status = [reader.read(), 'complete card read']

                GPIO.cleanup()
        except Exception as e:
                print("rfid read error  %d: %s" %(e.args[0], e.args[1]))
                         #로깅작업
                raise
        finally:
                return status

