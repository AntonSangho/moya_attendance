import pymysql
import pymysql.cursors
import os

# 데이타베이스 초기화 정보

sqlmapper = {
    # sqltype_connectionUserNum
    "sql_1_admin1": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    "sql_1_admin2": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    "sql_1_admin3": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    "sql_2_admin1": """SELECT a.id, a.name , b.* FROM users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_2_admin2": """SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin1": "INSERT INTO users(rfid_uid, `name`) VALUES",
    "sql_3_admin2": "INSERT INTO mh_users(rfid_uid, `name`) VALUES",
    "sql_4_admin1": "INSERT INTO mh_users(rfid_uid, `name`) VALUES"

}


def init_connect_db(switch_db):
    if switch_db == 1:
        db = pymysql.connect(
            # if app.env =='development':
            # user=os.getenv('DB_USER'),
            # passwd=os.getenv('DB_PASSWORD'), #beanstalk 환경변수 이용
            # db=os.getenv('DB_NAME'), #beanstalk 환경변수 이용
            # host=os.getenv('DB_HOST'), #beanstalk 환경변수 이용
            # charset='utf8', #beanstalk 환경변수 이용
            user='righthand',
            passwd='moya_0526',  # beanstalk 환경변수 이용
            db='moya',  # beanstalk 환경변수 이용
            host='moy.cismqc0tinee.ap-northeast-2.rds.amazonaws.com',  # beanstalk 환경변수 이용
            charset='utf8',  # beanstalk 환경변수 이용
            cursorclass=pymysql.cursors.DictCursor

        )

        print("1 번 유저로 로그인")
        return db

    db = pymysql.connect(
        # if app.env =='development':
        # user=os.getenv('DB_USER'),
        # passwd=os.getenv('DB_PASSWORD'), #beanstalk 환경변수 이용
        # db=os.getenv('DB_NAME'), #beanstalk 환경변수 이용
        # host=os.getenv('DB_HOST'), #beanstalk 환경변수 이용
        # charset='utf8', #beanstalk 환경변수 이용
        user='righthand_01',
        passwd='1cl1kc02,!c',  # beanstalk 환경변수 이용
        db='moya',  # beanstalk 환경변수 이용
        host='moy.cismqc0tinee.ap-northeast-2.rds.amazonaws.com',  # beanstalk 환경변수 이용
        charset='utf8',  # beanstalk 환경변수 이용
        cursorclass=pymysql.cursors.DictCursor
    )

    print("righthand_01 번 유저로 로그인")
    return db


# rfid 태그값 가져오기
def get_attendance(db, conn):
    try:
        cursor = db.cursor()
        cursor.execute(sqlmapper["sql_1_admin1"] if conn == 1 else sqlmapper["sql_1_admin" + conn])

        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_dayattendance(db, filter_date):
    try:
        cursor = db.cursor()
        print(filter_date)

        cursor.execute(
            f"""{sqlmapper["sql_2_admin1"]}='{filter_date}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_dayattendance_mh(db, filter_date):
    try:
        cursor = db.cursor()
        print('get_dayattendance_mh')
        print(filter_date)
        print('filterdate')

        cursor.execute(
            f"""{sqlmapper["sql_2_admin2"]}='{filter_date}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_RangeAttendance(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        print()

        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_RangeAttendance_mh(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        print()

        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userattendance(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where a.name ='{selected_name}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userattendance_mh(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where a.name ='{selected_name}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userinfo(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        # print("$$$$$$$$")
        # print(userid, rfid_uid)
        cursor.execute(f"SELECT name FROM users WHERE id = {userid} and rfid_uid = {rfid_uid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userinfo_mh(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        # print("$$$$$$$$")
        # print(userid, rfid_uid)
        cursor.execute(f"SELECT name FROM mh_users WHERE id = {userid} and rfid_uid = {rfid_uid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def is_rfid(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def is_rfid_mh(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from mh_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_rfid(db, rfid_uid):
    try:
        cursor = db.cursor()
        print("**************" + str(rfid_uid))
        cursor.execute(f"select id from users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_rfid_mh(db, rfid_uid):
    try:
        cursor = db.cursor()
        print("**************" + str(rfid_uid))
        cursor.execute(f"select id from mh_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userlist(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        # 이렇게 하면 나중에 돈 많이나옴.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_adduserlist(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"select users.id, users.name, users.rfid_uid from users where not exists(select users_detail.id from users_detail where users.id = users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0


# 마하도서관
def get_adduserlist_mh(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userdetail(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users_detail")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userdetail_mh(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM mh_users_detail")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userselectdetail(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userselectdetail_mh(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def set_modify(db, selected_name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE users_detail SET sex='{sex}', year={year}, phone={phone}, memo='{memo}' where name ='{selected_name}' ;")
        # print("1_1 - set_modify try")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        # print("1_2 - set_modify exception")
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1


def set_signup(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update users set name='{name}' where rfid_uid ='{rfid}';"
        cursor.execute(sql_2)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1


def set_signup_mh(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into mh_users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update mh_users set name='{name}' where rfid_uid ='{rfid}';"
        cursor.execute(sql_2)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1


## rfid 태깅기록
# 제천도서관 입장기록
def set_attendance(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO attendance(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        db.commit()
        db.close()
        return 1


# 마하도서관 입장기록
def set_attendance_mh(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO mh_attendance(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        db.commit()
        db.close()
        return 1


## rfid 태깅기록
# 제천도서관 퇴장기록
def set_exit(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO exits(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        raise
    else:
        db.commit()
        db.close()
        return 1


# 마하도서관 퇴장기록
def set_exit_mh(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO mh_exits(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        raise
    else:
        db.commit()
        db.close()
        return 1


## rfid 카드등록
# 도서관 카드등록
def add_newcard(db, rfid_uid, name, conn):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"{sqlmapper['sql_3_admin1'] if conn == 1 else sqlmapper['sql_3_admin' + str(conn)]}  ('{rfid_uid}','{name}')")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1
