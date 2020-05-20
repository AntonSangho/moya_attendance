# -*- coding: utf-8 -*-
from moya.driver_rpi import  rfid_write, rfid_read

import hashlib 
import random

hash = random.getrandbits(128)

print("hash value: %032x" % hash)
print("rfid write test")
print(rfid_write(hashlib.md5("{hash}".encode("utf8"))))
print("rfid write test-----")


print("rpi buzz test")
print(rfid_read())
print("rfid buzz test-----")