from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=["Cobalt","localhost:2525","Umsf_sqltutor","test_db"])
    
# =============================================================
def window_connection(root_window): # window
    root_window.withdraw()
    new_window = Tk("database_connection")
    new_window.resizable(0,0)
    new_window.geometry("300x300")
    new_window.title("Connect")

    for idx,x in enumerate(["User","Host","Password","Database"]):
        Label(new_window,text=x,width=16,anchor="s").grid(row=idx,column=0,pady=5) # Позиціювання елементів 

    user = ttk.Entry(new_window) # Поле "користувач"
    host = ttk.Entry(new_window) # Поле "хост"
    password = ttk.Entry(new_window,show="*") # Поле "пароль"
    database = ttk.Entry(new_window) # Поле "база даних"

    for idx, data in enumerate([user,host,password,database]):
        data.insert(0,connect_config[idx]) # Заповнення полів за замовчуванням (щоб не вводити усі дані вручну)
        data.grid(row=idx,column=1,pady=5) # Позиціювання елементів

    ttk.Button(new_window,text="Connect to database",width=32, # Кнопка
command=lambda: (
    # Отримання введених даних
    root_connection.change_data(user=user.get(),host=host.get(),password=password.get(),database=database.get()), 
                root_connection.connect(), # Підключення
                new_window.destroy(),root_window.deiconify()) # Видаленя вікна 
).place(anchor=S,relx=0.5,rely=0.95)# Позиціювання елементів
    
    new_window.protocol("WM_DELETE_WINDOW",lambda: root_window.quit())# Quit
# =============================================================

def window_create_table(root_window): # window
    root_window.withdraw()
    new_table = Tk("creation_tables")
    new_table.resizable(0,0)
    new_table.geometry("300x300")
    new_table.title("Table creation")
    
    ttk.Label(new_table,text="Назва таблиці",width=28,anchor="s").pack(anchor="center",pady=5)# Label
    
    new_table_name = ttk.Entry(new_table)

    new_table_name.pack(anchor=S,pady=5)
    ttk.Button(new_table,text="Create table",width=32,
command=lambda: (root_connection.query(f"""create table {new_table_name.get()} (`{new_table_name}id` int primary key auto_increment);"""),
                new_table.destroy(),
                root_window.deiconify())
            ).place(anchor=S,relx=0.5,rely=0.95)
    
    new_table.protocol("WM_DELETE_WINDOW",lambda: root_window.quit())# Quit
# =============================================================

def window_drop_table(root_window): # window
    root_window.withdraw()
    drop_table = Tk("drop_tables")
    drop_table.resizable(0,0)
    drop_table.geometry("300x300")
    drop_table.title("Removing table")
    
    ttk.Label(drop_table,text="Table name",width=28,anchor="s").pack(anchor="center",pady=5)# Label
    
    drop_table_name = ttk.Entry(drop_table)
    drop_table_name.pack(anchor=S,pady=5)
    
    ttk.Button(drop_table,text="Remove table",width=32,command=lambda:(
                root_connection.query(f"drop table {drop_table_name.get()};" ),
                drop_table.destroy(),
                root_window.deiconify() ) ).place(anchor=S,relx=0.5,rely=0.95)
    drop_table.protocol("WM_DELETE_WINDOW",lambda: root_window.quit())# Quit
# =============================================================
def rewriting_arrives(rows,columns,connection):

    rows.clear()
    columns.clear()
    for x in connection[0]:
        rows.append(x)
    for x in connection[1]:
        columns.append(x[0])
    
    return (rows,columns)
