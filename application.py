#-*- coding:utf-8 -*-
import os
import shutil

from flask import Flask, render_template, jsonify, abort
from moya.driver_rpi import rfid_read, rfid_write, buzzer_call

from moya.driver_db import init_connect_db, get_attendance, set_attendance, set_exit, get_userinfo

from flask.logging import default_handler

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

application = Flask(__name__)
application.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )
application.env = 'development'
application.debug = True

application.config['HOME_DIR'] = './'
application.config['LOGGING_LEVEL'] = logging.DEBUG
application.config['LOGGING_FORMAT'] = '%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d]'
application.config['LOGGING_LOCATION'] = 'log/'
application.config['LOGGING_FILENAME'] = 'loging.log'
application.config['LOGGING_MAX_BYTES'] = 100000
application.config['LOGGING_BACKUP_COUNT'] = 1000


@application.route('/')
def index(user=''):
    print(application.env)
    return render_template('index.html', platform="뭐야")


@application.route('/entry')
@application.route('/entry/<user>')
def entry(user=''):
    try:
        print(application.env)
        return render_template('entry.html', msg="카드를 올려 놓으세요!", platform="입장")
    except Exception as e:
        return str(e)
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
    try:
        print("rpi buzz test")
        rst = rfid_read()
        print("rfid buzz test-----")
        if rst[0] != "not support this platform.":
            db = init_connect_db()
            print(f"{rst[1]}, {rst[2]}")
            

            if rst[2] != None:
                userid = int(rst[2])
                rfid_uid = rst[1]
                name = get_userinfo(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_attendance(db, userid) else "DB FALSE")
                rst.append(name[0])
                buzzer_call()
    except Exception as e:
        print("error", e)
        return abort(500)
        #return jsonify({'ps': rst.append(str(e))})

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


def file_log(e):
    log_dir = os.path.join(application.config['HOME_DIR'], application.config['LOGGING_LOCATION'])
    ensure_dir_exists(log_dir)
    file_handler = RotatingFileHandler(application.config['LOGGING_LOCATION'] + application.config['LOGGING_FILENAME'],
                                    maxBytes=application.config['LOGGING_MAX_BYTES'],
                                    backupCount=application.config['LOGGING_BACKUP_COUNT'])
    file_handler.setFormatter(Formatter(application.config['LOGGING_FORMAT']))
    file_handler.setLevel(application.config['LOGGING_LEVEL'])
    application.logger.addHandler(file_handler)
    application.logger.error(e)
    application.logger.info('error', e)


@application.errorhandler(500)
def internal_error(error):
    #내부에러가 발생시 로깅 기록
    #file_log(error)
    return render_template('index.html'), 500 


@application.errorhandler(404)
def page_not_found(error):
    #페이지를 찾을 수 없을때
    #file_log(error)
    return render_template('index.html'), 404 


def ensure_dir_exists(dir_path, recursive=False):
    if not os.path.isdir(dir_path):
        if recursive:
            os.makedirs(dir_path)
        else:
            os.mkdir(dir_path)


# Run the application
if __name__ == "__main__":
    application.run(host="0.0.0.0")
