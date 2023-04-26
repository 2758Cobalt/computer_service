from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=["Cobalt","localhost:2525","Umsf_sqltutor","test_db"])

def window_connection(): # window
    new_window = Tk("database_connection")
    new_window.resizable(0,0)
    new_window.geometry("300x300")
    new_window.title("Connect")

    for idx,x in enumerate(["Користувач","Хост","Пароль","База даних"]):
        Label(new_window,text=x,width=16,anchor="s").grid(row=idx,column=0,pady=5)# LabelElement

    user = ttk.Entry(new_window)
    host = ttk.Entry(new_window)
    password = ttk.Entry(new_window,show="*")
    database = ttk.Entry(new_window)
    
    for idx, data in enumerate([user,host,password,database]):
        data.insert(0,connect_config[idx]) # default variable [test]
        data.grid(row=idx,column=1,pady=5) # user field

    ttk.Button(new_window,text="Підключитися",width=32,
command=lambda: (root_connection.change_data(user=user.get(),host=host.get(),password=password.get(),database=database.get()),
                root_connection.connect(),
                new_window.destroy()) ).place(anchor=S,relx=0.5,rely=0.95)

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple(),):
        super().__init__(parent)
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        scrollbar_x = Scrollbar(self, orient=HORIZONTAL,command=table.xview) # horizontal scrollbar
        scrollbar_y = Scrollbar(self,command=table.yview) # vertical scrollbar
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

    def add_column(self,header="NullHeader"):
        self.headings.append(header)

def rewriting_arrives(rows,columns,result):

    rows.clear()
    columns.clear()
    for x in result[0]:
        rows.append(x)
    for x in result[1]:
        columns.append(x[0])
    return (columns,rows)