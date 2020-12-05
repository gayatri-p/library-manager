import mysql.connector as sq
import csv 
import os
from datetime import datetime

PATH = os.getcwd() + '\\'
now = datetime.now()
DATE = now.strftime('%Y-%m-%d')

def new_connection(passwd):
    '''Establishes connection with MySQL database
        And adds sample data if needed'''
    global db
    db = sq.connect(host='localhost', user='root', password=passwd)
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS library')
    cursor.execute('USE library')
    cursor.execute('SHOW TABLES LIKE \'books\'')
    result = cursor.fetchone()
    if not result:
        add_data()

def defineCursor(func):
    '''Decorator funtion to create and close cursor instances'''
    def wrapper(*args, **kwargs):
        cursor = db.cursor()
        result = func(cursor, *args, **kwargs)
        try:
            cursor.close()
        except:
            _ = cursor.fetchall()
            cursor.close()
        return result
    return wrapper

@defineCursor
def add_data(cursor):
    '''Adding sample data to the database'''
    cursor.execute('''create table if not exists books(
        book_id int primary key auto_increment,
        book varchar(60),
        author varchar(60),
        genre varchar(15)
    )''')
    # cursor.execute(q)
    cursor.execute('''create table if not exists members(
        member_id int primary key auto_increment,
        name varchar(25),
        class varchar(5),
        join_date date
    )''')
    cursor.execute('''create table if not exists issued(
        book_id int,
        member_id int,
        date_of_issue date
    )''')
    
    books_data = get_sample_data(PATH+'sample_books.csv')
    members_data = get_sample_data(PATH+'sample_members.csv')
    issued_data = get_sample_data(PATH+'sample_issued.csv')

    try:
        for row in books_data:
            q = f'''INSERT INTO books(book, author, genre)
                    VALUES("{row[0]}", '{row[1]}', '{row[2]}')'''
            cursor.execute(q)
        for row in issued_data:
            q = f'''INSERT INTO issued
                    VALUES({row[0]}, {row[1]}, '{row[2]}')'''
            cursor.execute(q)
        for row in members_data:
            q = f'''INSERT INTO members(name, class, join_date)
                    VALUES('{row[0]}', '{row[1]}', '{row[2]}')'''
            cursor.execute(q)
    except:
        return

    db.commit()

def get_sample_data(path):
    data = []
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data  

@defineCursor
def fill_labels(cursor, table, column_id):
    '''Fill lables on KeyRelease functions'''
    if table == 'members':
        q = f'SELECT name, class FROM {table} WHERE member_id={column_id}'
    else:
        q = f'SELECT book, author FROM {table} WHERE book_id={column_id}'

    cursor.execute(q)
    row = cursor.fetchone()
    if cursor.rowcount == 1:
        col1, col2 = row
    else:
        col1 = col2 = ''
    if len(col1) > 18:
        col1 = shorten_string(col1)
    return col1, col2

def shorten_string(s):
    i = s.find(' ', 18, -1)
    i = s.rfind(' ') if i == -1 else i
    return s[:i] + '\n' + s[i:]

@defineCursor
def add_new_book(cursor, name, author, genre):
    '''Add a new book to the database'''
    q = f'''INSERT INTO books(book, author, genre)
        VALUES("{name}", '{author}', '{genre}')'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def get_issued_books(cursor, book_id, member_id):
    '''Get the list of issued books along with issuer's info'''
    query = '''SELECT issued.book_id, book, issued.member_id, name, class, date_of_issue FROM issued, members, books 
        WHERE members.member_id = issued.member_id
        AND books.book_id = issued.book_id'''
    
    if book_id and member_id:
        query += f' and issued.book_id = {book_id} and issued.member_id={member_id}'
    elif book_id:
        query += f' and issued.book_id = {book_id}'
    elif member_id:
        query += f' and issued.member_id={member_id}'

    query += ' ORDER BY date_of_issue'

    data = []
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
        return data

@defineCursor
def get_members(cursor, member_id, name, clss):
    q = f'''SELECT * FROM members
        WHERE name LIKE '%{name}%' AND class LIKE '%{clss}%' '''

    if member_id:
        q += f' AND member_id = {member_id}'

    data = []
    try:
        cursor.execute(q)
        data = cursor.fetchall()
        return data
    except:
        return data

@defineCursor
def get_search(cursor, book_id, name, author):
    '''Get results for searched books'''
    search_id = f' AND books.book_id = {book_id}'
    query = f'''SELECT books.book_id, book, author, genre,
            case
                when EXISTS (SELECT NULL FROM issued WHERE  books.book_id = issued.book_id)
                then 'Yes'
                ELSE 'No'
            END AS 'Issued'
        FROM books
        WHERE book LIKE '%{name}%' AND author LIKE '%{author}%'
        '''
    if book_id:
        query += search_id

    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
        return []

@defineCursor
def issue_book(cursor, book_id, member_id):
    '''Issue a book'''
    cursor.execute(f'SELECT * FROM issued WHERE book_id = {book_id}')
    is_issued = cursor.fetchone()
    if is_issued:
        return 'is issued'

    q = f"INSERT INTO issued VALUES({book_id},{member_id},'{DATE}')"
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False
    
@defineCursor
def return_book(cursor, book_id):
    '''Return a book'''
    q = f'''DELETE FROM issued WHERE book_id = {book_id}'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def fill_return_details(cursor, book_id, member_id):
    '''Fill return details if entered info is correct'''
    if member_id and book_id:
        q = f'WHERE issued.member_id = {member_id} AND issued.book_id = {book_id}'
    elif member_id:
        q = f'issued.member_id = {member_id}'
    elif book_id:
        q = f'issued.book_id = {book_id}'
    else:
        # no input
        return ['' for _ in range(6)]

    query = f'''SELECT issued.book_id, book, author, issued.member_id, name, class FROM issued, members, books 
        WHERE {q}
        AND members.member_id = issued.member_id
        AND books.book_id = issued.book_id'''

    try:
        cursor.execute(query)
        row = list(cursor.fetchone())
        if row and len(row[1]) > 18:
            row[1] = shorten_string(row[1])
        return row
    except:
        return False

@defineCursor
def add_new_member(cursor, name, clss):
    q = f'''INSERT INTO members(name, class, join_date)
        VALUES('{name}', '{clss}', '{DATE}')'''
    
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def update_member(cursor, table, _id, col1, col2, col3):
    if table == 'books':
        q = f'''UPDATE books
            SET book = '{col1}', author='{col2}', genre='{col3}'
            WHERE book_id = {_id}'''
    else:
        q = f'''UPDATE members
            SET name = '{col1}', class='{col2}', join_date='{col3}'
            WHERE member_id = {_id}'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def fill_member_details(cursor, table, _id):
    if table == 'members':
        q = f'''SELECT name, class, join_date FROM members
            WHERE member_id = {_id}'''
    else:
        q = f'''SELECT book, author, genre FROM books
            WHERE book_id = {_id}'''

    # row = 
    try:
        cursor.execute(q)
        row = cursor.fetchone()
        if row:
            return row
    except:
        pass
    return ['' for _ in range(3)]

@defineCursor
def delete_entry(cursor, table, _id):
    '''Delete a row from the database'''
    col = 'book_id' if table == 'books' else 'member_id'
    q = f'DELETE FROM {table} WHERE {col} = {_id}'
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

def close_connection():
    db.close()

if __name__ == '__main__':
    new_connection('alohomora')