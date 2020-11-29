import mysql.connector as sq

PASSWD = 'alohomora'
db = sq.connect(host='localhost', user='root', password=PASSWD)

def add_data(cursor):
    pass

def defineCursor(func):
    def wrapper(*args, **kwargs):
        cursor = db.cursor()
        result = func(cursor, *args, **kwargs)
        cursor.close()
        return result
    return wrapper

@defineCursor
def new_connection(cursor):
    cursor.execute('CREATE DATABASE IF NOT EXISTS library')
    cursor.execute('USE library')
    cursor.execute('SHOW TABLES LIKE \'books\'')
    result = cursor.fetchone()
    if not result:
        add_data(cursor)

@defineCursor
def fill_labels(cursor, table, column_id):
    cursor.execute(f'SELECT book, author FROM {table} WHERE book_id={column_id}')
    row = cursor.fetchone()
    if cursor.rowcount == 1:
        book, author = row
    else:
        book = author = ''
    if len(book) > 18:
        book = shorten_string(book)
    return book, author

def shorten_string(s):
    i = s.find(' ', 18, -1)
    i = s.rfind(' ') if i == -1 else i
    return s[:i] + '\n' + s[i:]

@defineCursor
def add_new_book(cursor, name, author, fiction):
    print(name, author, fiction)

@defineCursor
def get_issued_books(cursor, book_id, student_id):
    query = '''SELECT book_id, book, student_id, student_name, class FROM books, students
                WHERE .....'''
    data = [1, 'Bohemian Rhappsody', '1234', 'Freddie Mercury', 'XII Sci']
    return [data]

@defineCursor
def get_search(cursor, book_id, name, author):
    query = f'''SELECT book_id, book, author, type, 'yes' FROM books 
                WHERE book LIKE '%{name}%' and author LIKE '%{author}%' '''
    cursor.execute(query)
    data = []
    row = cursor.fetchone()
    while row:
        row = list(row)
        # if len(row[1]) > 18:
        #     row[1] = shorten_string(row[1])
            # print(row[1])
        # print(row)
        data.append(row)
        row = cursor.fetchone()
        
    return data

def close_connection():
    db.close()