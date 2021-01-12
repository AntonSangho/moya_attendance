import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import uinput

events = (
        uinput.KEY_H,
        uinput.KEY_L
        )

def leftbutton_callback(channel):
        with uinput.Device(events) as device:
                time.sleep(1) 
                device.emit_click(uinput.KEY_H)
        print("Left Button was pushed!")
def rightbutton_callback(channel):
        with uinput.Device(events) as device:
                time.sleep(1) 
                device.emit_click(uinput.KEY_L)
        print("Righ Button was pushed!")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 31 to be an input pin and set initial value to be pulled high (off)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 32 to be an input pin and set initial value to be pulled high (off)

GPIO.add_event_detect(31,GPIO.FALLING,callback=leftbutton_callback) # Setup event on pin 10 rising edge
GPIO.add_event_detect(32,GPIO.FALLING,callback=rightbutton_callback)

message = input("Press enter to quit\n\n") # Run until someone presses enter
        
GPIO.cleanup() # Clean up
