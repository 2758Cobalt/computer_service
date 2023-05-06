from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=["root","localhost:3306","","world"]) # default | test
    
# =============================================================
def window_connection(root_window): # window
    root_window.withdraw()
    new_window = Tk("database_connection")
    new_window.resizable(0,0)
    new_window.geometry("300x300+256+256")
    new_window.title("Connect")
    new_window.configure(background="#1f1f1f")

    for idx,x in enumerate(["User","Host","Password","Database"]):
        Label(new_window,text=x,background="#2f2f2f",foreground="white",width=16,anchor="s").grid(row=idx,column=0,pady=5) # Позиціювання елементів 

    user = ttk.Entry(new_window) # Поле "користувач"
    host = ttk.Entry(new_window) # Поле "хост"
    password = ttk.Entry(new_window,show="*") # Поле "пароль"
    database = ttk.Entry(new_window) # Поле "база даних"

    for idx, data in enumerate([user,host,password,database]):
        data.insert(0,connect_config[idx]) # Заповнення полів за замовчуванням (щоб не вводити усі дані вручну)
        data.grid(row=idx,column=1,pady=5) # Позиціювання елементів

    ttk.Button(new_window,text="Підключитися до бази даних",width=32, # Кнопка
command=lambda: (
    # Отримання введених даних
    root_connection.change_data(user=user.get(),host=host.get(),password=password.get(),database=database.get()), 
                root_connection.connect(), # Підключення
                new_window.destroy(),root_window.deiconify()) # Видаленя вікна 
).place(anchor=S,relx=0.5,rely=0.95) # Позиціювання елементів
    
    new_window.protocol("WM_DELETE_WINDOW",lambda: root_window.quit())# Quit
# =============================================================

def rewriting_arrays(rows,columns,connection):
    """Перезапись массивов"""
    rows.clear()
    columns.clear()
    for x in connection[0]:
        rows.append(x)
    for x in connection[1]:
        columns.append(x[0])
    return (rows,columns)