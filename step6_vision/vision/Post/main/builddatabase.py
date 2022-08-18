import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='yourpassword', port=3306)
cursor = db.cursor()
cursor.execute("CREATE DATABASE weibo2 DEFAULT CHARACTER SET utf8mb4")
db.close()