# #!/usr/bin/env python

# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
import platform

#라스베리파이에서 나오는 문자열 확인
print(platform.system())
# reader = SimpleMFRC522()

# try:
#         text = input('New data:')
#         print("Now place your tag to write")
#         reader.write(text)
#         print("Written")
# finally:
#         GPIO.cleanup()
