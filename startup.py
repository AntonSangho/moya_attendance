import time
from threading import Thread
import os


def startprgm():
    print('Running: gpio.py')
    time.sleep(1)
    os.system("sudo modeprobe -i uinput")
    time.sleep(1)
    os.system("sudo python3 /home/pi/moya_attendance/gpio.py")
    print('Running: application.py')
    time.sleep(1)
    os.system("sudo python3 /home/pi/moya_attendance/application.py")


for i in range(2):
    t = Thread(target=startprgm, args=(i,))
    t.start()
