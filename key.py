from pynput.keyboard import Key, Controller

keyboard = Controller()

keyboard.press('a')
keyboard.release('a')
