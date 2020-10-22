from time import sleep
import sys
from mfrc522 import SimpleMFRC522
read = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = read.read()
        print("ID: %s\nText: %s" % (id, text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise


