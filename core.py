from init import *
from mysql_client import *

def window_connection():
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
            command=lambda: (connection("",host.get(),user.get(),password.get(),database.get()), new_window.destroy() )).place(anchor=S,relx=0.5,rely=0.95)
    return (user,host,password,database)

def refresh_table(table,headers,table_data):
    table["columns"] = headers
    
    for header in headers:
        table.heading(header,text=header,anchor="center")
        table.column(header,anchor="center")

    for row in table_data:
        table.insert('','end',values=row)