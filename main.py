from tkinter import *
import dbConnect as db
from tkinter import ttk
from tkinter import messagebox

TABLE_STUDENTS = 'students'
TABLE_BOOKS = 'books'

BTN_FONT = ('arial',15,'bold')
FONT_ENTRY = ('verdana',10,'bold')
FONT_BIG = ('arial',15,'bold')
FONT_SMALL = ('arial',12,'bold')
FONT_REALLY_BIG = ('arial',18,'bold')



def show_books():
    show_window = Toplevel(root)
    show_window.title('All issued books')
    show_window.geometry("700x380+400+200")
    show_window.resizable(False, False)

    lb_title = Label(show_window, text='Issued Books', font=FONT_REALLY_BIG)
    lb_book_id = Label(show_window, text='Book Id:', font=FONT_SMALL)
    lb_student_id = Label(show_window, text='Student Id:', font=FONT_SMALL)

    entry_book = Entry(show_window, font=FONT_ENTRY, width=10)
    entry_student = Entry(show_window, font=FONT_ENTRY, width=10)

    search_issued_books = lambda e: populate_issued_table(show_window, entry_book, entry_student)
    
    entry_book.bind("<KeyRelease>", search_issued_books)
    entry_student.bind("<KeyRelease>", search_issued_books)
    # btn_search = Button(show_window, text='Search', width=10, font=FONT_SMALL, command=search_issued_books)
    # btn_search.grid(row=3, column=0, columnspan=2)

    lb_title.grid(row=0, column=0, columnspan=2, pady=15)
    lb_book_id.grid(row=1, column=0)
    lb_student_id.grid(row=1, column=1)
    entry_book.grid(row=2, column=0)
    entry_student.grid(row=2, column=1)

    search_issued_books(None)

def populate_issued_table(window, entry_book, entry_student):
    # configuring table
    tree_frame = Frame(window)
    tree_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=15)
    
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)
    tree.pack()

    # populating table
    tree['columns'] = ('book_id', 'book_name', 'student_id', 'student_name', 'class')
    tree.column('#0', width=0, stretch=NO) #phantom column for dropdowns
    tree.column('book_id', anchor=CENTER, width=50)
    tree.column('book_name', anchor=CENTER, width=250)
    tree.column('student_id', anchor=CENTER, width=70)
    tree.column('student_name', anchor=CENTER, width=200)
    tree.column('class', anchor=CENTER, width=80)

    # headings
    tree.heading('#0', text='')
    tree.heading('book_id', text='Book Id')
    tree.heading('book_name', text='Book')
    tree.heading('student_id', text='Student Id')
    tree.heading('student_name', text='Issued by')
    tree.heading('class', text='Class')

    data = db.get_issued_books(entry_book.get().strip(), entry_student.get().strip())
    i = 0
    for row in data:
        tree.insert(parent='', index='end', iid=i, text='', value=row)
        i += 1
    

def search_book():
    search_window = Toplevel(root)
    search_window.title('Search Books')
    search_window.geometry("740x500+400+200")
    search_window.resizable(False, False)

    lb_title = Label(search_window, text='Search Books', font=FONT_REALLY_BIG)
    lb_name = Label(search_window, text='Enter Name:', font=FONT_SMALL)
    lb_author = Label(search_window, text='Enter Author:', font=FONT_SMALL)
    lb_id = Label(search_window, text='Enter Id:', font=FONT_SMALL)
    entry_name = Entry(search_window, font=FONT_ENTRY, width=28)
    entry_author = Entry(search_window, font=FONT_ENTRY, width=25)
    entry_id = Entry(search_window, font=FONT_ENTRY, width=6)

    empty_text_box = Label(search_window, text='Enter search queries\n\nOr just press Search\nto show all books.',
                            font=FONT_BIG, fg='#999')
    empty_text_box.grid(row=5, column=0, columnspan=5, pady=40)

    search_data = lambda: populate_table(search_window, entry_id, entry_name, entry_author)
    btn_search = Button(search_window, text='Search', width=10, font=FONT_BIG, command=search_data)
    btn_search.grid(row=3, column=0, columnspan=5, pady=15)
    
    lb_title.grid(row=0, column=1, columnspan=3, pady=15)
    lb_id.grid(row=1, column=0)
    lb_name.grid(row=1, column=1, columnspan=2, pady=2)
    lb_author.grid(row=1, column=3, columnspan=2, pady=2)
    entry_id.grid(row=2, column=0, ipady=2, padx=45)
    entry_name.grid(row=2, column=1, columnspan=2, ipady=2, padx=30, pady=2)
    entry_author.grid(row=2, column=3, columnspan=2, ipady=2, padx=30, pady=2)

def populate_table(window, book_id, name, author):
    # configuring table
    tree_frame = Frame(window)
    tree_frame.grid(row=5, column=0, columnspan=5, padx=20, pady=15)
    
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)
    tree.pack(expand=True)

    # populating data
    tree['columns'] = ('id', 'name', 'author', 'fiction', 'issued')
    tree.column('#0', width=0, stretch=NO) #phantom column for dropdowns
    tree.column('id', anchor=CENTER, width=50)
    tree.column('name', anchor=CENTER, width=250)
    tree.column('author', anchor=CENTER, width=200)
    tree.column('fiction', anchor=CENTER, width=100)
    tree.column('issued', anchor=CENTER, width=90)

    # headings
    tree.heading('#0', text='')
    tree.heading('id', text='Id')
    tree.heading('name', text='Name')
    tree.heading('author', text='Author')
    tree.heading('fiction', text='Type')
    tree.heading('issued', text='Is issued')
    
    data = db.get_search(book_id.get().strip(), name.get().strip(), author.get().strip())
    i = 0
    for row in data:
        tree.insert(parent='', index='end', iid=i, text='', value=row)
        i += 1
    
def findBook(table, key, label1, label2):
    col1, col2 = db.fill_labels(table=table, column_id=key)
    label1.configure(text=col1)
    label2.configure(text=col2)

def return_book():
    return_window = Toplevel(root)
    return_window.title('Return a Book')
    return_window.geometry("380x530+400+180")
    return_window.resizable(False, False)

    book_id = StringVar()
    student_id = StringVar()
    
    fill_non_specific_info(return_window)

    keypress_event = lambda: fill_return_details(return_window, entry_book_id, entry_student_id, lb_book_name_show,
                                                lb_book_author_show, lb_student_name_show, lb_student_class_show)

    lb_book_name_show = Label(return_window, text='Harry Potter and\nthe half blood prince', font=FONT_SMALL)
    lb_book_author_show = Label(return_window, text='Stephen King', font=FONT_SMALL)
    entry_book_id = Entry(return_window, textvariable=book_id, width=20, font=FONT_ENTRY)
    find_student = Button(return_window, text='Find student', font=FONT_SMALL, command=keypress_event)
    # entry_book_id.bind("<KeyRelease>", keypress_event)
    
    lb_student_name_show = Label(return_window, text='Bruce Banner', font=FONT_SMALL)
    lb_student_class_show = Label(return_window, text='XII Science', font=FONT_SMALL)
    entry_student_id = Entry(return_window, textvariable=student_id, width=20, font=FONT_ENTRY)
    find_book = Button(return_window, text='Find book issued', font=FONT_SMALL, command=keypress_event)
    # entry_student_id.bind("<KeyRelease>", keypress_event)
    on_return = lambda: return_book_in_db(return_window, entry_book_id)
    btn_return = Button(return_window, text='Return Book', width=25, font=BTN_FONT, command=on_return)

    find_student.grid(row=4, column=0, columnspan=2, pady=5)
    find_book.grid(row=10, column=0, columnspan=2, pady=5)
    entry_book_id.grid(row=1, column=1, pady=5,sticky=W, ipady=2)
    lb_book_name_show.grid(row=2, column=1, pady=5)
    lb_book_author_show.grid(row=3, column=1, pady=5)
    entry_student_id.grid(row=6, column=1, pady=5,sticky=W, ipady=2)
    lb_student_name_show.grid(row=8, column=1, pady=5)
    lb_student_class_show.grid(row=9, column=1, pady=5)
    btn_return.grid(row=11, column=0, columnspan=2, padx=30, pady=25)

def return_book_in_db(window, entry_book_id):
    returned = db.return_book(entry_book_id.get().strip())
    if returned:
        messagebox.showinfo(title='Success',
            message='The book has been returned.')
        window.destroy()
    else:
        print(entry_book_id.get().strip())
        messagebox.showerror(title='Error', 
            message='Sorry, the book could not be returned.')
        window.lift(root)

def fill_return_details(window, book_id, std_id, lb_book, lb_author, lb_name, lb_class):
    row = db.fill_return_details(book_id.get().strip(), std_id.get().strip())

    # row form: [book_id, book, author, issued_by, student_name, class]
    if not row:
        row = ['' for _ in range(6)]
        messagebox.showwarning(title='Error', 
                message='Either the entered book is not issued\nOr the given student has not\nissued any book currently')
        window.lift(root)

    book_id.delete(0,END)
    book_id.insert(0,row[0])
    std_id.delete(0,END)
    std_id.insert(0,row[3])
    lb_book.configure(text=row[1])
    lb_author.configure(text=row[2])
    lb_name.configure(text=row[4])
    lb_class.configure(text=row[5])

def fill_non_specific_info(window):
    # not specific
    lb_book_details = Label(window, text='Book Details', font=FONT_BIG)
    lb_book_id = Label(window, text='Book id', font=FONT_SMALL)
    lb_book_name = Label(window, text='Name: ', font=FONT_SMALL)
    lb_book_author = Label(window, text='Author: ', font=FONT_SMALL)
    # not specific
    lb_student_details = Label(window, text='Student Details', font=FONT_BIG)
    lb_student_id = Label(window, text='Student id', font=FONT_SMALL)
    lb_student_name = Label(window, text='Name: ', font=FONT_SMALL)
    lb_student_class = Label(window, text='Class: ', font=FONT_SMALL)
    # not specific
    lb_book_details.grid(row=0, column=0, pady=15, columnspan=2)
    lb_book_id.grid(row=1, column=0, pady=5, padx=40)
    lb_book_name.grid(row=2, column=0, pady=5)
    lb_book_author.grid(row=3, column=0, pady=5)
    lb_student_details.grid(row=5, column=0, pady=15, columnspan=2)
    lb_student_id.grid(row=6, column=0, pady=5)
    lb_student_name.grid(row=8, column=0, pady=5)
    lb_student_class.grid(row=9, column=0, pady=5)

def issue_book():
    issue_window = Toplevel(root)
    issue_window.title('Issue new Book')
    issue_window.geometry("380x450+400+220")
    issue_window.resizable(False, False)
    
    book_id = StringVar()
    student_id = StringVar()
    
    fill_non_specific_info(issue_window)

    lb_book_name_show = Label(issue_window, text='Harry Potter and\nthe half blood prince', font=FONT_SMALL)
    lb_book_author_show = Label(issue_window, text='Stephen King', font=FONT_SMALL)
    entry_book_id = Entry(issue_window, textvariable=book_id, width=20, font=FONT_ENTRY)
    keypress_book = lambda e: findBook(TABLE_BOOKS, entry_book_id.get(), lb_book_name_show, lb_book_author_show)
    entry_book_id.bind("<KeyRelease>", keypress_book)
    
    lb_student_name_show = Label(issue_window, text='Bruce Banner', font=FONT_SMALL)
    lb_student_class_show = Label(issue_window, text='XII Science', font=FONT_SMALL)
    entry_student_id = Entry(issue_window, textvariable=student_id, width=20, font=FONT_ENTRY)
    keypress_student = lambda e: findBook(TABLE_STUDENTS, entry_student_id.get(), lb_student_name_show, lb_student_class_show)
    entry_student_id.bind("<KeyRelease>", keypress_student)
    
    on_issue = lambda: issue_book_in_db(issue_window, entry_book_id, entry_student_id)
    btn_issue = Button(issue_window, text='Issue Book', width=25, font=BTN_FONT, command=on_issue)

    entry_book_id.grid(row=1, column=1, pady=5,sticky=W, ipady=2)
    lb_book_name_show.grid(row=2, column=1, pady=5)
    lb_book_author_show.grid(row=3, column=1, pady=5)
    entry_student_id.grid(row=6, column=1, pady=5,sticky=W, ipady=2)
    lb_student_name_show.grid(row=8, column=1, pady=5)
    lb_student_class_show.grid(row=9, column=1, pady=5)
    btn_issue.grid(row=11, column=0, columnspan=2, padx=30, pady=25)

def issue_book_in_db(window, book_id, std_id):
    book_id = book_id.get().strip()
    std_id = std_id.get().strip()

    issued = db.issue_book(book_id, std_id)
    if issued == 'is issued':
        messagebox.showerror(title='Error',
            message='The book is already issued by someone')
        window.lift(root)
    elif issued == 'already issued':
        messagebox.showerror(title='Error',
            message='The student has already issued another book')
        window.lift(root)
    elif issued == False:
        messagebox.showerror(title='Error',
            message='There was some problem.\nThe book could not be issued.')
        window.destroy()
    else:
        messagebox.showinfo(title='Success',
            message='The book has been issued successfully.')
        window.destroy()
        

def add_new_book():
    add_window = Toplevel(root)
    add_window.title('Add New Book')
    add_window.geometry("450x290+400+220")
    add_window.resizable(False, False)

    fiction = BooleanVar()

    lb_title = Label(add_window, text='Add New Book', font=FONT_BIG)
    lb_name = Label(add_window, text='Name:', font=FONT_SMALL)
    lb_author = Label(add_window, text='Author:', font=FONT_SMALL)
    lb_fiction = Label(add_window, text='Select Type:', font=FONT_SMALL)
    
    entry_name = Entry(add_window, width=30, font=FONT_ENTRY)
    entry_author = Entry(add_window, width=30, font=FONT_ENTRY)
    drp_fiction = Radiobutton(add_window, text='Fiction', variable=fiction, value=True, font=FONT_SMALL)
    drp_nonfiction = Radiobutton(add_window, text='Non-fiction', variable=fiction, value=False, font=FONT_SMALL)

    add_to_db = lambda: add_new_book_in_db(add_window, entry_name, entry_author, fiction)
    btn_submit = Button(add_window, text='Submit', width=25, font=BTN_FONT, command=add_to_db)

    lb_title.grid(row=0, column=0, columnspan=3, pady=10)
    lb_name.grid(row=1, column=0, pady=10)
    entry_name.grid(row=1, column=1, pady=10, ipady=3, columnspan=2)
    lb_author.grid(row=2, column=0, pady=10)
    entry_author.grid(row=2, column=1, pady=10, ipady=3, columnspan=2)
    lb_fiction.grid(row=3, column=0, padx=25, pady=10)
    drp_fiction.grid(row=3, column=1)
    drp_nonfiction.grid(row=3, column=2)

    btn_submit.grid(row=4, column=0, columnspan=3, pady=30)

def add_new_book_in_db(window, name, author, fiction):
    name = name.get().strip()
    author = author.get().strip()
    fiction = fiction.get()
    fiction = 'fiction' if fiction else 'non fiction'
    # print(name, author, fiction, 'asdd')
    if name and author:
        added = db.add_new_book(name, author, fiction)
        if added:
            messagebox.showinfo(title='Success',
                message='The book has been added to the database.')
            window.destroy()
        else:
            messagebox.showerror(title='Error',
                message='There was an error in adding the book.')
            window.lift(root)
    else:
        messagebox.showwarning(title='Invalid',
                message='Please enter the correct values.')
        window.lift(root)

root = Tk()
root.title('Library Management System')
root.geometry("480x450+400+200")
root.resizable(False,False)

app_title = Label(root, text='Library Management System', font=FONT_REALLY_BIG)

issue_btn = Button(root, text='Issue Book', font=BTN_FONT, width=30, command=issue_book)
return_btn = Button(root, text='Return Book', font=BTN_FONT, width=30, command=return_book)
search_btn = Button(root, text='Search Book', font=BTN_FONT, width=30, command=search_book)
add_btn = Button(root, text='Add New Book', font=BTN_FONT, width=30, command=add_new_book)
show_btn = Button(root, text='Show Issued Books', font=BTN_FONT, width=30, command=show_books)

app_title.pack(pady=20)
issue_btn.pack(pady=10)
return_btn.pack(pady=10)
search_btn.pack(pady=10)
add_btn.pack(pady=10)
show_btn.pack(pady=10)


db.new_connection()
root.mainloop()
db.close_connection()