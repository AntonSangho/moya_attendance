from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
reader = SimpleMFRC522()
status = [reader.read(), 'complete card read']

print(status)
GPIO.cleanup()

