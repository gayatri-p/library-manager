from tkinter import *
from tkinter import ttk

COLOR = '#f6f6f6'
CLR_GRAY = '#5d5d66'

FONT_ENTRY = ('verdana',10,'bold')
BTN_FONT = ('arial',15,'bold')
FONT_BIG = ('arial',15,'bold')
FONT_SMALL = ('arial',12,'bold')
FONT_REALLY_BIG = ('arial',19,'bold')

class HomeButton(Button):
    def __init__(self, parent, **options):
        Button.__init__(self, parent, options, relief=GROOVE, font=BTN_FONT, width=20, bg=COLOR)

    def set_grid(self, **kwargs):
        self.grid(kwargs, pady=10, padx=25)

class MyEntry(Entry):
    def __init__(self, parent, **options):
        Entry.__init__(self, parent, options, font=FONT_ENTRY)
    
    def val(self):
        return self.get().strip()
    
    def set_val(self, val):
        self.delete(0, END)
        self.insert(0, val)

class MyLabel(Label):
    def __init__(self, parent, **options):
        Label.__init__(self, parent, options, font=FONT_SMALL)

class MyTree(ttk.Treeview):
    def __init__(self, parent, **options):
        self.tree_frame = Frame(parent)
        self.tree_frame.grid(options)
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.config(command=self.tree.yview)
        self.tree.pack(expand=True)

    def set_columns(self, columns, headings, widths):
        self.tree['columns'] = tuple(columns)
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.heading('#0', text='')

        for column, heading, width in zip(columns, headings, widths):
            self.tree.column(column, anchor=CENTER, width=width)
            self.tree.heading(column, text=heading)

    def insert_data(self, data):
        i = 0
        for row in data:
            self.tree.insert(parent='', index='end', iid=i, text='', value=row)
            i += 1