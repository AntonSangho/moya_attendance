# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
# from time import sleep
# import time
import os
# from omxplayer.player import OMXPlayer
# from pathlib import Path

def buzz():
    try:
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BCM)
        # buzzer=5
        os.system('omxplayer ./sound/ascend.mp3 &')
        #omxplayer wrapper
        # mp3_path = Path("./sound/ascend.mp3")
        # player = OMXPlayer(mp3_path)
        # sleep(1)
        # player.quit()
        ##
        # GPIO.setup(buzzer,GPIO.OUT)
        # GPIO.output(buzzer,GPIO.HIGH)
        # sleep(0.2)
        # GPIO.output(buzzer,GPIO.LOW)
        # sleep(0.2)
    except Exception as e:
        # GPIO.cleanup()
        # print("buzz GPIO error  %d: %s" %(e.args[0], e.args[1]))
        print("OMXplayer error  %d: %s" % (e.args[0], e.args[1]))
        raise
    # finally:
        # GPIO.cleanup()
    
    

