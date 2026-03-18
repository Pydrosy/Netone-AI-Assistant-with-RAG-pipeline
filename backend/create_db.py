# save as create_db.py
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Lisa2021!',
    port=3306
)

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS netone_chat_db")
print("✅ Database 'netone_chat_db' is ready")
cursor.close()
connection.close()