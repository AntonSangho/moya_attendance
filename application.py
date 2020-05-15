#-*- coding:utf-8 -*-
import os
from flask import Flask, render_template
from moya.read_buzzer import rfid_read, rfid_rpi_read

import moya.Write




application = Flask(__name__)
application.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )
application.env = 'development'
application.debug = True


@application.route('/')
@application.route('/<user>')
def index(user=''):
    print(rfid_read())
    print(rfid_rpi_read())
    return render_template('entry.html', name=user, platform=rfid_rpi_read())
    # url test1 request path /두루
    # url test2 request path /
    # if user exist turn on green led

@application.route('/entrance')
#activate when push button GPIO 6
#pop up message "출입증을 태깅하세요"
#blink red_rfid led
@application.route('/exit')
#activate when push button GPIO 12
#pop up message "출입증을 태깅하세요"
#blink red_rfid led
@application.route('/gpio')
def gpio():
    return render_template('main2.html')

@application.route("/<changePin>/<action>")
def action (changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    templateData = {
        'message' : 'message',
        'pin' : 'pins'
    }
    return render_template('main2.html', **templateData)



# Run the application
if __name__ == "__main__":
    application.run(host="0.0.0.0")
