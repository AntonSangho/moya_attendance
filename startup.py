import time
from threading import Thread
import os


def startprgm(i):
    print("Running thread %d" % i)
    if i == 0:
        time.sleep(1)
        print('Running: shutdown command')
        os.system("sudo shutdown -h now")
    elif i == 1:
        print('Running: gpio.py')
        time.sleep(1)
        os.system("sudo modeprobe -i uinput")
        time.sleep(1)
        os.system("sudo python3 /home/pi/moya_attendance/gpio.py")
        print('Running: application.py')
        time.sleep(1)
        os.system("sudo python3 /home/pi/moya_attendance/application.py")
    else:
        pass


for i in range(2):
    t = Thread(target=startprgm, args=(i,))
    t.start()
