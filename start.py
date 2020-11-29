from tkinter import *
import os
from tkinter import messagebox
import mysql.connector as sq

def login(e):
    passwd = entry.get().strip()
    try:
        db = sq.connect(host='localhost', user='root', password=passwd)
        root.destroy()
        os.chdir('data')
        os.system(f'python main.py {passwd}')
    except:
        messagebox.showinfo(title='Access Denied', message='The password is incorrect.')

FONT_BIG = ('arial',14,'bold')
FONT_SMALL = ('arial',12,'bold')
FONT_INP = ('verdana',11,'bold')

root = Tk()
root.title('User Authentication')
root.geometry('290x181+500+300')
COLOR='#d9ecff'
root.configure(bg=COLOR)

lbl = Label(root, text='Enter your\nMySQL password', bg=COLOR, font=FONT_BIG)
entry = Entry(root, width=20, font=FONT_INP)
btn = Button(root, text='Submit', font=FONT_SMALL, bg='#fff', command=lambda: login(1))

lbl.grid(row=0, column=0, pady=10, padx=10)
entry.grid(row=1, column=0, ipady=3, ipadx=3, pady=5, padx=30)
btn.grid(row=2, column=0, pady=20, padx=10)
entry.focus()
root.bind('<Return>', login)

root.mainloop()