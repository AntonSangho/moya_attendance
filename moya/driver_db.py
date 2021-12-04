import pymysql
import pymysql.cursors
import os

# 데이타베이스 초기화 정보

sqlmapper = {
    # sqltype_connectionUserNum
    # 제천기적의도서관
    "sql_2_admin1": """SELECT a.id, a.name , b.* FROM users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin1": "INSERT INTO users(rfid_uid, `name`) VALUES",
    "sql_5_admin1": "SELECT * FROM users_detail",
    "sql_6_admin1": "select users.id, users.name, users.rfid_uid from users where not exists(select users_detail.id from users_detail where users.id = users_detail.id);",
    "sql_7_admin1": "SELECT * FROM users_detail where name = %s",
    "sql_8_admin1": """
            SELECT a.id, a.name , b.* FROM users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s""",

    # 진주마하도서관
    "sql_2_admin2": """SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin2": "INSERT INTO mh_users(rfid_uid, `name`) VALUES",
    "sql_5_admin2": "SELECT * FROM mh_users_detail",
    "sql_6_admin2": "select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);",
    "sql_7_admin2": "SELECT * FROM mh_users_detail where name = %s",
    "sql_8_admin2": """
            SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s""",

    # 수원바른샘도서
    "sql_2_admin3": """SELECT a.id, a.name , b.* FROM sw_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM sw_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin4": "INSERT INTO sw_users(rfid_uid, `name`) VALUES",
    "sql_5_admin3": "SELECT * FROM sw_users_detail",
    "sql_6_admin3": "select sw_users.id, sw_users.name, sw_users.rfid_uid from moya.sw_users where not exists(select sw_users_detail.id from sw_users_detail where sw_users.id = sw_users_detail.id);",
    "sql_7_admin3": "SELECT * FROM sw_users_detail where name = %s",
    "sql_8_admin3": """
            SELECT a.id, a.name , b.* FROM sw_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM sw_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s""",
    
    # 개발용
    "sql_2_admin4": """SELECT a.id, a.name , b.* FROM dev_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin5": "INSERT INTO dev_users(rfid_uid, `name`) VALUES",
    "sql_5_admin4": "SELECT * FROM dev_users_detail",
    "sql_6_admin4": "select dev_users.id, dev_users.name, dev_users.rfid_uid from moya.dev_users where not exists(select dev_users_detail.id from dev_users_detail where dev_users.id = dev_users_detail.id);",
    "sql_7_admin4": "SELECT * FROM dev_users_detail where name = %s",
    "sql_8_admin4": """
            SELECT a.id, a.name , b.* FROM dev_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s""",
            

    # 미정
    # "sql_1_admin1": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    # "sql_1_admin2": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    # "sql_1_admin3": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
   
    # 반포도서관 
    "sql_2_admin5": """SELECT a.id, a.name , b.* FROM bp_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM bp_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin6": "INSERT INTO bp_users(rfid_uid, `name`) VALUES",
    "sql_5_admin5": "SELECT * FROM bp_users_detail",
    "sql_6_admin5": "select bp_users.id, bp_users.name, bp_users.rfid_uid from moya.bp_users where not exists(select bp_users_detail.id from bp_users_detail where bp_users.id = bp_users_detail.id);",
    "sql_7_admin5": "SELECT * FROM bp_users_detail where name = %s",
    "sql_8_admin5": """
            SELECT a.id, a.name , b.* FROM bp_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM bp_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s""",
    
    # 세종시립도서관 
    "sql_2_admin6": """SELECT a.id, a.name , b.* FROM sj_users a LEFT JOIN 
            (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM sj_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
            b ON a.id = b.userid 
            where b.ent""",
    "sql_3_admin7": "INSERT INTO sj_users(rfid_uid, `name`) VALUES",
    "sql_5_admin6": "SELECT * FROM sj_users_detail",
    "sql_6_admin6": "select sj_users.id, sj_users.name, sj_users.rfid_uid from moya.sj_users where not exists(select sj_users_detail.id from sj_users_detail where sj_users.id = sj_users_detail.id);",
    "sql_7_admin6": "SELECT * FROM sj_users_detail where name = %s",
    "sql_8_admin6": """
            SELECT a.id, a.name , b.* FROM sj_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM sj_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s"""
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


def get_dayattendance_sw(db, filter_date):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_2_admin3"]}='{filter_date}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_dayattendance_test(db, filter_date):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_2_admin4"]}='{filter_date}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_dayattendance_bp(db, filter_date):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_2_admin5"]}='{filter_date}'"""
        )
        # cursor.execute(
        #     f'SELECT userid, substr(entry_time, 1, 10), max(used_time) '
        #     f'from stat_attentance '
        #     f'WHERE substr(entry_time, 1, 10) = \'2020-08-21\' '
        #     f'group by userid, substr(entry_time, 1, 10);')
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_dayattendance_sj(db, filter_date):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_2_admin6"]}='{filter_date}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_RangeAttendance(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT a.id, a.name , b.* FROM users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_RangeAttendance_mh(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_RangeAttendance_sw(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM sw_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM sw_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_RangeAttendance_test(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM dev_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_RangeAttendance_bp(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM bp_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM bp_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_RangeAttendance_sj(db, StartDate, EndDate):
    try:
        cursor = db.cursor()
        cursor.execute(
            f""" 
            SELECT a.id, a.name , b.* FROM sj_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(date_format(entry_time,"%r")) AS entry, MAX(date_format(exit_time,"%r")) AS exits, max(used_time) AS used
            FROM sj_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid 
            where b.ent between '{StartDate}'AND '{EndDate}'"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userattendance(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin1']}", [selected_name])
        # cursor.execute(
        #     f"""
        #     SELECT a.id, a.name , b.* FROM users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
        #     FROM stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
        #     where a.name ='{selected_name}'"""
        # )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userattendance_mh(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin2']}", [selected_name])
        # cursor.execute(
        #     f"""
        #     SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
        #     FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
        #     where a.name ='{selected_name}'"""
        # )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userattendance_sw(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin3']}", [selected_name])
        # cursor.execute(
        #     f"""
        #     SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
        #     FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
        #     where a.name ='{selected_name}'"""
        # )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_userattendance_test(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin4']}", [selected_name])
        # cursor.execute(
        #     f"""
        #     SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
        #     FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
        #     where a.name ='{selected_name}'"""
        # )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_userattendance_bp(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin5']}", [selected_name])
        # cursor.execute(
        #     f"""
        #     SELECT a.id, a.name , b.* FROM mh_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
        #     FROM mh_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
        #     where a.name ='{selected_name}'"""
        # )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_userattendance_sj(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_8_admin6']}", [selected_name])
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


def get_userinfo_sw(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        # print("$$$$$$$$")
        # print(userid, rfid_uid)
        cursor.execute(f"SELECT name FROM sw_users WHERE id = {userid} and rfid_uid = {rfid_uid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_userinfo_test(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        # print("$$$$$$$$")
        # print(userid, rfid_uid)
        cursor.execute(f"SELECT name FROM dev_users WHERE id = {userid} and rfid_uid = {rfid_uid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_userinfo_bp(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        # print("$$$$$$$$")
        # print(userid, rfid_uid)
        cursor.execute(f"SELECT name FROM bp_users WHERE id = {userid} and rfid_uid = {rfid_uid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_userinfo_sj(db, userid, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT name FROM sj_users WHERE id = {userid} and rfid_uid = {rfid_uid};")
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


def is_rfid_sw(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from sw_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def is_rfid_test(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from dev_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def is_rfid_bp(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from bp_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def is_rfid_sj(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select count(*) as cnt from sj_users where rfid_uid = {rfid_uid};")
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


def get_rfid_sw(db, rfid_uid):
    try:
        cursor = db.cursor()
        print("**************" + str(rfid_uid))
        cursor.execute(f"select id from sw_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_rfid_test(db, rfid_uid):
    try:
        cursor = db.cursor()
        print("**************" + str(rfid_uid))
        cursor.execute(f"select id from dev_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_rfid_bp(db, rfid_uid):
    try:
        cursor = db.cursor()
        # print("**************" + str(rfid_uid))
        cursor.execute(f"select id from bp_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))

def get_rfid_sj(db, rfid_uid):
    try:
        cursor = db.cursor()
        cursor.execute(f"select id from sj_users where rfid_uid = {rfid_uid};")
        return cursor.fetchone()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


# def get_userlist(db):
#     try:
#         cursor = db.cursor()
#         cursor.execute(f"SELECT * FROM users")
#         # 이렇게 하면 나중에 돈 많이나옴.
#         return cursor.fetchall()
#     except pymysql.Error as e:
#         print("db error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_adduserlist(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin1"]}"""
        )
        # cursor.execute(
        #     f"select users.id, users.name, users.rfid_uid from users where not exists(select users_detail.id from users_detail where users.id = users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_adduserlist_mh(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin2"]}"""
        )
        # cursor.execute(
        #     f"select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_adduserlist_sw(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin3"]}"""
        )
        # cursor.execute(
        #     f"select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_adduserlist_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin4"]}"""
        )
        # cursor.execute(
        #     f"select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_adduserlist_bp(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin5"]}"""
        )
        # cursor.execute(
        #     f"select mh_users.id, mh_users.name, mh_users.rfid_uid from moya.mh_users where not exists(select mh_users_detail.id from mh_users_detail where mh_users.id = mh_users_detail.id);")
        # 카드등록시 미등록된 리스트만 나오도록 하기위함.
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_adduserlist_sj(db):
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""{sqlmapper["sql_6_admin6"]}"""
        )
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pomysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userdetail(db):
    try:
        cursor = db.cursor()
        # cursor.execute(f"SELECT * FROM users_detail")
        cursor.execute(f"{sqlmapper['sql_5_admin1']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userdetail_mh(db):
    try:
        cursor = db.cursor()
        # cursor.execute(f"SELECT * FROM mh_users_detail")
        cursor.execute(f"{sqlmapper['sql_5_admin2']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userdetail_sw(db):
    try:
        cursor = db.cursor()
        # cursor.execute(f"SELECT * FROM mh_users_detail")
        cursor.execute(f"{sqlmapper['sql_5_admin3']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userdetail_test(db):
    try:
        cursor = db.cursor()
        # cursor.execute(f"SELECT * FROM mh_users_detail")
        cursor.execute(f"{sqlmapper['sql_5_admin4']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userdetail_bp(db):
    try:
        cursor = db.cursor()
        # cursor.execute(f"SELECT * FROM mh_users_detail")
        cursor.execute(f"{sqlmapper['sql_5_admin5']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userdetail_sj(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_5_admin6']}")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userselectdetail(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin1']}", [selected_name])
        # cursor.execute(f"SELECT * FROM users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userselectdetail_mh(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin2']}", [selected_name])
        # cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


def get_userselectdetail_sw(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin3']}", [selected_name])
        # cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userselectdetail_test(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin4']}", [selected_name])
        # cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userselectdetail_bp(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin5']}", [selected_name])
        # cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

def get_userselectdetail_sj(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"{sqlmapper['sql_7_admin6']}", [selected_name])
        # cursor.execute(f"SELECT * FROM mh_users_detail where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0


# 테스트코드로 보임
def get_username_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT name FROM dev_users_detail; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

# [개발] 방문 횟수와 작업시간 가져오는 기능
def get_workingtime_test(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT a.id, a.name , b.* FROM dev_users a LEFT JOIN (SELECT userid, max(used_time) AS used, count(*) as visit, sum(used_time) as total FROM dev_stat_attendance GROUP BY userid) b ON a.id = b.userid where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 오픈이후의 방문자 수, 작업시간 
def get_TotalVisit_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT  count(*) as 'total_visit', 
                sum(used) as 'total_time' FROM dev_users a LEFT JOIN 
                    (SELECT substr(entry_time, 1, 10) AS ent, 
                    userid, 
                    MAX(date_format(entry_time,"%r")) AS entry, 
                    MAX(date_format(exit_time,"%r")) AS exits, 
                    max(used_time) AS used
                    FROM dev_stat_attendance 
                    GROUP BY userid, substr(entry_time, 1, 10) 
                    ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
                b ON a.id =b.userid; 
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 오픈 이후주말 방문자 수  
def get_WeekendVisit_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        select count(weekday(entry_time)) as 'weekend_visit'
        from dev_stat_attendance 
        where weekday(entry_time) between 5 and 6; 
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 오픈 이후 평일 방문자 수  
def get_WeekVisit_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        select count(weekday(entry_time)) as 'week_visit'
        from dev_stat_attendance 
        where weekday(entry_time) between 0 and 4; 
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

# [개발] 최근 한달 방문자 수  
def get_LastMonthVisit_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT count(*) as 'last_month_visit', 
            sum(used) as 'last_month_time' FROM dev_users a LEFT JOIN 
                (SELECT substr(entry_time, 1, 10) AS ent, 
                userid, 
                MAX(date_format(entry_time,"%r")) AS entry, 
                MAX(date_format(exit_time,"%r")) AS exits, 
                max(used_time) AS used
                FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
                b ON a.id = b.userid 
            where date_format(b.ent, '%Y%m') = date_format(current_date, '%Y%m');
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

# [개발] 최근 한주 방문자 수  
def get_LastWeekVisit_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT count(*) as 'last_week_visit', 
            sum(used) as 'last_week_time' FROM dev_users a LEFT JOIN 
                (SELECT substr(entry_time, 1, 10) AS ent, 
                userid, 
                MAX(date_format(entry_time,"%r")) AS entry, 
                MAX(date_format(exit_time,"%r")) AS exits, 
                max(used_time) AS used
                FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) 
                b ON a.id = b.userid 
            where date_format(b.ent, '%Y%m%j') = date_format(current_date, '%Y%m%j');
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0

# [개발] 이번달 신규회원  
def get_NewMember_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        select count(created) as 'new_member' from `dev_users_detail` 
        where date_format(created, '%Y%m') = date_format(current_date, '%Y%m');
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 회원정보 구별
def get_Member_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        select  count(*) as 'total_member',
                count(case when sex = '남자' then 1 end) as 'boy', 
                count(case when sex = '여자' then 1 end) as 'girl',
                count(case when (year(current_date) - 6) = year  then 1 end) as 'seven',
                count(case when (year(current_date) - 7) = year  then 1 end) as 'eight',
                count(case when (year(current_date) - 8) = year  then 1 end) as 'nine',
                count(case when (year(current_date) - 9) = year  then 1 end) as 'ten',
                count(case when (year(current_date) - 10) = year  then 1 end) as 'eleven',
                count(case when (year(current_date) - 11) = year  then 1 end) as 'twelve'
        from dev_users_detail;
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 최근 한달간 자주오는 작은손  
def get_ComeOften_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT  name as 'name', 
                count(*) as 'times' 
                FROM dev_users a LEFT JOIN 
                (SELECT substr(entry_time, 1, 10) AS ent, 
                userid, 
                MAX(date_format(entry_time,"%r")) AS entry, 
                MAX(date_format(exit_time,"%r")) AS exits, 
                max(used_time) AS used
                FROM dev_stat_attendance GROUP BY userid, 
                substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , 
                userid ASC ) 
            b ON a.id = b.userid 
            where date_format(b.ent, '%Y%m') = date_format(current_date, '%Y%m') 
            group by name 
            order by count(*) desc 
            limit 3;
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

# [개발] 최근 한달간 작업시간이 많은 작은손  
def get_Workload_test(db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT  name as 'workload', 
                sum(used) as 'used_time' 
                FROM dev_users a LEFT JOIN 
                (SELECT substr(entry_time, 1, 10) AS ent, 
                userid, 
                MAX(date_format(entry_time,"%r")) AS entry, 
                MAX(date_format(exit_time,"%r")) AS exits, 
                max(used_time) AS used
                FROM dev_stat_attendance GROUP BY userid, 
                substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , 
                userid ASC ) 
            b ON a.id = b.userid 
            where date_format(b.ent, '%Y%m') = date_format(current_date, '%Y%m') 
            group by name 
            order by sum(used) desc 
            limit 3;
        """)
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 
# [세종] 방문 횟수와 작업시간 가져오는 기능
def get_workingtime_sj(db, selected_name):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT a.id, a.name , b.* FROM sj_users a LEFT JOIN (SELECT userid, max(used_time) AS used, count(*) as visit, sum(used_time) as total FROM sj_stat_attendance GROUP BY userid) b ON a.id = b.userid where name = '{selected_name}'; ")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0 

## [제천기적의도서관]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1

## [마하도서관]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify_mh(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE mh_users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE mh_users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1

## [수원바름샘]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify_sw(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE sw_users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE sw_users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1

## [개발용]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify_test(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE dev_users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE dev_users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1

## [반포도서관]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify_bp(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE bp_users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE bp_users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1

## [세종시립도서관]이름, 성별, 년도, 전화번호, 메모를 수정하는 기능 
def set_modify_sj(db, selected_name, modifyname, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_4 = f"UPDATE sj_users_detail SET name='{modifyname}', sex='{sex}', year={year}, phone='{phone}', memo='{memo}' where name ='{selected_name}' ;"
        cursor.execute(sql_4)
        db.commit()
        sql_5 = f"UPDATE sj_users SET name='{modifyname}' where name ='{selected_name}' ;" 
        cursor.execute(sql_5)
    except pymysql.Error as e:
        db.rollback()
        db.close()
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


def set_signup_sw(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into sw_users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update sw_users set name='{name}' where rfid_uid ='{rfid}';"
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

def set_signup_test(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into dev_users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update dev_users set name='{name}' where rfid_uid ='{rfid}';"
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

def set_signup_bp(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into bp_users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update bp_users set name='{name}' where rfid_uid ='{rfid}';"
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

def set_signup_sj(db, id, rfid, name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        sql_1 = f"insert into sj_users_detail(id,rfid,`name`, sex, year, phone, memo) value ('{id}','{rfid}', '{name}','{sex}','{year}','{phone}','{memo}');"
        cursor.execute(sql_1)
        db.commit()
        sql_2 = f"update sj_users set name='{name}' where rfid_uid ='{rfid}';"
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


def set_attendance_sw(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO sw_attendance(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        db.commit()
        db.close()
        return 1

def set_attendance_test(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO dev_attendance(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        db.commit()
        db.close()
        return 1

def set_attendance_bp(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO bp_attendance(user_id) VALUES ({userid})")
        print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        db.commit()
        db.close()
        return 1

def set_attendance_sj(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO sj_attendance(user_id) VALUES ({userid})")
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


def set_exit_sw(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO sw_exits(user_id) VALUES ({userid})")
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

def set_exit_test(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO dev_exits(user_id) VALUES ({userid})")
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

def set_exit_bp(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO bp_exits(user_id) VALUES ({userid})")
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

def set_exit_sj(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO sj_exits(user_id) VALUES ({userid})")
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
