# test_connection.py

import pymysql
from scrapy.utils.project import get_project_settings


settings = get_project_settings()
host = settings['DB_HOST']
port = settings['DB_PORT']
user = settings['DB_USER']
password = settings['DB_PASSWORD']
name = settings['DB_NAME']
charset = settings['DB_CHARSET']

print(host, port, user, password, name,charset)
connection = pymysql.connect(host=host, 
                            port=port,
                            user=user, 
                            password=password,
                            db=name, 
                            charset=charset)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print("Database version: {}".format(result))
finally:
    connection.close()
