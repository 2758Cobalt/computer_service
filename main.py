from init import *
from mysql_client import *
from core import *
from random import randint

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple(),):
        super().__init__(parent)
        print(f"TableOptions_initialize ({self}).\nheaders -> {headings}\nRows -> {rows} ")

        table = ttk.Treeview(self, show="headings", selectmode="browse")

        scrollbar_x = Scrollbar(self, orient=HORIZONTAL,command=table.xview)
        scrollbar_y = Scrollbar(self,command=table.yview)
        table.configure(xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        table.pack(expand=True, fill=BOTH)

        self.table = table
        self.headings = headings
        self.rows = rows

    def refresh(self):
        try:
            self.table.delete(*self.table.get_children())
            self.table["columns"] = self.headings

            for header in self.headings:
                self.table.heading(header,text=header,anchor="center")
                self.table.column(header,anchor="center")

            for row in self.rows:
                self.table.insert('','end',values=row)

        except Exception as e:
            print(e)


root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")


file_menu = Menu(root)
file_menu.add_cascade(label="Connect to database",command=window_connection) # messagebox.showinfo("Database", "Option connect to db")
file_menu.add_cascade(label="None")



test_row = [("Tom", 38, "tom@email.com"), ("Sam", 28, "sam@email.com")] # example
test_column = ["col1","col2","col3"]

sys_widget_table = Table(root,test_column,test_row)
sys_widget_table.pack(fill=BOTH,expand=1,padx=10,pady=20)

frame = Frame(root,bg="#3f3f3f")
frame.pack(expand=1,anchor=N,fill=X)









ttk.Button(frame,text="Refresh",width=16,command=lambda: sys_widget_table.refresh() ).pack(anchor=NE) # refresh
ttk.Button(frame,text="Exit",width=16,command=lambda: exit()).pack(anchor=SE)
ttk.Button(frame,text="Test",width=16,command=lambda: (test_column.append(str(randint(0,100)))) ).pack(anchor=SE)





root.config(menu=file_menu)

root.mainloop()

#messagebox.showinfo("title", "desc")