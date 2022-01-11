import pymysql

# 접속
db = pymysql.connect(user='righthand',passwd='moya_0526', db='moya', host='moy.cismqc0tinee.ap-northeast-2.rds.amazonaws.com',charset='utf8',cursorclass=pymysql.cursors.DictCursor)

# 커서 가져오기
cursor = db.cursor()

try:
    with db.cursor() as cursor:
        sql = ''' 
            select * from dev_users
            '''
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
finally:
    db.close()

for row in result:
    print(row)
    print("\n")



