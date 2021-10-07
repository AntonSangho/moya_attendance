# -*- coding:utf-8 -*-
import os
import shutil
import hashlib
import time
import pandas as pd
import datetime
from flask import Flask, render_template, jsonify, abort, request, redirect, session, url_for, Response, make_response
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from wtforms import SelectField
# from wtforms import DateField
from datetime import date

from moya.driver_rpi import rfid_read, rfid_write, buzzer_call
from moya.driver_db import init_connect_db, get_attendance, set_attendance, set_attendance_mh, set_exit, set_exit_mh, \
    get_userinfo, get_userinfo_mh, \
    set_signup, set_signup_mh, is_rfid, is_rfid_mh, add_newcard, get_rfid, get_rfid_mh, get_dayattendance, \
    get_RangeAttendance, \
    get_RangeAttendance_mh, get_userdetail, get_userdetail_mh, \
    get_userattendance, get_userattendance_mh, set_modify, set_modify_mh, get_userselectdetail, get_userselectdetail_mh, \
    get_adduserlist, get_adduserlist_mh, get_dayattendance_mh, \
    get_dayattendance_sw, get_RangeAttendance_sw, get_userattendance_sw, get_userinfo_sw, is_rfid_sw, get_rfid_sw, \
    get_adduserlist_sw, get_userdetail_sw, get_userselectdetail_sw, set_modify_sw, set_signup_sw, set_attendance_sw, \
    set_exit_sw

from sqlalchemy import create_engine

from flask.logging import default_handler

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

db = init_connect_db(2)


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


# 로그인 페이지
@application.route('/', methods=['POST', 'GET'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pp = request.form['pp']
        try:
            if (hashlib.sha256(
                    pp.encode()).hexdigest().upper() == 'B6E01168DC7579E745D41638CBDA0D9EAEA5EE9E8DADD1DB250AFCAD9D6B29D2'):
                session['reliquum'] = "active"
                db = init_connect_db(1);
                res = make_response(redirect('./inputdateform'))
                res.set_cookie('conn', '1', max_age=60 * 60 * 24 * 365 * 2)
                return res

            # lib2password
            if (hashlib.sha256(
                    pp.encode()).hexdigest().upper() == "ac4624660c6bd995ae624f978cd85865e3e6aa40db3a95bbf119780f03080671".upper()):
                session['reliquum'] = "active"
                db = init_connect_db(2);

                res = make_response(redirect('./mh/inputdateform'))
                res.set_cookie('conn', '2', max_age=60 * 60 * 24 * 365 * 2)
                return res

            # adminmoya
            if (hashlib.sha256(
                    pp.encode()).hexdigest().upper() == '203D45443356D2BB30B4A2D6C0119F18A8B54E9E686D6D17FF636D85112E8351'):
                session['reliquum'] = "active"
                db = init_connect_db(3);
                res = make_response(redirect('./adminmoya'))
                res.set_cookie('conn', '3', max_age=60 * 60 * 24 * 365 * 2)
                return res

            # suwon1
            if (hashlib.sha256(
                    pp.encode()).hexdigest().upper() == 'AB42590B4070E9B6C79B1E650C464FBCC7834E1BA7871F0B2E935B28F58A6856'):
                session['reliquum'] = "active"
                db = init_connect_db(4);
                res = make_response(redirect('./sw/inputdateform'))
                res.set_cookie('conn', '4', max_age=60 * 60 * 24 * 365 * 2)
                return res
            else:
                return render_template('login_error.html')
        except:
            return render_template('login.html')


@application.route('/webapp')
def index():
    # print(application.env)
    return render_template('webapp.html', platform="진주마하어린이도서관")


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


# 총괄 관리자 페이지
@application.route('/admin')
def admin():
    print(application.env)
    user = {'name': '관리자'}
    print('admin')
    if 'reliquum' in session:
        on_active = session['reliquum']
        return render_template('admin.html', title='관리자', user=user)
    return "권한이 없습니다. <br><a href = '/auth'>" + "로그인 페이지로 가기</a>"


# adminmoya관리 페이지
@application.route('/adminmoya')
def adminmoya():
    print(application.env)
    user = {'name': '관리자'}
    print('admin')
    if 'reliquum' in session:
        on_active = session['reliquum']
        return render_template('adminmoya.html', title='관리자', user=user)
    return "권한이 없습니다. <br><a href = '/auth'>" + "로그인 페이지로 가기</a>"

# 현재 사용자를 확인하는 페이지
@application.route('/userlist', methods=['GET', 'POST'])
def userlist():
    # print(application.env)
    user = {'name': '관리자'}
    userlist = []
    db = get_conn()
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
    print(request.method)
    if request.method == 'POST':
        df = pd.DataFrame(get_userdetail(db))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="userlist.csv")
        return response
    if 'reliquum' in session:
        return render_template('userlist.html', title='도서관현황판', user=user, userlist=userlist)
    else:
        return redirect(url_for('auth'))


# [마하도서관] 현재 사용자를 확인하는 페이지
@application.route('/mh/userlist', methods=['GET', 'POST'])
def userlist_mh():
    # print(application.env)
    user = {'name': '관리자'}
    userlist = []
    db = get_conn()
    get_userdetail(db)
    # return 'f<h1>dd</h1>'
    for dbuser in get_userdetail_mh(db):
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
    print(request.method)
    if request.method == 'POST':
        df = pd.DataFrame(get_userdetail(db))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="userlist.csv")
        return response
    if 'reliquum' in session:
        return render_template('userlist_mh.html', title='도서관현황판', user=user, userlist=userlist)

    else:
        return redirect(url_for('mh/auth'))


# [바른샘도서관] 현재 사용자를 확인하는 페이지
@application.route('/sw/userlist', methods=['GET', 'POST'])
def userlist_sw():
    # print(application.env)
    user = {'name': '관리자'}
    userlist = []
    db = get_conn()
    get_userdetail(db)
    # return 'f<h1>dd</h1>'
    for dbuser in get_userdetail_sw(db):
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
    print(request.method)
    if request.method == 'POST':
        df = pd.DataFrame(get_userdetail_sw(db))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="userlist.csv")
        return response
    if 'reliquum' in session:
        return render_template('userlist_sw.html', title='도서관현황판', user=user, userlist=userlist)

    else:
        return redirect(url_for('sw/auth'))


# 사용자를 확인하는 페이지
@application.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'GET':
        abort(403, '잘못된 접근입니다.')
    # print("######" + str(request.form))
    if request.method == 'POST':
        selected_name = request.form['name']
        user = {'name': '관리자'}
        # db = init_connect_db()
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
        # print(user)
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
        # print(user_info)
        # print('****' + selected_name)
        # print(userlist)
        # print(userlist_info)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 기록이 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('userinfo.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)

    else:
        return f"<h1>not selected</h1>"


# [마하도서관] 사용자를 확인하는 페이지
@application.route('/mh/userinfo', methods=['GET', 'POST'])
def userinfo_mh():
    if request.method == 'GET':
        abort(403, '잘못된 접근입니다.')
    # print("######" + str(request.form))
    if request.method == 'POST':
        selected_name = request.form['name']
        user = {'name': '관리자'}
        # db = init_connect_db()
        db = get_conn()
        userlist = []
        for dbuser in get_userattendance_mh(db, selected_name):
            user = {
                'profile': {'userid': dbuser['userid'],
                            'name': dbuser['name'],
                            'entry': dbuser['entry'],
                            'exits': dbuser['exits'],
                            'used': dbuser['used']
                            }
            }
            userlist.append(user)
        # print(user)
        userlist_info = []
        for dbuser in get_userselectdetail_mh(db, selected_name):
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
        # print(user_info)
        # print('****' + selected_name)
        # print(userlist)
        # print(userlist_info)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 기록이 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('userinfo_mh.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)

    else:
        return f"<h1>not selected</h1>"


# [바른샘도서관] 사용자를 확인하는 페이지
@application.route('/sw/userinfo', methods=['GET', 'POST'])
def userinfo_sw():
    if request.method == 'GET':
        abort(403, '잘못된 접근입니다.')
    # print("######" + str(request.form))
    if request.method == 'POST':
        selected_name = request.form['name']
        user = {'name': '관리자'}
        # db = init_connect_db()
        db = get_conn()
        userlist = []
        for dbuser in get_userattendance_sw(db, selected_name):
            user = {
                'profile': {'userid': dbuser['userid'],
                            'name': dbuser['name'],
                            'entry': dbuser['entry'],
                            'exits': dbuser['exits'],
                            'used': dbuser['used']
                            }
            }
            userlist.append(user)
        # print(user)
        userlist_info = []
        for dbuser in get_userselectdetail_sw(db, selected_name):
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
        # print(user_info)
        # print('****' + selected_name)
        # print(userlist)
        # print(userlist_info)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 기록이 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('userinfo_sw.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)

    else:
        return f"<h1>not selected</h1>"


# @application.route('/userinfo/userinfo/<username>', methods=['POST', 'GET'])
# def fixed_url(username):
#     return redirect('/userinfo/'+username)
@application.route('/view/<username>', methods=['POST', 'GET'])
def aftermodify(username):
    # print('270#########' + username)
    if request.method == 'GET':
        selected_name = username
        # print(selected_name)

        user = {'name': '관리자'}
        # db = init_connect_db()
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
        # print(user)
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
        # print(user_info)
        print(selected_name)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 아직 개인정보가 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('afteruserinfo.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)


## [마하도서관] 사용자이름 선택시 정보 확인
@application.route('/mh/view/<username>', methods=['POST', 'GET'])
def aftermodify_mh(username):
    # print('270#########' + username)
    if request.method == 'GET':
        selected_name = username
        # print(selected_name)

        user = {'name': '관리자'}
        # db = init_connect_db()
        db = get_conn()
        userlist = []
        for dbuser in get_userattendance_mh(db, selected_name):
            user = {
                'profile': {'userid': dbuser['userid'],
                            'name': dbuser['name'],
                            'entry': dbuser['entry'],
                            'exits': dbuser['exits'],
                            'used': dbuser['used']
                            }
            }
            userlist.append(user)
        print(userlist)
        userlist_info = []
        for dbuser in get_userselectdetail_mh(db, selected_name):
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
        print(selected_name)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 아직 개인정보가 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('afteruserinfo_mh.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)


## [바른샘도서관] 사용자이름 선택시 정보 확인
@application.route('/sw/view/<username>', methods=['POST', 'GET'])
def aftermodify_sw(username):
    # print('270#########' + username)
    if request.method == 'GET':
        selected_name = username
        # print(selected_name)

        user = {'name': '관리자'}
        # db = init_connect_db()
        db = get_conn()
        userlist = []
        for dbuser in get_userattendance_sw(db, selected_name):
            user = {
                'profile': {'userid': dbuser['userid'],
                            'name': dbuser['name'],
                            'entry': dbuser['entry'],
                            'exits': dbuser['exits'],
                            'used': dbuser['used']
                            }
            }
            userlist.append(user)
        print(userlist)
        userlist_info = []
        for dbuser in get_userselectdetail_sw(db, selected_name):
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
        print(selected_name)
        if len(userlist_info) == 0:
            return """<h2>해당사용자는 아직 개인정보가 없습니다.</h2>
                        <script>
                        setTimeout(function(){
                            history.back()
                        }, 3000);
                        </script>"""
        return render_template('afteruserinfo_sw.html', title='검색', user=user, userlist=userlist, user_info=user_info,
                               userlist_info=userlist_info)


## 수정하는 기능
@application.route('/userinfo/<username>', methods=['POST', 'GET'])
def modify(username):
    user = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
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
        # print(user_info)
    if request.method == "POST":
        # print('1 - request POST')
        # db = init_connect_db()
        year = request.form.get('year')
        phone = request.form.get('phone')
        memo = request.form.get('memo')
        sex = request.form.get('sex')
        selected_name = username
        if set_modify(db, selected_name, sex, year, phone, memo):
            return redirect(url_for('aftermodify', username=selected_name))
        return render_template('update.html', username=username, user=user, user_info=user_info,
                               userlist_info=userlist_info)


## [마하도서관] 수정하는 기능
@application.route('/mh/userinfo/<username>', methods=['POST', 'GET'])
def modify_mh(username):
    user = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
    userlist_info = []
    for dbuser in get_userselectdetail_mh(db, username):
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
        # print(user_info)
    if request.method == "POST":
        # print('1 - request POST')
        # db = init_connect_db()
        year = request.form.get('year')
        phone = request.form.get('phone')
        memo = request.form.get('memo')
        sex = request.form.get('sex')
        selected_name = username
        if set_modify_mh(db, selected_name, sex, year, phone, memo):
            return redirect(url_for('aftermodify_mh', username=selected_name))
        return render_template('update_mh.html', username=username, user=user, user_info=user_info,
                               userlist_info=userlist_info)


## [바른샘도서관] 수정하는 기능
@application.route('/sw/userinfo/<username>', methods=['POST', 'GET'])
def modify_sw(username):
    user = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
    userlist_info = []
    for dbuser in get_userselectdetail_sw(db, username):
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
        # print(user_info)
    if request.method == "POST":
        # print('1 - request POST')
        # db = init_connect_db()
        year = request.form.get('year')
        phone = request.form.get('phone')
        memo = request.form.get('memo')
        sex = request.form.get('sex')
        selected_name = username
        if set_modify_sw(db, selected_name, sex, year, phone, memo):
            return redirect(url_for('aftermodify_sw', username=selected_name))
        return render_template('update_sw.html', username=username, user=user, user_info=user_info,
                               userlist_info=userlist_info)


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
        # db = init_connect_db()
        df = pd.DataFrame(get_RangeAttendance(db, StartDate, EndDate))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")
        return response
    return render_template('/daterange.html', user=user, title='관리자', form=form)


# [마하도서관] 자료받기 원하는 구간을 정하기
@application.route('/mh/daterange', methods=['GET', 'POST'])
def daterange_mh():
    user = {'name': '관리자'}
    form = DateForm()
    if request.method == 'POST':
        StartDate = form.dStart.data.strftime('%Y-%m-%d')
        EndDate = form.dEnd.data.strftime('%Y-%m-%d')
        print(StartDate)
        print(EndDate)
        # db = init_connect_db()
        df = pd.DataFrame(get_RangeAttendance_mh(db, StartDate, EndDate))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")
        return response
    return render_template('daterange_mh.html', user=user, title='관리자', form=form)


# [바른샘도서관] 자료받기 원하는 구간을 정하기
@application.route('/sw/daterange', methods=['GET', 'POST'])
def daterange_sw():
    user = {'name': '관리자'}
    form = DateForm()
    if request.method == 'POST':
        StartDate = form.dStart.data.strftime('%Y-%m-%d')
        EndDate = form.dEnd.data.strftime('%Y-%m-%d')
        print(StartDate)
        print(EndDate)
        # db = init_connect_db()
        df = pd.DataFrame(get_RangeAttendance_sw(db, StartDate, EndDate))
        csv_data = df.to_csv(index='false', encoding='utf-8')
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")
        return response
    return render_template('daterange_sw.html', user=user, title='관리자', form=form)


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
        db = get_conn()
        userlist = []
        print(filterdate)
        for dbuser in get_dayattendance(db, filterdate):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)

        print('###379' + str(userlist))
        if len(userlist) == 0:
            return """<h2>해당날짜에는 기록이 없습니다.</h2>
            <script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""

        return render_template('daylist.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)
        # return '''<h1>{}</h1>'''.format(filterdate)
    else:
        today = datetime.date.today()
        print(today)
        user = {'name': '관리자'}
        db = get_conn()
        userlist = []
        for dbuser in get_dayattendance(db, today):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)
            print(user)
        return render_template('todaytable.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)


# [마하도서관] 날짜를 입력해서 날짜에 해당하는 테이블을 불러오는 페이지
@application.route('/mh/inputdateform', methods=['GET', 'POST'])
def inputdateform_mh():
    form = DateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filterdate = form.dt.data.strftime('%Y-%m-%d')
        else:
            return redirect('/mh/inputdateform')
        user = {'name': '관리자'}
        db = get_conn()
        userlist = []
        print(filterdate)
        for dbuser in get_dayattendance_mh(db, filterdate):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)

        print('mh_attendace' + str(userlist))
        if len(userlist) == 0:
            return """<h2>해당날짜에는 기록이 없습니다.</h2>
            <script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""

        return render_template('daylist_mh.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)
        # return '''<h1>{}</h1>'''.format(filterdate)
    else:
        today = datetime.date.today()
        print(today)
        user = {'name': '관리자'}
        db = get_conn()
        userlist = []
        for dbuser in get_dayattendance_mh(db, today):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)
            print(user)
        return render_template('todaytable_mh.html', user=user, userlist=userlist, title='도서관현황판', platform="",
                               form=form)


# [바른샘도서관] 날짜를 입력해서 날짜에 해당하는 테이블을 불러오는 페이지
@application.route('/sw/inputdateform', methods=['GET', 'POST'])
def inputdateform_sw():
    form = DateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filterdate = form.dt.data.strftime('%Y-%m-%d')
        else:
            return redirect('/sw/inputdateform')
        user = {'name': '관리자'}
        db = get_conn()
        userlist = []
        print(filterdate)
        for dbuser in get_dayattendance_sw(db, filterdate):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)

        print('sw_attendace' + str(userlist))
        if len(userlist) == 0:
            return """<h2>해당날짜에는 기록이 없습니다.</h2>
            <script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""

        return render_template('daylist_sw.html', user=user, userlist=userlist, title='도서관현황판', platform="", form=form)
        # return '''<h1>{}</h1>'''.format(filterdate)
    else:
        today = datetime.date.today()
        print(today)
        user = {'name': '관리자'}
        db = get_conn()
        userlist = []
        for dbuser in get_dayattendance_sw(db, today):
            user = {
                'profile': {'userid': dbuser['userid'], 'name': dbuser['name'], 'entry': dbuser['entry'],
                            'exits': dbuser['exits'], 'used': dbuser['used']}
            }
            userlist.append(user)
            print(user)
        return render_template('todaytable_sw.html', user=user, userlist=userlist, title='도서관현황판', platform="",
                               form=form)


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
        id = idrfid.split("^")[0]
        rfid = idrfid.split("^")[1]
        name = request.form['name']
        year = request.form['year']
        sex = request.form['sex']
        phone = request.form['phone']
        memo = request.form['memo']

        ## 데이타베이스 저장하는 코드

        # db = init_connect_db()
        if set_signup(db, id, rfid, name, sex, year, phone, memo):
            return """<h2>새로운 회원을 등록했습니다.</h2><script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""
        else:
            return f"<h2>관리자한테 연락주세요</h2>"  # 이미등록된 카드일 경우 알려줄 필요가 있음.

        ## 이상이 없으면 alert 창 뛰우기
        return f"<h2>{age}post 입니다{rfid} </h2>"

    usert = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
    userlist = []
    for dbuser in get_adduserlist(db):
        user = {
            'profile': {'id': dbuser['id'], 'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)
    return render_template('signup.html', title='신규 회원 등록', len=len(userlist), user=user, userlist=userlist)


# [마하도서관] 회원 신규 등록 페이지
@application.route('/mh/signup', methods=['POST', 'GET'])
def signup_mh():
    if request.method == 'POST':

        idrfid = request.form['idrfid']
        id = idrfid.split("^")[0]
        rfid = idrfid.split("^")[1]
        name = request.form['name']
        year = request.form['year']
        sex = request.form['sex']
        phone = request.form['phone']
        memo = request.form['memo']

        ## 데이타베이스 저장하는 코드

        # db = init_connect_db()
        db = get_conn()
        if set_signup_mh(db, id, rfid, name, sex, year, phone, memo):
            return """<h2>새로운 회원을 등록했습니다.</h2><script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""
        else:
            return f"<h2>관리자한테 연락주세요</h2>"  # 이미등록된 카드일 경우 알려줄 필요가 있음.

        ## 이상이 없으면 alert 창 뛰우기
        return f"<h2>{age}post 입니다{rfid} </h2>"

    usert = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
    userlist = []
    for dbuser in get_adduserlist_mh(db):
        user = {
            'profile': {'id': dbuser['id'], 'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)
    return render_template('signup_mh.html', title='신규 회원 등록', len=len(userlist), user=user, userlist=userlist)


# [바른샘도서관] 회원 신규 등록 페이지
@application.route('/sw/signup', methods=['POST', 'GET'])
def signup_sw():
    if request.method == 'POST':

        idrfid = request.form['idrfid']
        id = idrfid.split("^")[0]
        rfid = idrfid.split("^")[1]
        name = request.form['name']
        year = request.form['year']
        sex = request.form['sex']
        phone = request.form['phone']
        memo = request.form['memo']

        ## 데이타베이스 저장하는 코드

        # db = init_connect_db()
        db = get_conn()
        if set_signup_sw(db, id, rfid, name, sex, year, phone, memo):
            return """<h2>새로운 회원을 등록했습니다.</h2><script>
            setTimeout(function(){
                history.back()
            }, 3000);
            </script>"""
        else:
            return f"<h2>관리자한테 연락주세요</h2>"  # 이미등록된 카드일 경우 알려줄 필요가 있음.

        ## 이상이 없으면 alert 창 뛰우기
        return f"<h2>{age}post 입니다{rfid} </h2>"

    usert = {'name': '관리자'}
    # db = init_connect_db()
    db = get_conn()
    userlist = []
    for dbuser in get_adduserlist_sw(db):
        user = {
            'profile': {'id': dbuser['id'], 'name': dbuser['name'], 'rfid': dbuser['rfid_uid']},
            'status': '입장중',
            'is': True
        }
        userlist.append(user)
    return render_template('signup_sw.html', title='신규 회원 등록', len=len(userlist), user=user, userlist=userlist)


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
                name = get_userinfo_mh(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_exit_mh(db, userid) else "DB FALSE")
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
                name = get_userinfo_mh(db, userid, rfid_uid)
                rst.append("DB TRUE" if set_attendance_mh(db, userid) else "DB FALSE")
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
        rfid_uid = ""
        uid = 0
        rst = rfid_read()
        if rst[0] != "not support the platform.":
            db = get_conn()
            if rst[1] != None:
                rfid_uid = rst[1]
                # rfid_uid가 user_mh테이블에 있는지 확인하는 함수
                if is_rfid_mh(db, rfid_uid)['cnt'] == 0:
                    # 새로운 카드 등록시 마하도서관은 2번의 db 번호로 강제정의
                    add_newcard(db, rfid_uid, '이름없음', 2)
                    time.sleep(1)
                    buzzer_call()
                    # DB에 접속해서 배정된 카드번호 표시
                else:
                    uid = get_rfid_mh(db, rfid_uid)['id']
                    # 이미카드가 있는 경우
                    rfid_write(str(uid))
                    print("uid write %d", uid)
                    rfid_uid = 00000
                    buzzer_call()
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
