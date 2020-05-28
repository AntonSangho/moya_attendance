import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER= 5
buzzState = False
GPIO.setup(BUZZER, GPIO.OUT)

while True:
    buzzState = not buzzState
    GPIO.output(BUZZER, buzzState)
    time.sleep(0.5)
