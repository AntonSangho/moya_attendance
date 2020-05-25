#-*- coding:utf-8 -*-
import os
from flask import Flask, render_template, jsonify
from moya.driver_rpi import rfid_read, rfid_write, buzzer_call

from moya.driver_db import init_connect_db, get_attendance, set_attendance, set_exit



application = Flask(__name__)
application.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )
application.env = 'development'
application.debug = True

@application.route('/')
def index(user=''):
    print(application.env)
    return render_template('index.html', platform="뭐야")


@application.route('/entry')
@application.route('/entry/<user>')
def entry(user=''):
    print(application.env)
    return render_template('entry.html', msg="카드를 올려 놓으세요!", platform="입장")
    # url test1 request path /두루
    # url test2 request path /
    # if user exist turn on green led


@application.route('/exits')
@application.route('/exits/<user>')
def exis(user=''):
    print(application.env)
    return render_template('exits.html', msg="카드를 올려 놓으세요!", platform="퇴장")
    # url test1 request path /두루
    # url test2 request path /
    # if user exist turn on green led


@application.route('/api/v1.0/entry', methods=['GET'])
def endpoint_rfid_read():
    print("rpi buzz test")
    rst = rfid_read()
    print("rfid buzz test-----")
    if rst[0] != "not support this platform.":
        print(f"{rst[1]}, {rst[2]}")
        if rst[2] != None:
            userid = int(rst[2])
            db = init_connect_db()
            rst.append("DB TRUE" if set_attendance(db, userid) else "DB FALSE")
            buzzer_call()

    return jsonify({'ps': rst})


@application.route('/api/v1.0/exits', methods=['GET'])
def endpoint_rfid_read_exit():
    print("rpi buzz test- exit")
    rst = rfid_read()
    if rst[0] != "not support this platform.":
        print(f"{rst[1]}, {rst[2]}")
        if rst[2] != None:
            userid = int(rst[2])
            db = init_connect_db()
            rst.append("DB TRUE" if set_exit(db, userid) else "DB FALSE")
            buzzer_call()

    return jsonify({'ps': rst})





@application.route('/dbtest')
def dbselect():
    db = init_connect_db()
    lists = get_attendance(db)
    print(lists)
    return "db select test"

@application.route('/db_insert_test/<cnt>')
def dbinsert(cnt):
    import random
    db = init_connect_db()
    if cnt :
       for i in range(int(cnt)):
        success = set_attendance(db, (random.randint(0, 10)%2)) #(i%2))
    
    return "db insert test /db_insert_test/1000 insert test"
    

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
