# save as quick_test.py
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Lisa2021!',
        port=3306
    )
    print("✅ SUCCESS! Connected to MySQL")
    connection.close()
except Exception as e:
    print(f"❌ Failed: {e}")