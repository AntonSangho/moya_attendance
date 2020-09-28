# -*- coding:utf-8 -*-
import os
import shutil
import hashlib
import time
import pandas as pd
import datetime
from flask import Flask, render_template, jsonify, abort, request, redirect, session, url_for, Response
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from wtforms import SelectField
# from wtforms import DateField
from datetime import date

from moya.driver_rpi import rfid_read, rfid_write, buzzer_call
from moya.driver_db import init_connect_db, get_attendance, set_attendance, set_exit, get_userinfo, get_userlist, \
    set_signup, is_rfid, add_newcard, get_rfid, get_dayattendance, get_RangeAttendance, get_userdetail, \
    get_userattendance, set_modify, get_userselectdetail
from sqlalchemy import create_engine

from flask.logging import default_handler

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter


# datepicker에 사용됨
class DateForm(Form):
    dt = DateField('날짜선택', format='%Y-%m-%d')
    dStart = DateField('시작일자', format='%Y-%m-%d')
    dEnd = DateField('종료일자', format='%Y-%m-%d')


# signup신규등록에 사용됨
class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    yob = StringField('yearofbirth', validators=[DataRequired()])


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
                return redirect('./inputdateform')

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


# 로그인된 관리자 페이지 <- 수정예정
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
    # print(application.env)
    user = {'name': '관리자'}
    db = init_connect_db()
    userlist = []
    get_userdetail(db)
    # return 'f<h1>dd</h1>'
    for dbuser in get_userdetail(db):
        user = {
            'profile': {'id': dbuser['id'],
                        'name': dbuser['name'],
                        'rfid': dbuser['rfid'],
                        'sex': dbuser['sex'],
                        'phone': dbuser['phone'],
                        'year': dbuser['year'],
                        'memo': dbuser['memo']
                        },
            'status': '입장중',
            'is': True
        }
        userlist.append(user)

    # print(userlist)

    if 'reliquum' in session:
        return render_template('userlist.html', title='도서관현황판', user=user, userlist=userlist)

    else:
        return redirect(url_for('auth'))


# 사용자를 확인하는 페이지
@application.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'POST':
        selected_name = request.form['name']
        print(selected_name)

        user = {'name': '관리자'}
        db = init_connect_db()
        userlist = []
        for dbuser in get_userattendance(db, selected_name):
            user = {
                'profile': {'userid': dbuser['userid'],
                            'name': dbuser['name'],
                            'entry': dbuser['entry'],
                            'exits': dbuser['exits'],
                            'used': dbuser['used']
                            }
            }
            userlist.append(user)
        print(user)
        userlist_info = []
        for dbuser in get_userselectdetail(db, selected_name):
            user_info = {
                'info': {
                    'id': dbuser['id'],
                    'sex': dbuser['sex'],
                    'phone': dbuser['phone'],
                    'year': dbuser['year'],
                    'memo': dbuser['memo']
                }
            }
            userlist_info.append(user_info)
        print(user_info)
        return render_template('userinfo.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)
    else:
        return f"<h1>not selected</h1>"


@application.route('/userinfo/<username>', methods=['POST', 'GET'])
def modify(username):
    user = {'name': '관리자'}
    db = init_connect_db()
    userlist_info = []
    for dbuser in get_userselectdetail(db, username):
        user_info = {
            'info': {
                'id': dbuser['id'],
                'sex': dbuser['sex'],
                'phone': dbuser['phone'],
                'year': dbuser['year'],
                'memo': dbuser['memo']
            }
        }
        userlist_info.append(user_info)
    if request.method == "POST":
        print(username)
        db = init_connect_db()
        year = request.form['year']
        selected_name = username

        if set_modify(db, selected_name, year):
            print('******')
        else:
            print('not modified')
        return render_template('test.html', nickname=username, user=user, user_info=user_info, userlist_info=userlist_info)
    # if request.method == 'POST':
    #     username = request.form['name']
    # try:
    #     return render_template("modify.html", username=username)
    # except Exception as e:
    #     return str(e)

    # if request.method == 'POST':
    #     print('*******xx')
    #     usert = {'name': '관리자'}
    #     db = init_connect_db()
    #     userlist = []
    #     for dbuser in get_userlist(db):
    #         user = {
    #             'profile': {'id': dbuser['id'], 'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
    #             'status': '입장중',
    #             'is': True
    #         }
    #         userlist.append(user)
    # 데이터베이스 수정하는 코
    # if request.method == 'POST':
    #
    #     idrfid = request.form['idrfid']
    #     print(idrfid)
    #     id = idrfid.split("^")[0]
    #     rfid = idrfid.split("^")[1]
    #     name = request.form['name']
    #     year = request.form['year']
    #     sex = request.form['sex']
    #     phone = request.form['phone']
    #     memo = request.form['memo']
    #     print('*************')
    #
    #     ## 데이타베이스 저장하는 코드
    #
    #     db = init_connect_db()
    #     if set_modify(db, id, rfid, name, sex, year, phone, memo):
    #         print('&&&&&&&&&&&')
    #         return f"<h2>회원정보를 수정했습니다.</h2>"
    #     else:
    #         return f"<h2>관리자한테 연락주세요</h2>"
    # return render_template('modify.html', title='회원정보 수정', user=user, userlist=userlist)


@application.route('/update', methods=['GET', 'POST'])
def update(username):
    if request.method == 'POST':
        selected_name = username
        year = request.form['year']
        db = init_connect_db()
        if set_modify(db, selected_name, year):
            return f"<h2>회원정보수정</h2>"
        else:
            return f"<h2>수정안됨</h2>"
    return render_template('userinfo.html', title='검색', user=user, userlist=userlist, user_info=user_info, userlist_info=userlist_info)


# 엑셀파일을 다운로드하는 페이지
@application.route('/download', methods=['GET', 'POST'])
def download():
    form = DateForm()
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        filterdate = year + '-' + month + '-' + day
        print(filterdate)
        if form.validate_on_submit():
            filterdate = form.dt.data.strftime('%Y-%m-%d')
        user = {'name': '관리자'}
        db = init_connect_db()

        df = pd.DataFrame(get_dayattendance(db, filterdate))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")
        return response
    else:
        return "권한이 없습니다. <br><a href = '/auth'>" + "로그인 페이지로 가기</a>"


# 자료받기 원하는 구간을 정하기
@application.route('/daterange', methods=['GET', 'POST'])
def daterange():
    user = {'name': '관리자'}
    form = DateForm()
    if request.method == 'POST':
        StartDate = form.dStart.data.strftime('%Y-%m-%d')
        EndDate = form.dEnd.data.strftime('%Y-%m-%d')
        print(StartDate)
        print(EndDate)
        db = init_connect_db()
        df = pd.DataFrame(get_RangeAttendance(db, StartDate, EndDate))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")
        return response
    return render_template('/daterange.html', user=user, title='관리자', form=form)


# 날짜를 입력해서 날짜에 해당하는 테이블을 불러오는 페이지
@application.route('/inputdateform', methods=['GET', 'POST'])
def inputdateform():
    form = DateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filterdate = form.dt.data.strftime('%Y-%m-%d')
        else:
            return redirect('/inputdateform')
        user = {'name': '관리자'}
        db = init_connect_db()
        userlist = []
        for dbuser in get_dayattendance(db, filterdate):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)
            print(user)
        return render_template('daylist.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)
        # return '''<h1>{}</h1>'''.format(filterdate)
    else:
        today = datetime.datetime.today()
        print(today)
        user = {'name': '관리자'}
        db = init_connect_db()
        userlist = []
        for dbuser in get_dayattendance(db, today):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)
            print(user)
        return render_template('todaytable.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)


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

        idrfid = request.form['idrfid']
        print(idrfid)
        id = idrfid.split("^")[0]
        rfid = idrfid.split("^")[1]
        name = request.form['name']
        year = request.form['year']
        sex = request.form['sex']
        phone = request.form['phone']
        memo = request.form['memo']
        print('*************')

        ## 데이타베이스 저장하는 코드

        db = init_connect_db()
        if set_signup(db, id, rfid, name, sex, year, phone, memo):
            print('&&&&&&&&&&&')
            return f"<h2>새로운 회원을 등록했습니다.</h2>"
        else:
            return f"<h2>관리자한테 연락주세요</h2>"

        ## 이상이 없으면 alert 창 뛰우기
        return f"<h2>{age}post 입니다{rfid} </h2>"

    usert = {'name': '관리자'}
    db = init_connect_db()
    userlist = []
    for dbuser in get_userlist(db):
        user = {
            'profile': {'id': dbuser['id'], 'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)

    return render_template('signup.html', title='신규 회원 등록', user=user, userlist=userlist)


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
                print("*****************1")
                userid = rst[2]
                rfid_uid = rst[1]
                print("*****************2")
                name = get_userinfo(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_attendance(db, userid) else "DB FALSE")

                print("*****************3")
                if len(name) > 0:
                    rst.append(name[0])
                else:
                    rst.append('누구예요?')
    except Exception as e:
        print("error", e)
        return abort(500)

    return jsonify({'ps': rst})


# 새로운 카드등록시 RFID카드와 DB 대조작업
@application.route('/api/v1.0/newcard', methods=['GET'])
def endpoint_rfid_read():
    try:
        print("rpi buzz")
        rfid_uid = ""
        uid = 0
        rst = rfid_read()
        if rst[0] != "not support the platform.":
            db = init_connect_db()
            if rst[1] != None:
                rfid_uid = rst[1]

                if is_rfid(db, rfid_uid)['cnt'] == 0:
                    add_newcard(db, rfid_uid, '이름없음')
                    time.sleep(1)
                    # DB에 접속해서 배정된 카드번호 표시
                else:
                    uid = get_rfid(db, rfid_uid)['id']
                    # 이미카드가 있는 경우
                    rfid_write(str(uid))
                    print("uid write %d", uid)
                    rfid_uid = 00000

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
