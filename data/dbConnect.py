import mysql.connector as sq
import csv 
import os

PATH = os.getcwd() + '\\'

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
    q1 = '''create table if not exists books(
        book_id int primary key auto_increment,
        book varchar(60),
        author varchar(60),
        type varchar(12),
        issued_by int
        )'''
    q2 = '''create table if not exists students(
        student_id int primary key,
        student_name varchar(25),
        class varchar(5)
        )'''
    cursor.execute(q1)
    cursor.execute(q2)
    student_data = get_student_data()
    books_data = get_books_data()
    
    try:
        for row in books_data:
            q = f'''INSERT INTO books(book, author, type, issued_by)
                    VALUES("{row[0]}", '{row[1]}', '{row[2]}', {row[3]})'''
            cursor.execute(q)
        for row in student_data:
            q = f'''INSERT INTO students
                    VALUES({row[0]}, '{row[1]}', '{row[2]}')'''
            cursor.execute(q)
    except:
        return

    db.commit()

def get_student_data():
    data = []
    with open(PATH+'sample_students.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            row[0] = int(row[0])
            data.append(row)
    return data

def get_books_data():
    data = []
    with open(PATH+'sample_books.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data  

@defineCursor
def fill_labels(cursor, table, column_id):
    '''Fill lables on KeyRelease functions'''
    if table == 'students':
        q = f'SELECT student_name, class FROM {table} WHERE student_id={column_id}'
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
def add_new_book(cursor, name, author, fiction):
    '''Add a new book to the database'''
    q = f'''INSERT INTO books(book, author, type)
        VALUES('{name}', '{author}', '{fiction}')'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def get_issued_books(cursor, book_id, student_id):
    '''Get the list of issued books along with issuer's info'''
    query = '''select book_id, book, student_id, student_name, class 
            from books, students
            where issued_by is not null and issued_by = student_id'''
    
    if book_id and student_id:
        query += f' and book_id = {book_id} and student_id={student_id}'
    elif book_id:
        query += f' and book_id = {book_id}'
    elif student_id:
        query += f' and student_id={student_id}'

    query += ' order by class'

    data = []
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
        return data

@defineCursor
def get_search(cursor, book_id, name, author):
    '''Get results for searched books'''
    if book_id:
        query = f''' SELECT book_id, book, author, type, issued_by FROM books 
                    WHERE book LIKE '%{name}%' and author LIKE '%{author}%'
                    AND book_id = {book_id} 
                '''
    else:
        query = f'''SELECT book_id, book, author, type, issued_by FROM books 
                    WHERE book LIKE '%{name}%' and author LIKE '%{author}%' '''
    
    cursor.execute(query)
    data = []
    row = cursor.fetchone()
    while row:
        row = list(row)
        row[4] = 'no' if row[4] == None else 'yes'
        data.append(row)
        row = cursor.fetchone()
        
    return data

@defineCursor
def issue_book(cursor, book_id, student_id):
    '''Issue a book'''
    cursor.execute(f'select issued_by from books where book_id = {book_id}')
    is_issued = cursor.fetchone()
    if is_issued[0]:
        return 'is issued'
    cursor.execute(f'select book from books where issued_by = {student_id}')
    already_issued = cursor.fetchone()
    if already_issued != None:
        return 'already issued'

    q = f'''UPDATE books SET issued_by={student_id}
        WHERE book_id={book_id}'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False
    
@defineCursor
def return_book(cursor, book_id):
    '''Return a book'''
    q = f'''UPDATE books SET issued_by=NULL
        WHERE book_id={book_id}'''
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

@defineCursor
def fill_return_details(cursor, book_id, student_id):
    '''Fill return details if entered info is correct'''
    q = ''
    if student_id and book_id:
        q = f'''SELECT book_id, book, author, issued_by, student_name, class from books, students
                WHERE issued_by = student_id and student_id={student_id} 
                and book_id={book_id}'''
    elif student_id:
        q = f'''SELECT book_id, book, author, issued_by, student_name, class from books, students
                WHERE issued_by = student_id and issued_by={student_id}'''
    elif book_id:
        q = f'''SELECT book_id, book, author, issued_by, student_name, class from books, students
            WHERE issued_by = student_id and book_id={book_id}'''
    else:
        # no input
        return ['' for _ in range(6)]

    try:
        cursor.execute(q)
        row = cursor.fetchone()
        return row
    except:
        return False

@defineCursor
def delete_book(cursor, book_id):
    '''Delete a book from the database'''
    q = f'DELETE FROM books WHERE book_id = {book_id}'
    try:
        cursor.execute(q)
        db.commit()
        return True
    except:
        return False

def close_connection():
    db.close()