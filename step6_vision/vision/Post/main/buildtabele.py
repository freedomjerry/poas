import pymysql
def tableexit(keyword):
    db = pymysql.connect(host='127.0.0.1', user='root', password='yourpassword', port=3306, db='weibo2')
    cursor = db.cursor()
    sql = 'drop table if exists comments_{keyword}'.format(keyword=keyword)
    cursor.execute(sql)
    db.close()
    
def buildtable(keyword):
    db = pymysql.connect(host='127.0.0.1', user='root', password='yourpassword', port=3306, db='weibo2')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS comments_{keyword} (id int NOT NULL AUTO_INCREMENT,user_id VARCHAR(255) NOT NULL, user_message VARCHAR(255) NOT NULL, weibo_message VARCHAR(255) NOT NULL, comment VARCHAR(255) NOT NULL, praise VARCHAR(255) NOT NULL, date VARCHAR(255) NOT NULL,sneti VARCHAR(255),label int, PRIMARY KEY (id))'.format(keyword=keyword)
    cursor.execute(sql)
    db.close()
