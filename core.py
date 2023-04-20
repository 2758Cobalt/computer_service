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
                root_connection.connect("show tables;"), 
                new_window.destroy()) ).place(anchor=S,relx=0.5,rely=0.95)
