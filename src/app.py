from tkinter import *
import dbConnect as db
from tkinter import ttk
from tkinter import messagebox
import sys
from components import *

TABLE_MEMBERS = 'members'
TABLE_BOOKS = 'books'
GENRES = ['Fiction', 'Non-Fiction', 'Biography', 'Course Book']

def show_issued_books():
    '''Show issued books window'''
    show_window = Toplevel(root)
    show_window.title('All issued books')
    show_window.geometry("740x380+400+200")
    show_window.resizable(False, False)

    lb_title = Label(show_window, text='Issued Books', font=FONT_REALLY_BIG)
    lb_book_id = MyLabel(show_window, text='Book Id')
    lb_student_id = MyLabel(show_window, text='Student Id')

    entry_book = MyEntry(show_window, width=10)
    entry_student = MyEntry(show_window, width=10)

    entry_book.bind("<KeyRelease>", lambda e: populate_table())
    entry_student.bind("<KeyRelease>", lambda e: populate_table())

    lb_title.grid(row=0, column=0, columnspan=2, pady=15)
    lb_book_id.grid(row=1, column=0)
    lb_student_id.grid(row=1, column=1)
    entry_book.grid(row=2, column=0)
    entry_student.grid(row=2, column=1)

    def populate_table():
        cols = ['book_id', 'book_name', 'student_id', 'student_name', 'class', 'date']
        col_names = ['Book Id', 'Book', 'Student Id', 'Issued by', 'Class', 'Issue Date']
        widths = [50, 250, 70, 140, 80, 100]

        tree = MyTree(show_window, row=4, column=0, columnspan=2, padx=20, pady=15)
        tree.set_columns(columns=cols, headings=col_names, widths=widths)
        
        data = db.get_issued_books(entry_book.val(), entry_student.val())
        tree.insert_data(data)
    
    populate_table()

def search_books():
    '''Search books window'''
    search_window = Toplevel(root)
    search_window.title('Search Books')
    search_window.geometry("740x500+400+200")
    search_window.resizable(False, False)

    entry_name = MyEntry(search_window, width=28)
    entry_author = MyEntry(search_window, width=22)
    entry_id = MyEntry(search_window, width=6)

    lb_length = Label(search_window, font=FONT_SMALL, fg=CLR_GRAY)
    lb_length.grid(row=5, column=0)

    btn_search = Button(search_window, text='Search', width=10, font=FONT_BIG, 
        command=lambda: populate_table())
    btn_search.grid(row=3, column=0, columnspan=5, pady=15)
    
    Label(search_window, text='Search Books', font=FONT_REALLY_BIG).grid(
        row=0, column=0, columnspan=4, pady=15)
    MyLabel(search_window, text='Enter Id:').grid(row=1, column=0)
    MyLabel(search_window, text='Enter Name:').grid(
        row=1, column=1, columnspan=2, pady=2)
    MyLabel(search_window, text='Enter Author:').grid(
        row=1, column=3, columnspan=2, pady=2)
    entry_id.grid(row=2, column=0, ipady=2, padx=45)
    entry_name.grid(row=2, column=1, columnspan=2, ipady=2, padx=30, pady=2)
    entry_author.grid(row=2, column=3, columnspan=2, ipady=2, padx=30, pady=2)

    def populate_table():
        book_id = entry_id.val()
        name = entry_name.val()
        author = entry_author.val()
        tree = MyTree(search_window, row=4, column=0, columnspan=4, padx=20, pady=15)
        
        cols = ['id', 'name', 'author', 'fiction', 'issued']
        col_names = ['Id', 'Name', 'Author', 'Type', 'Is issued']
        widths = [50, 250, 200, 100, 90]
        tree.set_columns(columns=cols, headings=col_names, widths=widths)
        
        data = db.get_search(book_id, name, author)
        lb_length.configure(text=f'{len(data)} results')
        tree.insert_data(data)

    populate_table()

def fill_non_specific_info(window):
    '''Fill the common fields in issue/return windows'''
    Label(window, text='Book Details', font=FONT_BIG).grid(
        row=0, column=0, pady=15, columnspan=2)
    MyLabel(window, text='Book id').grid(row=1, column=0, pady=5, padx=40)
    MyLabel(window, text='Name: ').grid(row=2, column=0, pady=5)
    MyLabel(window, text='Author: ').grid(row=3, column=0, pady=5)
    Label(window, text='Student Details', font=FONT_BIG).grid(
        row=5, column=0, pady=15, columnspan=2)
    MyLabel(window, text='Student id').grid(row=6, column=0, pady=5)
    MyLabel(window, text='Name: ').grid(row=8, column=0, pady=5)
    MyLabel(window, text='Class: ').grid(row=9, column=0, pady=5)

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

    lb_book_name = MyLabel(return_window)
    lb_author = MyLabel(return_window)
    entry_book_id = MyEntry(return_window, width=20)
    find_student = Button(return_window, text='Find student', font=FONT_SMALL, command=keypress_event)
    
    lb_member_name = MyLabel(return_window)
    lb_member_class = MyLabel(return_window)
    entry_member_id = MyEntry(return_window, width=20)
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
        returned = db.return_book(entry_book_id.val())
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
            entry_book_id.val(), entry_member_id.val())

        # row form: [book_id, book, author, issued_by, student_name, class]
        if not row:
            msg='Either the entered book is not issued\nOr the given member has not\nissued any books currently'
            row = ['' for _ in range(6)]
            messagebox.showwarning(title='Error', message=msg)
            return_window.lift(root)

        entry_book_id.set_val(row[0])
        entry_member_id.set_val(row[3])
        lb_book_name.configure(text=row[1])
        lb_author.configure(text=row[2])
        lb_member_name.configure(text=row[4])
        lb_member_class.configure(text=row[5])

def issue_book():
    '''Issue book window'''
    issue_window = Toplevel(root)
    issue_window.title('Issue new Book')
    issue_window.geometry("380x450+400+220")
    issue_window.resizable(False, False)
    
    fill_non_specific_info(issue_window)

    lb_book = MyLabel(issue_window)
    lb_author = MyLabel(issue_window)
    lb_member = MyLabel(issue_window)
    lb_class = MyLabel(issue_window)

    entry_book_id = MyEntry(issue_window, width=20)
    entry_member_id = MyEntry(issue_window, width=20)
    
    entry_book_id.bind("<KeyRelease>", 
        lambda e: fill_details(TABLE_BOOKS, e, lb_book, lb_author))
    entry_member_id.bind("<KeyRelease>", 
        lambda e: fill_details(TABLE_MEMBERS, e, lb_member, lb_class))
    
    btn_issue = Button(issue_window, text='Issue Book', width=25, font=BTN_FONT, 
        command=lambda: issue_book_in_db())

    entry_book_id.grid(row=1, column=1, pady=5,sticky=W, ipady=2)
    lb_book.grid(row=2, column=1, pady=5)
    lb_author.grid(row=3, column=1, pady=5)
    entry_member_id.grid(row=6, column=1, pady=5,sticky=W, ipady=2)
    lb_member.grid(row=8, column=1, pady=5)
    lb_class.grid(row=9, column=1, pady=5)
    btn_issue.grid(row=11, column=0, columnspan=2, padx=30, pady=25)

    def fill_details(table, e, label1, label2):
        col1, col2 = db.fill_issue_details(table, e.widget.val())
        label1.configure(text=col1)
        label2.configure(text=col2)

    def issue_book_in_db():
        book_id = entry_book_id.val()
        mem_id = entry_member_id.val()

        issued = db.issue_book(book_id, mem_id)
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

    entry_id = MyEntry(edit_window, width=28)
    entry_name = MyEntry(edit_window, width=28)
    entry_author = MyEntry(edit_window, width=28)
    drp_genre = OptionMenu(edit_window, var_genre, *GENRES)
    drp_genre.config(font=FONT_SMALL)
    
    entry_id.bind('<KeyRelease>', lambda e:fill_details())
    
    btn_fr = Frame(edit_window)
    btn_fr.grid(row=5, column=0, columnspan=2, pady=20)
    btn_update = Button(btn_fr, text='Update', width=12, font=BTN_FONT, 
        command=lambda: update_book())
    btn_delete = Button(btn_fr, text='Delete', width=12, font=BTN_FONT, 
        command=lambda: delete_book())
    btn_update.grid(row=0, column=0, padx=20)
    btn_delete.grid(row=0, column=1)

    drp_genre.grid(row=4, column=1)
    entry_id.grid(row=1, column=1, pady=10, ipady=3)
    entry_name.grid(row=2, column=1, pady=10, ipady=3)
    entry_author.grid(row=3, column=1, pady=10, ipady=3)

    Label(edit_window, text=' '*7+'Update / Delete Book', font=FONT_BIG).grid(
        row=0, column=0, columnspan=2, pady=10)
    MyLabel(edit_window, text='Book Id:').grid(row=1, column=0, pady=10, padx=30)
    MyLabel(edit_window, text='Name:').grid(row=2, column=0, pady=10)
    MyLabel(edit_window, text='Author:').grid(row=3, column=0, pady=10)
    MyLabel(edit_window, text='Genre:').grid(row=4, column=0, pady=10)

    def fill_details():
        book_id = entry_id.val()
        name, author, genre = db.fill_column_details(TABLE_BOOKS, book_id)
        entry_name.set_val(name)
        entry_author.set_val(author)
        var_genre.set(genre)

    def update_book():
        book_id = entry_id.val()
        name = entry_name.val()
        author = entry_author.val()
        genre = var_genre.get()

        if book_id and name and author:
            updated = db.update_column(TABLE_BOOKS, book_id, name, author, genre)
            if updated:
                messagebox.showinfo(title='Success',
                    message='Book details have been Updated.')
                edit_window.destroy()
                return

        messagebox.showerror(title='Error',
            message='Please enter proper values.')
        edit_window.lift(root)

    def delete_book():
        book_id = entry_id.val()
        deleted = db.delete_column(TABLE_BOOKS, book_id)
        if deleted:
            messagebox.showinfo(title='Success',
                message='The Book has been deleted.')
            edit_window.destroy()
        else:
            messagebox.showerror(title='Error',
                message='There was some problem.\nTry again later.')
            edit_window.lift(root) 

def add_new_book():
    '''Add a new book window'''
    add_window = Toplevel(root)
    add_window.title('Add New Book')
    add_window.geometry("400x290+400+220")
    add_window.resizable(False, False)

    genre = StringVar(add_window)
    genre.set(GENRES[0])

    lb_title = Label(add_window, text='Add New Book', font=FONT_BIG)
    lb_name = MyLabel(add_window, text='Name:')
    lb_author = MyLabel(add_window, text='Author:')
    lb_genre = MyLabel(add_window, text='Genre:')
    
    entry_name = MyEntry(add_window, width=30)
    entry_author = MyEntry(add_window, width=30)
    drp_genre = OptionMenu(add_window, genre, *GENRES)
    drp_genre.config(font=FONT_SMALL)

    btn_submit = Button(add_window, text='Submit', width=25, font=BTN_FONT, 
        command=lambda: add_to_db())

    lb_title.grid(row=0, column=0, columnspan=3, pady=10)
    lb_name.grid(row=1, column=0, pady=10)
    entry_name.grid(row=1, column=1, pady=10, ipady=3, columnspan=2)
    lb_author.grid(row=2, column=0, pady=10)
    entry_author.grid(row=2, column=1, pady=10, ipady=3, columnspan=2)
    lb_genre.grid(row=3, column=0, padx=15, pady=10)
    drp_genre.grid(row=3, column=1)

    btn_submit.grid(row=4, column=0, columnspan=3, padx=30, pady=30)

    def add_to_db():
        name = entry_name.val()
        author = entry_author.val()
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

    entry_name = MyEntry(add_mem_window, width=20)
    entry_class = MyEntry(add_mem_window, width=20)
    entry_section = MyEntry(add_mem_window, width=20)

    entry_name.grid(row=1, column=1, ipady=3)
    entry_class.grid(row=2, column=1, ipady=3)
    entry_section.grid(row=3, column=1, ipady=3)

    btn_submit = Button(add_mem_window, text='Submit', width=25, font=BTN_FONT,
         command=lambda: add_to_db())

    btn_submit.grid(row=4, column=0, columnspan=2, padx=25, pady=20)
    Label(add_mem_window, text='Add New Member', font=FONT_BIG).grid(
        row=0, column=0, pady=10, columnspan=2)
    MyLabel(add_mem_window, text='Name:').grid(
        row=1, column=0, pady=10, padx=25)
    MyLabel(add_mem_window, text='Class:').grid(
        row=2, column=0, pady=10)
    MyLabel(add_mem_window, text='Section: ').grid(
        row=3, column=0, pady=10)

    def add_to_db():
        name = entry_name.val()
        clss = entry_class.val() + ' ' + entry_section.val().upper()
        
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

    entry_id = MyEntry(edit_mem_window, width=20)
    entry_name = MyEntry(edit_mem_window, width=20)
    entry_class = MyEntry(edit_mem_window, width=20)
    entry_section = MyEntry(edit_mem_window, width=20)
    entry_date = MyEntry(edit_mem_window, width=20)

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
    MyLabel(edit_mem_window, text='Id:').grid(
        row=1, column=0, pady=10)
    MyLabel(edit_mem_window, text='Edit Name:').grid(
        row=2, column=0, pady=10)
    MyLabel(edit_mem_window, text='Edit Class:').grid(
        row=3, column=0, pady=10, padx=35)
    MyLabel(edit_mem_window, text='Edit Section:').grid(
        row=4, column=0, pady=10)
    MyLabel(edit_mem_window, text='Edit Date of\nJoining:\n(YYYY-MM-DD)').grid(
        row=5, column=0, pady=10)

    def fill_details():
        mem_id = entry_id.val()
        name, clss, date = db.fill_column_details(TABLE_MEMBERS, mem_id)

        clss = clss.split(maxsplit=1) if clss else ['','']
        entry_name.set_val(name)
        entry_class.set_val(clss[0])
        entry_section.set_val(clss[-1])
        entry_date.set_val(date)

    def update_member():
        mem_id = entry_id.val()
        name = entry_name.val()
        clss = entry_class.val() + ' ' + entry_section.val()
        date = entry_date.val()
        
        if mem_id and name and clss and date:
            updated = db.update_column(TABLE_MEMBERS, mem_id, name, clss, date)
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
        mem_id = entry_id.val()
        deleted = db.delete_column(TABLE_MEMBERS, mem_id)
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

    entry_id = MyEntry(members_window, width=6)
    entry_name = MyEntry(members_window, width=28)
    entry_class = MyEntry(members_window, width=10)

    Label(members_window, text='Library Members', font=FONT_REALLY_BIG).grid(
        row=0, column=0, columnspan=3, pady=15)
    MyLabel(members_window, text='Search by Id:').grid(
        row=1, column=0)
    MyLabel(members_window, text='Search by Name:').grid(
        row=1, column=1, pady=2)
    MyLabel(members_window, text='Search by Class:').grid(
        row=1, column=2, pady=2)
    entry_id.grid(row=2, column=0, ipady=2, padx=10)
    entry_name.grid(row=2, column=1, ipady=2, padx=10, pady=10)
    entry_class.grid(row=2, column=2, ipady=2, padx=10)

    event_click = lambda e: populate_table()
    entry_id.bind('<KeyRelease>', event_click)
    entry_name.bind('<KeyRelease>', event_click)
    entry_class.bind('<KeyRelease>', event_click)

    def populate_table():
        mem_id = entry_id.val()
        name = entry_name.val()
        clss = entry_class.val()

        cols = ['member_id', 'name', 'class', 'date']
        col_names = ['Member Id', 'Name', 'Class', 'Join Date']
        widths = [100, 250, 100, 120]

        tree = MyTree(members_window, row=3, column=0, columnspan=3, padx=20, pady=10)
        tree.set_columns(columns=cols, headings=col_names, widths=widths)
        
        data = db.get_members(mem_id, name, clss)
        tree.insert_data(data)

    populate_table()

'''Home page'''
root = Tk()
root.title('Library Management System')
root.geometry("900x380+350+200")
root.resizable(False,False)
root.configure(bg=COLOR)

app_title = Label(root, text='Library Management\nSystem', bg=COLOR, font=FONT_REALLY_BIG)

issue_btn = HomeButton(root, text='Issue Book', command=issue_book)
return_btn = HomeButton(root, text='Return Book', command=return_book)
show_btn = HomeButton(root, text='Show Issued Books', command=show_issued_books)
search_btn = HomeButton(root, text='Search for Books', command=search_books)
add_btn = HomeButton(root, text='Add New Book', command=add_new_book)
edit_btn = HomeButton(root, text='Update/Delete Book', command=edit_book)
show_members_btn = HomeButton(root, text='Show All Members', command=show_members)
add_member_btn = HomeButton(root, text='Add a Member', command=add_member)
edit_member_btn = HomeButton(root, text='Update/Delete Member', command=edit_member)

Label(root, text='Issue & Return\nBooks', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=1)
Label(root, text='Manage\nBooks', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=0)
Label(root, text='Manage\nMembers', font=FONT_BIG, bg=COLOR, fg=CLR_GRAY).grid(row=1, column=2)

app_title.grid(row=0, column=1, columnspan=1, pady=25)
issue_btn.set_grid(row=2, column=1)
return_btn.set_grid(row=3, column=1)
show_btn.set_grid(row=4, column=1)
search_btn.set_grid(row=2, column=0)
add_btn.set_grid(row=3, column=0)
edit_btn.set_grid(row=4, column=0)
show_members_btn.set_grid(row=2, column=2)
add_member_btn.set_grid(row=3, column=2)
edit_member_btn.set_grid(row=4, column=2)

try:
    PASSWD = sys.argv[1]
    db.new_connection(passwd=PASSWD)
    root.mainloop()
    db.close_connection()
except:
    messagebox.showwarning(title='Error',
        message='Could not connect to the database.')