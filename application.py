# -*- coding:utf-8 -*-
import os
import shutil
import hashlib
import time

from flask import Flask, render_template, jsonify, abort, request, redirect, session, url_for

from moya.driver_rpi import rfid_read, rfid_write, buzzer_call
from moya.driver_db import init_connect_db, get_attendance, set_attendance, set_exit, get_userinfo, get_userlist, \
    set_signup, is_rfid, add_newcard

from flask.logging import default_handler

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

application = Flask(__name__)

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


# global blocking
# blocking = False

# 관리자 메인 페이지 (기획에 없음)
@application.route('/')
def index():
    # print(application.env)
    return render_template('index.html', platform="")


# YouTube embedded page
@application.route('/intro')
def intro():
    # print(application.env)
    return render_template('intro.html', platform="")


# YouTube embedded page for small library
@application.route('/intro-s')
def intro2():
    # print(application.env)
    return render_template('intro-s.html', platform="")


# 입장시 RFID카드를 인식하는 페이지
@application.route('/entry')
def entry():
    try:
        # print(application.env)
        # global blocking
        # blocking = False
        return render_template('entry.html', msg="카드를 올려 놓으세요!", platform="입장")
    except Exception as e:
        return str(e)


@application.route('/newcard')
def newcard():
    try:
        # print(application.env)
        # global blocking
        # blocking = False
        return render_template('newcard.html', msg="카드를 올려 놓으세요!", platform="카드등록")
    except Exception as e:
        return str(e)


# 관리자 로그인 창
@application.route('/auth', methods=['POST', 'GET'])
def auth():
    try:
        print(application.env)
        if request.method == "POST":
            pp = request.form['pp']

            if (hashlib.sha256(
                    pp.encode()).hexdigest().upper() == 'B6E01168DC7579E745D41638CBDA0D9EAEA5EE9E8DADD1DB250AFCAD9D6B29D2'):
                session['reliquum'] = "active"
                return redirect('./admin')

            return f"""<h1> 비밀번호가 잘못되었습니다. : {pp}</h1>
                    <form method='post' action='./auth'>
                    <input type='password' value='' name='pp' placehold='비밀번호 입력해주세요' /> 
                    <input type='submit' value='login' />
                    </form>
                    """
        else:
            return """<h1> 관리자 비밀번호를 입력해주세요</h1>
                    <form method='post' action='./auth'>
                    <input type='password' value='' name='pp' placehold='비밀번호 입력해주세요' /> 
                    <input type='submit' value='login' />
                    </form>"""
    except Exception as e:
        return str(e)


# 로그인된 관리자 페이지
@application.route('/admin')
def admin():
    print(application.env)
    user = {'name': '관리자'}
    if 'reliquum' in session:
        on_active = session['reliquum']
        return render_template('admin.html', title='관리자', user=user)
    return "권한이 없습니다. <br><a href = '/auth'>" + "로그인 페이지로 가기</a>"


# 현재 사용자를 확인하는 페이지
@application.route('/userlist')
def userlist():
    print(application.env)
    user = {'name': '관리자'}
    db = init_connect_db()
    userlist = []
    for dbuser in get_userlist(db):
        user = {
            'profile': {'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)

    print(userlist)

    if 'reliquum' in session:
        return render_template('userlist.html', title='도서관현황판', user=user, userlist=userlist)

    else:
        return redirect(url_for('auth'))


# 관리자 로그아웃시 index로 이동하는 페이지
@application.route('/logout')
def logout():
    # print(application.env)
    session.pop('reliquum', None)
    return redirect(url_for('index'))


# 회원 신규 등록 페이지
@application.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        rfid = request.form['rfid']
        name = request.form['name']
        age = request.form['age']
        memo = request.form['memo']

        ## 데이타베이스 저장하는 코드
        db = init_connect_db()
        if set_signup(db, rfid, name):
            return f"<h2>저장했습니다. 신규 유져 </h2>"
        else:
            return f"<h2>관리자한테 연락주세요</h2>"

        ## 이상이 없으면 alert 창 뛰우기
        return f"<h2>{age}post 입니다{rfid} </h2>"

    usert = {'name': '관리자'}
    db = init_connect_db()
    userlist = []
    for dbuser in get_userlist(db):
        user = {
            'profile': {'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)

    return render_template('signup.html', title='신규 회원 등록', user=usert, userlist=userlist)


# 퇴장시 RFID카드를 인식하는 페이지
@application.route('/exits')
def exis():
    print(application.env)
    return render_template('exits.html', msg="카드를 올려 놓으세요!", platform="퇴장")


# 퇴장시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/exits', methods=['GET'])
def endpoint_rfid_read_exit():
    try:
        print("rpi buzz test- exit")
        rst = rfid_read()
        print("rfid buzz test-----")
        if rst[0] != "not support this platform.":
            db = init_connect_db()
            if rst[2] != None:
                userid = int(rst[2])
                rfid_uid = rst[1]
                name = get_userinfo(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_exit(db, userid) else "DB FALSE")
                if len(name) > 0:
                    rst.append(name[0])
                else:
                    rst.append('누구예요?')
                buzzer_call()
    except Exception as e:
        print("error", e)
        return abort(500)

    return jsonify({'ps': rst})


# 입장시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/entry', methods=['GET'])
# def endpoint_rfid_read():
def endpoint_rfid_read_entry():
    try:
        print("rpi buzz test")

        rst = rfid_read()
        if rst[0] != "not support this platform.":
            db = init_connect_db()
            if rst[2] != None:
                userid = int(rst[2])
                rfid_uid = rst[1]
                name = get_userinfo(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_attendance(db, userid) else "DB FALSE")
                if len(name) > 0:
                    rst.append(name[0])
                else:
                    rst.append('누구예요?')
                buzzer_call()
    except Exception as e:
        print("error", e)
        return abort(500)

    return jsonify({'ps': rst})


# 새로운 카드등록시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/newcard', methods=['GET'])
def endpoint_rfid_read():
    try:
        print("rpi buzz")
        rfid_uid=""
        rst = rfid_read()
        if rst[0] != "not support the platform.":
            db = init_connect_db()
            if rst[1] != None:
                rfid_uid = rst[1]
                if is_rfid(db, rfid_uid)['cnt'] == 0 :
                    add_newcard(db, rfid_uid, '이름없음')
                    time.sleep( 1 )
                    
                     

    except Exception as e:
        print("error", e)
        return abort(500)
    return jsonify({'ps': rfid_uid})




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
