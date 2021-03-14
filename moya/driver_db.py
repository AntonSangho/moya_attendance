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
    "sql_5_admin4": "SELECT * FROM test_users_detail",
    "sql_6_admin4": "select test_users.id, test_users.name, test_users.rfid_uid from moya.test_users where not exists(select test_users_detail.id from test_users_detail where test_users.id = test_users_detail.id);",
    "sql_7_admin4": "SELECT * FROM dev_users_detail where name = %s",
    "sql_8_admin4": """
            SELECT a.id, a.name , b.* FROM dev_users a LEFT JOIN (SELECT substr(entry_time, 1, 10) AS ent, userid, MAX(entry_time) AS entry, MAX(exit_time) AS exits, max(used_time) AS used
            FROM dev_stat_attendance GROUP BY userid, substr(entry_time, 1, 10) ORDER BY substr(entry_time, 1, 10) DESC , userid ASC ) b ON a.id = b.userid
            where a.name = %s"""
            

    # 미정
    # "sql_1_admin1": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    # "sql_1_admin2": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
    # "sql_1_admin3": "SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC",
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

def set_modify(db, selected_name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        # cursor.execute(f"{sqlmapper['sql_9_admin1']}", ([sex], [year], [phone], [memo], [selected_name]))
        cursor.execute(
            f"UPDATE users_detail SET sex='{sex}', year={year}, phone={phone}, memo='{memo}' where name ='{selected_name}' ;")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" % (e.args[0], e.args[1]))
        return 0
    else:
        db.commit()
        db.close()
        return 1


def set_modify_mh(db, selected_name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        # cursor.execute(f"{sqlmapper['sql_9_admin2']}",({sex}, {year}, {phone}, {memo}, {selected_name}))
        cursor.execute(
            f"UPDATE mh_users_detail SET sex='{sex}', year={year}, phone={phone}, memo='{memo}' where name ='{selected_name}' ;")
        print("1_1 - set_modify try")
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


def set_modify_sw(db, selected_name, sex, year, phone, memo):
    try:
        cursor = db.cursor()
        # cursor.execute(f"{sqlmapper['sql_9_admin2']}",({sex}, {year}, {phone}, {memo}, {selected_name}))
        cursor.execute(
            f"UPDATE sw_users_detail SET sex='{sex}', year={year}, phone={phone}, memo='{memo}' where name ='{selected_name}' ;")
        print("1_1 - set_modify try")
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
