from tkinter import *
import dbConnect as db
from tkinter import ttk
from tkinter import messagebox
import sys

TABLE_MEMBERS = 'members'
TABLE_BOOKS = 'books'
GENRES = [
    'Fiction', 'Non-Fiction', 'Biography', 'Course Book'
]
COLOR = '#f6f6f6'
CLR_GRAY = '#999'

BTN_FONT = ('arial',15,'bold')
FONT_ENTRY = ('verdana',10,'bold')
FONT_BIG = ('arial',15,'bold')
FONT_SMALL = ('arial',12,'bold')
FONT_REALLY_BIG = ('arial',19,'bold')

def insert_into_entry(entry, val):
    # for key, val in items.items():
    entry.delete(0, END)
    entry.insert(0, val)

def configure_treeview(window, **kwargs):
    # configuring table 
    tree_frame = Frame(window)
    tree_frame.grid(kwargs)#row=4, column=0, columnspan=2, padx=20, pady=15)
    
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)
    tree.pack()
    return tree

def show_books():
    '''Show issued books window'''
    show_window = Toplevel(root)
    show_window.title('All issued books')
    show_window.geometry("740x380+400+200")
    show_window.resizable(False, False)

    lb_title = Label(show_window, text='Issued Books', font=FONT_REALLY_BIG)
    lb_book_id = Label(show_window, text='Book Id:', font=FONT_SMALL)
    lb_student_id = Label(show_window, text='Student Id:', font=FONT_SMALL)

    entry_book = Entry(show_window, font=FONT_ENTRY, width=10)
    entry_student = Entry(show_window, font=FONT_ENTRY, width=10)

    entry_book.bind("<KeyRelease>", lambda e: populate_table())
    entry_student.bind("<KeyRelease>", lambda e: populate_table())

    lb_title.grid(row=0, column=0, columnspan=2, pady=15)
    lb_book_id.grid(row=1, column=0)
    lb_student_id.grid(row=1, column=1)
    entry_book.grid(row=2, column=0)
    entry_student.grid(row=2, column=1)

    def populate_table():
        tree = configure_treeview(show_window, row=4, column=0, columnspan=2, padx=20, pady=15)
        # populating table
        tree['columns'] = ('book_id', 'book_name', 'student_id', 'student_name', 'class', 'date')
        tree.column('#0', width=0, stretch=NO) #phantom column for dropdowns
        tree.column('book_id', anchor=CENTER, width=50)
        tree.column('book_name', anchor=CENTER, width=250)
        tree.column('student_id', anchor=CENTER, width=70)
        tree.column('student_name', anchor=CENTER, width=140)
        tree.column('class', anchor=CENTER, width=80)
        tree.column('date', anchor=CENTER, width=100)

        # headings
        tree.heading('#0', text='')
        tree.heading('book_id', text='Book Id')
        tree.heading('book_name', text='Book')
        tree.heading('student_id', text='Student Id')
        tree.heading('student_name', text='Issued by')
        tree.heading('class', text='Class')
        tree.heading('date', text='Issue Date')

        data = db.get_issued_books(entry_book.get().strip(), entry_student.get().strip())
        i = 0
        for row in data:
            tree.insert(parent='', index='end', iid=i, text='', value=row)
            i += 1
    
    populate_table()

def search_book():
    '''Search books window'''
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
                            font=FONT_BIG, fg=CLR_GRAY)
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
    '''Fill info on KeyRelease'''
    col1, col2 = db.fill_labels(table=table, column_id=key)
    label1.configure(text=col1)
    label2.configure(text=col2)

def return_book():
    '''Return book window'''
    return_window = Toplevel(root)
    return_window.title('Return a Book')
    return_window.geometry("380x530+400+180")
    return_window.resizable(False, False)

    book_id = StringVar()
    student_id = StringVar()
    
    fill_non_specific_info(return_window)

    keypress_event = lambda: fill_return_details()

    lb_book_name = Label(return_window, text='', font=FONT_SMALL)
    lb_author = Label(return_window, text='', font=FONT_SMALL)
    entry_book_id = Entry(return_window, textvariable=book_id, width=20, font=FONT_ENTRY)
    find_student = Button(return_window, text='Find student', font=FONT_SMALL, command=keypress_event)
    
    lb_member_name = Label(return_window, text='', font=FONT_SMALL)
    lb_member_class = Label(return_window, text='', font=FONT_SMALL)
    entry_member_id = Entry(return_window, textvariable=student_id, width=20, font=FONT_ENTRY)
    find_book = Button(return_window, text='Find book issued', font=FONT_SMALL, command=keypress_event)
    on_return = lambda: return_book_in_db()
    btn_return = Button(return_window, text='Return Book', width=25, font=BTN_FONT, command=on_return)

    find_student.grid(row=4, column=0, columnspan=2, pady=5)
    find_book.grid(row=10, column=0, columnspan=2, pady=5)
    entry_book_id.grid(row=1, column=1, pady=5,sticky=W, ipady=2)
    lb_book_name.grid(row=2, column=1, pady=5)
    lb_author.grid(row=3, column=1, pady=5)
    entry_member_id.grid(row=6, column=1, pady=5,sticky=W, ipady=2)
    lb_member_name.grid(row=8, column=1, pady=5)
    lb_member_class.grid(row=9, column=1, pady=5)
    btn_return.grid(row=11, column=0, columnspan=2, padx=30, pady=25)

    def return_book_in_db():
        returned = db.return_book(entry_book_id.get().strip())
        if returned:
            messagebox.showinfo(title='Success',
                message='The book has been returned.')
            return_window.destroy()
        else:
            messagebox.showerror(title='Error', 
                message='Sorry, the book could not be returned.')
            return_window.lift(root)

    def fill_return_details():
        row = db.fill_return_details(
            entry_book_id.get().strip(), entry_member_id.get().strip())

        # row form: [book_id, book, author, issued_by, student_name, class]
        if not row:
            row = ['' for _ in range(6)]
            messagebox.showwarning(title='Error', 
                    message='Either the entered book is not issued\nOr the given member has not\nissued any books currently')
            return_window.lift(root)

        entry_book_id.delete(0,END)
        entry_book_id.insert(0,row[0])
        entry_member_id.delete(0,END)
        entry_member_id.insert(0,row[3])
        lb_book_name.configure(text=row[1])
        lb_author.configure(text=row[2])
        lb_member_name.configure(text=row[4])
        lb_member_class.configure(text=row[5])

def fill_non_specific_info(window):
    '''Fill the common fields in issue/return windows'''
    lb_book_details = Label(window, text='Book Details', font=FONT_BIG)
    lb_book_id = Label(window, text='Book id', font=FONT_SMALL)
    lb_book_name = Label(window, text='Name: ', font=FONT_SMALL)
    lb_book_author = Label(window, text='Author: ', font=FONT_SMALL)
    lb_student_details = Label(window, text='Student Details', font=FONT_BIG)
    lb_student_id = Label(window, text='Student id', font=FONT_SMALL)
    lb_student_name = Label(window, text='Name: ', font=FONT_SMALL)
    lb_student_class = Label(window, text='Class: ', font=FONT_SMALL)

    lb_book_details.grid(row=0, column=0, pady=15, columnspan=2)
    lb_book_id.grid(row=1, column=0, pady=5, padx=40)
    lb_book_name.grid(row=2, column=0, pady=5)
    lb_book_author.grid(row=3, column=0, pady=5)
    lb_student_details.grid(row=5, column=0, pady=15, columnspan=2)
    lb_student_id.grid(row=6, column=0, pady=5)
    lb_student_name.grid(row=8, column=0, pady=5)
    lb_student_class.grid(row=9, column=0, pady=5)

def issue_book():
    '''Issue book window'''
    issue_window = Toplevel(root)
    issue_window.title('Issue new Book')
    issue_window.geometry("380x450+400+220")
    issue_window.resizable(False, False)
    
    book_id = StringVar()
    student_id = StringVar()
    
    fill_non_specific_info(issue_window)

    lb_book_name_show = Label(issue_window, text='', font=FONT_SMALL)
    lb_book_author_show = Label(issue_window, text='', font=FONT_SMALL)
    entry_book_id = Entry(issue_window, textvariable=book_id, width=20, font=FONT_ENTRY)
    keypress_book = lambda e: findBook(TABLE_BOOKS, entry_book_id.get(), lb_book_name_show, lb_book_author_show)
    entry_book_id.bind("<KeyRelease>", keypress_book)
    
    lb_student_name_show = Label(issue_window, text='', font=FONT_SMALL)
    lb_student_class_show = Label(issue_window, text='', font=FONT_SMALL)
    entry_student_id = Entry(issue_window, textvariable=student_id, width=20, font=FONT_ENTRY)
    keypress_student = lambda e: findBook(TABLE_MEMBERS, entry_student_id.get(), lb_student_name_show, lb_student_class_show)
    entry_student_id.bind("<KeyRelease>", keypress_student)
    
    btn_issue = Button(issue_window, text='Issue Book', width=25, font=BTN_FONT, 
        command=lambda: issue_book_in_db())

    entry_book_id.grid(row=1, column=1, pady=5,sticky=W, ipady=2)
    lb_book_name_show.grid(row=2, column=1, pady=5)
    lb_book_author_show.grid(row=3, column=1, pady=5)
    entry_student_id.grid(row=6, column=1, pady=5,sticky=W, ipady=2)
    lb_student_name_show.grid(row=8, column=1, pady=5)
    lb_student_class_show.grid(row=9, column=1, pady=5)
    btn_issue.grid(row=11, column=0, columnspan=2, padx=30, pady=25)

    def issue_book_in_db():
        book_id = entry_book_id.get().strip()
        std_id = entry_student_id.get().strip()

        issued = db.issue_book(book_id, std_id)
        if issued == 'is issued':
            messagebox.showwarning(title='Error',
                message='The book is already issued by someone')
            issue_window.lift(root)
        elif issued == False:
            messagebox.showerror(title='Error',
                message='There was some problem.\nThe book could not be issued.')
            issue_window.destroy()
        else:
            messagebox.showinfo(title='Success',
                message='The book has been issued successfully.')
            issue_window.destroy()

def edit_book():
    '''Delete book window'''
    edit_window = Toplevel(root)
    edit_window.title('Update/Delete Book')
    edit_window.geometry("420x320+500+220")
    edit_window.resizable(False, False)

    var_genre = StringVar(edit_window)
    var_genre.set('')

    entry_id = Entry(edit_window, width=28, font=FONT_ENTRY)
    entry_name = Entry(edit_window, width=28, font=FONT_ENTRY)
    entry_author = Entry(edit_window, width=28, font=FONT_ENTRY)
    drp_genre = OptionMenu(edit_window, var_genre, *GENRES)
    drp_genre.config(font=FONT_SMALL)
    
    # fill_details = lambda e: findBook(TABLE_BOOKS, entry_id.get().strip(), entry_name, entry_author)
    entry_id.bind('<KeyRelease>', lambda e:fill_details())
    
    delete = lambda: delete_from_db(edit_window, entry_id.get().strip())
    
    btn_fr = Frame(edit_window)
    btn_fr.grid(row=5, column=0, columnspan=2, pady=20)
    btn_update = Button(btn_fr, text='Update', width=12, font=BTN_FONT, 
        command=lambda: update_book())
    btn_delete = Button(btn_fr, text='Delete', width=12, font=BTN_FONT, 
        command=delete)
    btn_update.grid(row=0, column=0, padx=5)
    btn_delete.grid(row=0, column=1)

    drp_genre.grid(row=4, column=1)
    entry_id.grid(row=1, column=1, pady=10, ipady=3)
    entry_name.grid(row=2, column=1, pady=10, ipady=3)
    entry_author.grid(row=3, column=1, pady=10, ipady=3)

    Label(edit_window, text=' '*7+'Update / Delete Book', font=FONT_BIG).grid(
        row=0, column=0, columnspan=2, pady=10)
    Label(edit_window, text='Book Id:', font=FONT_SMALL).grid(
        row=1, column=0, pady=10, padx=30)
    Label(edit_window, text='Name:', font=FONT_SMALL).grid(
        row=2, column=0, pady=10)
    Label(edit_window, text='Author:', font=FONT_SMALL).grid(
        row=3, column=0, pady=10)
    Label(edit_window, text='Genre:', font=FONT_SMALL).grid(
        row=4, column=0, pady=10)

    def fill_details():
        book_id = entry_id.get()
        name, author, genre = db.fill_member_details(TABLE_BOOKS, book_id)
        insert_into_entry(entry_name, name)
        insert_into_entry(entry_author, author)
        var_genre.set(genre)

    def update_book():
        book_id = entry_id.get()
        name = entry_name.get().strip()
        author = entry_author.get().strip()
        genre = var_genre.get()

        if book_id and name and author:
            updated = db.update_member(TABLE_BOOKS, book_id, name, author, genre)
            if updated:
                messagebox.showinfo(title='Success',
                    message='Book details have been Updated.')
                edit_window.destroy()
                return

        messagebox.showerror(title='Error',
            message='Please enter proper values.')
        edit_window.lift(root)

    def delete_book():
        book_id = entry_id.get()
        deleted = db.delete_entry(TABLE_BOOKS, book_id)
        if deleted:
            messagebox.showinfo(title='Success',
                message='The Book has been deleted.')
            edit_window.destroy()
        else:
            messagebox.showerror(title='Error',
                message='There was some problem.\nTry again later.')
            edit_window.lift(root) 


def delete_from_db(window, book_id):
    deleted = db.delete_entry('books', book_id)
    if deleted:
        messagebox.showinfo(title='Success',
                message='The book has been deleted.')
    else:
        messagebox.showerror(title='Error',
                message='There was an error in deleting the book.')
    window.destroy()

def add_new_book():
    '''Add a new book window'''
    add_window = Toplevel(root)
    add_window.title('Add New Book')
    add_window.geometry("450x290+400+220")
    add_window.resizable(False, False)

    genre = StringVar(add_window)
    genre.set(GENRES[0])

    lb_title = Label(add_window, text='Add New Book', font=FONT_BIG)
    lb_name = Label(add_window, text='Name:', font=FONT_SMALL)
    lb_author = Label(add_window, text='Author:', font=FONT_SMALL)
    lb_fiction = Label(add_window, text='Genre:', font=FONT_SMALL)
    
    entry_name = Entry(add_window, width=30, font=FONT_ENTRY)
    entry_author = Entry(add_window, width=30, font=FONT_ENTRY)
    drp_genre = OptionMenu(add_window, genre, *GENRES)
    drp_genre.config(font=FONT_SMALL)

    btn_submit = Button(add_window, text='Submit', width=25, font=BTN_FONT, 
        command=lambda: add_to_db())

    lb_title.grid(row=0, column=0, columnspan=3, pady=10)
    lb_name.grid(row=1, column=0, pady=10)
    entry_name.grid(row=1, column=1, pady=10, ipady=3, columnspan=2)
    lb_author.grid(row=2, column=0, pady=10)
    entry_author.grid(row=2, column=1, pady=10, ipady=3, columnspan=2)
    lb_fiction.grid(row=3, column=0, padx=25, pady=10)
    drp_genre.grid(row=3, column=1)

    btn_submit.grid(row=4, column=0, columnspan=3, pady=30)

    def add_to_db():
        name = entry_name.get().strip()
        author = entry_author.get().strip()
        sel_genre = genre.get()
        if name and author:
            added = db.add_new_book(name, author, sel_genre)
            if added:
                messagebox.showinfo(title='Success',
                    message='The book has been added to the database.')
                add_window.destroy()
            else:
                messagebox.showerror(title='Error',
                    message='There was an error in adding the book.')
                add_window.lift(root)
        else:
            messagebox.showwarning(title='Invalid',
                    message='Please enter the correct values.')
            add_window.lift(root)

def add_member():
    ''' Adds new member into the database '''
    add_mem_window = Toplevel(root)
    add_mem_window.title('Add New Member')
    add_mem_window.geometry("400x280+400+220")
    add_mem_window.resizable(False, False)

    entry_name = Entry(add_mem_window, width=20, font=FONT_ENTRY)
    entry_class = Entry(add_mem_window, width=20, font=FONT_ENTRY)
    entry_section = Entry(add_mem_window, width=20, font=FONT_ENTRY)

    entry_name.grid(row=1, column=1, ipady=3)
    entry_class.grid(row=2, column=1, ipady=3)
    entry_section.grid(row=3, column=1, ipady=3)

    btn_submit = Button(add_mem_window, text='Submit', width=25, font=BTN_FONT,
         command=lambda: add_new_member_in_db())

    btn_submit.grid(row=4, column=0, columnspan=2, padx=25, pady=20)
    Label(add_mem_window, text='Add New Member', font=FONT_BIG).grid(
        row=0, column=0, pady=10, columnspan=2)
    Label(add_mem_window, text='Name:', font=FONT_SMALL).grid(
        row=1, column=0, pady=10, padx=25)
    Label(add_mem_window, text='Class:', font=FONT_SMALL).grid(
        row=2, column=0, pady=10)
    Label(add_mem_window, text='Section: ', font=FONT_SMALL).grid(
        row=3, column=0, pady=10)

    def add_new_member_in_db():
        name = entry_name.get().strip()
        clss = entry_class.get().strip() + ' ' + entry_section.get().strip().upper()
        
        inserted = db.add_new_member(name, clss)
        if inserted:
            messagebox.showinfo(title='Success',
                message='Member details have been added.')
            add_mem_window.destroy()
        else:
            messagebox.showerror(title='Error',
                message='There was some problem.\nTry again later.')
            add_mem_window.lift(root)

def edit_member():
    ''' Update member details or delete a member from database '''
    edit_mem_window = Toplevel(root)
    edit_mem_window.title('Add New Member')
    edit_mem_window.geometry("420x420+600+220")
    edit_mem_window.resizable(False, False)

    entry_id = Entry(edit_mem_window, width=20, font=FONT_ENTRY)
    entry_name = Entry(edit_mem_window, width=20, font=FONT_ENTRY)
    entry_class = Entry(edit_mem_window, width=20, font=FONT_ENTRY)
    entry_section = Entry(edit_mem_window, width=20, font=FONT_ENTRY)
    entry_date = Entry(edit_mem_window, width=20, font=FONT_ENTRY)

    entry_id.grid(row=1, column=1, ipady=3)
    entry_name.grid(row=2, column=1, ipady=3)
    entry_class.grid(row=3, column=1, ipady=3)
    entry_section.grid(row=4, column=1, ipady=3)
    entry_date.grid(row=5, column=1, ipady=3)

    entry_id.bind('<KeyRelease>', lambda e: fill_details())
    btn_update = Button(edit_mem_window, text='Update', width=12, font=BTN_FONT,
         command=lambda: update_member())
    btn_delete = Button(edit_mem_window, text='Delete', width=12, font=BTN_FONT,
         command=lambda: delete_member())

    btn_update.grid(row=6, column=0, pady=20, padx=25)
    btn_delete.grid(row=6, column=1, pady=20, padx=10)

    Label(edit_mem_window, text=' '*10+'Update / Delete Member', font=FONT_BIG).grid(
        row=0, column=0, padx=50, pady=15, columnspan=2)
    Label(edit_mem_window, text='Id:', font=FONT_SMALL).grid(
        row=1, column=0, pady=10)
    Label(edit_mem_window, text='Edit Name:', font=FONT_SMALL).grid(
        row=2, column=0, pady=10)
    Label(edit_mem_window, text='Edit Class:', font=FONT_SMALL).grid(
        row=3, column=0, pady=10, padx=35)
    Label(edit_mem_window, text='Edit Section:', font=FONT_SMALL).grid(
        row=4, column=0, pady=10)
    Label(edit_mem_window, text='Edit Date of\nJoining:\n(YYYY-MM-DD)', font=FONT_SMALL).grid(
        row=5, column=0, pady=10)

    def fill_details():
        mem_id = entry_id.get()
        name, clss, date = db.fill_member_details(TABLE_MEMBERS, mem_id)

        clss = clss.split(maxsplit=1) if clss else ['','']
        insert_into_entry(entry_name, name)
        insert_into_entry(entry_class, clss[0])
        insert_into_entry(entry_section, clss[-1])
        insert_into_entry(entry_date, date)

    def update_member():
        mem_id = entry_id.get()
        name = entry_name.get().strip()
        clss = entry_class.get().strip() + ' ' + entry_section.get().strip()
        date = entry_date.get().strip()
        
        if mem_id and name and clss and date:
            updated = db.update_member(TABLE_MEMBERS, mem_id, name, clss, date)
            if updated:
                messagebox.showinfo(title='Success',
                    message='Member details have been Updated.')
                edit_mem_window.destroy()
            else:
                messagebox.showerror(title='Error',
                    message='Please enter proper values\nMake sure the date is in correct format.')
                edit_mem_window.lift(root)
        else:
            messagebox.showerror(title='Error',
                message='Please enter proper values.')
            edit_mem_window.lift(root)

    def delete_member():
        mem_id = entry_id.get()
        deleted = db.delete_entry(TABLE_MEMBERS, mem_id)
        if deleted:
            messagebox.showinfo(title='Success',
                message='Member details have been deleted.')
            edit_mem_window.destroy()
        else:
            messagebox.showerror(title='Error',
                message='There was some problem.\nTry again later.')
            edit_mem_window.lift(root)

def show_members():
    ''' Window to show and search members '''
    members_window = Toplevel(root)
    members_window.title('Show All Members')
    members_window.geometry("640x420+400+200")
    members_window.resizable(False, False)

    entry_id = Entry(members_window, font=FONT_ENTRY, width=6)
    entry_name = Entry(members_window, font=FONT_ENTRY, width=28)
    entry_class = Entry(members_window, font=FONT_ENTRY, width=10)

    Label(members_window, text='Library Members', font=FONT_REALLY_BIG).grid(
        row=0, column=0, columnspan=3, pady=15)
    Label(members_window, text='Search by Id:', font=FONT_SMALL).grid(
        row=1, column=0)
    Label(members_window, text='Search by Name:', font=FONT_SMALL).grid(
        row=1, column=1, pady=2)
    Label(members_window, text='Search by Class:', font=FONT_SMALL).grid(
        row=1, column=2, pady=2)
    entry_id.grid(row=2, column=0, ipady=2, padx=10)
    entry_name.grid(row=2, column=1, ipady=2, padx=10, pady=10)
    entry_class.grid(row=2, column=2, ipady=2, padx=10)

    event_click = lambda e: populate_table()
    entry_id.bind('<KeyRelease>', event_click)
    entry_name.bind('<KeyRelease>', event_click)
    entry_class.bind('<KeyRelease>', event_click)

    def populate_table():
        tree = configure_treeview(members_window, row=3, column=0, columnspan=3, padx=20, pady=10)
        tree['columns'] = ('member_id', 'name', 'class', 'date')
        tree.column('#0', width=0, stretch=NO) #phantom column for dropdowns
        tree.column('member_id', anchor=CENTER, width=100)
        tree.column('name', anchor=CENTER, width=250)
        tree.column('class', anchor=CENTER, width=100)
        tree.column('date', anchor=CENTER, width=120)

        tree.heading('#0', text='')
        tree.heading('member_id', text='Member Id')
        tree.heading('name', text='Name')
        tree.heading('class', text='Class')
        tree.heading('date', text='Join Date')

        data = db.get_members(entry_id.get().strip(), entry_name.get().strip(), entry_class.get().strip())
        i = 0
        for row in data:
            tree.insert(parent='', index='end', iid=i, text='', value=row)
            i += 1
    populate_table()

'''Home page'''
root = Tk()
root.title('Library Management System')
root.geometry("900x380+350+200")
root.resizable(False,False)
root.configure(bg=COLOR)

app_title = Label(root, text='Library Management\nSystem', bg=COLOR, font=FONT_REALLY_BIG)

issue_btn = Button(root, text='Issue Book', font=BTN_FONT, width=20, bg=COLOR, command=issue_book)
return_btn = Button(root, text='Return Book', font=BTN_FONT, width=20, bg=COLOR, command=return_book)
search_btn = Button(root, text='Search for Books', font=BTN_FONT, width=20, bg=COLOR, command=search_book)
add_btn = Button(root, text='Add New Book', font=BTN_FONT, width=20, bg=COLOR, command=add_new_book)
edit_btn = Button(root, text='Update/Delete Book', font=BTN_FONT, width=20, bg=COLOR, command=edit_book)
show_btn = Button(root, text='Show Issued Books', font=BTN_FONT, width=20, bg=COLOR, command=show_books)
add_member_btn = Button(root, text='Add a Member', font=BTN_FONT, width=20, bg=COLOR, command=add_member)
edit_member_btn = Button(root, text='Update/Delete Member', font=BTN_FONT, width=20, bg=COLOR, command=edit_member)
show_members_btn = Button(root, text='Show All Members', font=BTN_FONT, width=20, bg=COLOR, command=show_members)

Label(root, text='Issue & Return\nBooks', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=1)
Label(root, text='Manage\nBooks', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=0)
Label(root, text='Manage\nMembers', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=2)

app_title.grid(row=0, column=1, columnspan=1, pady=25)
issue_btn.grid(row=2, column=1, pady=10, padx=25)
return_btn.grid(row=3, column=1, pady=10, padx=25)
show_btn.grid(row=4, column=1, pady=10, padx=25)
search_btn.grid(row=2, column=0, pady=10, padx=25)
add_btn.grid(row=3, column=0, pady=10, padx=25)
edit_btn.grid(row=4, column=0, pady=10, padx=25)
show_members_btn.grid(row=2, column=2, pady=10, padx=25)
add_member_btn.grid(row=3, column=2, pady=10, padx=25)
edit_member_btn.grid(row=4, column=2, pady=10, padx=25)

# TODO
# issue ✅
# return ✅
# show currently issued books ✅
# 🍧 use delete entry for return
# show members ✅
# add member ✅
# update/delete member ✅

# search books ✅
# add book ✅
# update/delete book ✅


try:
    PASSWD = 'alohomora'#sys.argv[1]
    db.new_connection(passwd=PASSWD)
    root.mainloop()
    db.close_connection()
except:
    messagebox.showwarning(title='Error',
        message='Could not connect to the database.')
