import os.path
rpi_file = '/proc/device-tree/model'
print(rpi_file)
print(os.path.exists(rpi_file))
