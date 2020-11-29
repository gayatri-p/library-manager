import mysql.connector as sq

PASSWD = 'alohomora'
db = sq.connect(host='localhost', user='root', password=PASSWD)

def add_data(cursor):
    pass

def new_connection():
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS library')
    cursor.execute('USE library')
    cursor.execute('SHOW TABLES LIKE \'books\'')
    result = cursor.fetchone()
    if not result:
        add_data(cursor)
    
    cursor.close()

new_connection()

db.close()