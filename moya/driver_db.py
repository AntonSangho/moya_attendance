import pymysql
import os;

# 데이타베이스 초기화 정보

def init_connect_db():
    db = pymysql.connect(
        #if app.env =='development':
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASSWORD'), #beanstalk 환경변수 이용
        db=os.getenv('DB_NAME'), #beanstalk 환경변수 이용
        host=os.getenv('DB_HOST'), #beanstalk 환경변수 이용
        charset='utf8', #beanstalk 환경변수 이용
        cursorclass=pymysql.cursors.DictCursor
    )
    return db


# rfid 태그값 가져오기
def get_attendance(db):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, user_id, clock_in FROM attendance ORDER BY id DESC")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" %(e.args[0], e.args[1]))

def get_userinfo(db, userid):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT name FROM users WHERE id = {userid};")
        return cursor.fetchall()
    except pymysql.Error as e:
        print("db error pymysql %d: %s" %(e.args[0], e.args[1]))

# rfid 태깅기록
# 입장기록 
def set_attendance(db, userid):
    try:
         cursor = db.cursor()
         cursor.execute(f"INSERT INTO attendance(user_id) VALUES ({userid})")
         print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" %(e.args[0], e.args[1]))
    else:
        db.commit()
        #db.close()
        return 1

# rfid 태깅기록
# 퇴장기록 
def set_exit(db, userid):
    try:
         cursor = db.cursor()
         cursor.execute(f"INSERT INTO exits(user_id) VALUES ({userid})")
         print("db commit successfully")
    except pymysql.Error as e:
        db.rollback()
        db.close()
        print("db error pymysql %d: %s" %(e.args[0], e.args[1]))
        raise
    else:
        db.commit()
        #db.close()
        return 1
   
    
    