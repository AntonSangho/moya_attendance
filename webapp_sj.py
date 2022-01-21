# -*- coding:utf-8 -*-
import os
import time
from flask import Flask, render_template, jsonify, abort, request 
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from time import sleep
from moya.driver_rpi import rfid_read, rfid_write, buzzer_call
from moya.driver_db import init_connect_db, add_newcard, is_rfid_sj, get_rfid_sj, get_userinfo_sj, set_exit_sj, set_attendance_sj, get_workingtimeWithUserid_sj
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

db = init_connect_db(2)

application = Flask(__name__, static_folder="static")

application.env = 'development'
application.debug = True
application.secret_key = '05C18B18FBDBD041342F6D0360523720934514A9C55945E64EA9D13BF74E09E5'  # sha256 str(time.time()) 10분에 한번씩 변경하도록

application.config['HOME_DIR'] = './'
application.config['LOGGING_LEVEL'] = logging.DEBUG
application.config['LOGGING_FORMAT'] = '%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d]'
application.config['LOGGING_LOCATION'] = 'log/'
application.config['LOGGING_FILENAME'] = 'loging.log'
application.config['LOGGING_MAX_BYTES'] = 100000
application.config['LOGGING_BACKUP_COUNT'] = 1000

@application.route('/webapp')
def index():
    return render_template('webapp.html', platform="세종시립도서관")

@application.route('/newcard')
def newcard():
    try:
        return render_template('newcard.html', msg="카드를 대주세요", platform="카드등록")
    except Exception as e:
        return str(e)

def get_conn():
    conn = request.cookies.get('conn')
    if conn == "1":
        return init_connect_db(1)
    elif conn == "2":
        return init_connect_db(2)
    elif conn == "3":
        return init_connect_db(3)
    else:
        return init_connect_db(4)
# 입장시 RFID카드를 인식하는 페이지
@application.route('/entry')
def entry():
    try:
        return render_template('entry.html', msg="카드를 대주세요", platform="입장")
    except Exception as e:
        return str(e)

# 퇴장시 RFID카드를 인식하는 페이지
@application.route('/exits')
def exis():
    print(application.env)
    return render_template('exits.html', msg="카드를 대주세요", platform="퇴장")

# 퇴장시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/exits', methods=['GET'])
def endpoint_rfid_read_exit():
    try:
        rst = rfid_read()
        if rst[0] != "not support this platform.":
            # db = init_connect_db()
            db = get_conn()
            if rst[2] != None:
                # 공백을 확인해서 0으로 변경
                userid = str(rst[2]).replace(' ', '') + "0"
                if len(userid) == 49:
                    userid = 0
                else:
                    userid = rst[2]
                rfid_uid = rst[1]
                #카드의 userid를 가지고 DB에 등록된 name을 가져온다
                name = get_userinfo_sj(db, userid, rfid_uid)
                #카드의 userid를 가지고 DB에 등록된 방문횟수와 작업시간을 가져온다.
                #info = get_workingtimeWithUserid_sj(db, userid)
                rst.append("DB TRUE" if set_exit_sj(db, userid) else "DB FALSE")
                # 이름이 DB에 등록되어있으면 방문횟수와 작업시간 정보를 가지고 있는다. 
                if len(name) > 0:
                    #rst.append(info[0])
                    rst.append(name[0])
                else:
                    rst.append('누구예요?')
                buzzer_call()
                time.sleep(0.1)
    except Exception as e:
        print("error", e)
        return abort(500)

    return jsonify({'ps': rst})

# 입장시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/entry', methods=['GET'])
# def endpoint_rfid_read():
def endpoint_rfid_read_entry():
    try:
        rst = rfid_read()
        if rst[0] != "not support this platform.":
            # db = init_connect_db()
            db = get_conn()
            if rst[2] != None:
                # 공백을 확인해서 0으로 변경
                userid = str(rst[2]).replace(' ', '') + "0"
                if len(userid) == 49:
                    userid = 0
                else:
                    userid = rst[2]
                rfid_uid = rst[1]
                name = get_userinfo_sj(db, userid, rfid_uid)
                # 카드의 userid를 가지고 DB에 등록된 방문횟수와 작업시간을 가져온다.
                # info = get_workingtimeWithUserid_sj(db, userid)
                rst.append("DB TRUE" if set_attendance_sj(db, userid) else "DB FALSE")
                # 이름이 DB에 등록되어있으면 방문횟수와 작업시간 정보를 가지고 있는다.
                if len(name) > 0:
                    #rst.append(info[0])
                    rst.append(name[0])
                else:
                    rst.append('누구예요?')
                buzzer_call()
                time.sleep(0.1)
    except Exception as e:
        print("error", e)
        return abort(500)

    return jsonify({'ps': rst})

# 새로운 카드등록시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/newcard', methods=['GET'])
def endpoint_rfid_read():
    try:
        rfid_uid = ""
        uid = 0
        rst = rfid_read()
        if rst[0] != "not support the platform.":
            db = get_conn()
            if rst[1] != None:
                rfid_uid = rst[1]
                # rfid_uid가 user_mh테이블에 있는지 확인하는 함수
                if is_rfid_sj(db, rfid_uid)['cnt'] == 0:
                    # 새로운 카드 등록시 세종시립도서관은 7번의 db 번호로 강제정의
                    add_newcard(db, rfid_uid, '이름없음', 7)
                    time.sleep(1)
                    buzzer_call()
                    # DB에 접속해서 배정된 카드번호 표시
                else:
                    uid = get_rfid_sj(db, rfid_uid)['id']
                    # 이미카드가 있는 경우
                    rfid_write(str(uid))
                    # print("uid write %d", uid)
                    rfid_uid = 00000
                    buzzer_call()
                    time.sleep(1)
    except Exception as e:
        print("error", e)
        return abort(500)
    return jsonify({'ps': rfid_uid, 'uid': uid})


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
    # file_log(error)
    # todo : 에러시 관리자 연락하거나 노티가게
    return render_template('index.html'), 500


@application.errorhandler(404)
def page_not_found(error):
    # file_log(error)
    # todo : 페이지 안내
    return render_template('index.html'), 404


def ensure_dir_exists(dir_path, recursive=False):
    if not os.path.isdir(dir_path):
        if recursive:
            os.makedirs(dir_path)
        else:
            os.mkdir(dir_path)


if __name__ == "__main__":
    application.run(host="0.0.0.0")
