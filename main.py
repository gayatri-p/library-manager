from tkinter import *
import dbConnect as db

BTN_FONT = ('arial',15,'bold')
FONT_ENTRY = ('verdana',10,'bold')


def show_books():
    show_window = Toplevel(root)
    show_window.title('All issued books')

def issue_book():
    issue_window = Toplevel(root)
    issue_window.title('Issue new Book')
    issue_window.geometry("380x350+400+220")
    a = StringVar()
    b = StringVar()

    issue_window.resizable(False, False)

    enteno = Entry(issue_window,textvariable=a,width=20,bg='yellow',fg='red',font=FONT_ENTRY)
    enteno.grid(row=1,column=1,pady=10,sticky=W)

    return





root = Tk()
root.title('Library Management System')
root.geometry("480x450+400+200")
root.resizable(False,False)

app_title = Label(root, text='Library Management System', font=BTN_FONT)

issue_btn = Button(root, text='Issue Book', font=BTN_FONT, width=30, command=issue_book)
return_btn = Button(root, text='Return Book', font=BTN_FONT, width=30)
search_btn = Button(root, text='Search Book', font=BTN_FONT, width=30)
add_btn = Button(root, text='Add New Book', font=BTN_FONT, width=30)
show_btn = Button(root, text='Show Issued Books', font=BTN_FONT, width=30, command=show_books)

app_title.pack(pady=20)
issue_btn.pack(pady=10)
return_btn.pack(pady=10)
search_btn.pack(pady=10)
add_btn.pack(pady=10)
show_btn.pack(pady=10)

root.mainloop()