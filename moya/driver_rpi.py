#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path 
import importlib
from time import sleep
from . import rfid_read_exception


def load_module(module_name):
    return importlib.import_module(module_name)

def is_support_platform():
        rpi_file = '/proc/device-tree/model'
        print(rpi_file)
        return os.path.exists(rpi_file)

def load_package():
        load_module('RPi.GPIO as GPIO')
        load_module('from mfrc522 import SimpleMFRC522')


def rfid_write(tag_text):
        try:
                status = 'not suppert this platform.'
                if not is_support_platform():
                        return False
                status = 'support this platform'
                from . import write
                write.rpi_rfid_write(tag_text)
                status = 'complete write card'
        except Exception as e:
                         print("write error  %d: %s" %(e.args[0], e.args[1]))
                         #로깅작업
                         raise
        finally:
                return status

def rfid_read():
        try:
                status = ['not support this platform.']
                if not is_support_platform():
                        return False
                status = ['support this platform']
                from . import read
                status = status + read.read()
        except Exception as e:
                print("rfid read error  %d: %s" %(e.args[0], e.args[1]))
        finally:
                return status
       
        


def buzzer_call():
        from . import buzz
        buzz.buzz()