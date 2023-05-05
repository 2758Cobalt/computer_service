from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=["Cobalt","localhost:2525","Umsf_sqltutor","test_db"]) # default | test
    
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

    ttk.Button(new_window,text="Connect to database",width=32, # Кнопка
command=lambda: (
    # Отримання введених даних
    root_connection.change_data(user=user.get(),host=host.get(),password=password.get(),database=database.get()), 
                root_connection.connect(), # Підключення
                new_window.destroy(),root_window.deiconify()) # Видаленя вікна 
).place(anchor=S,relx=0.5,rely=0.95) # Позиціювання елементів
    
    new_window.protocol("WM_DELETE_WINDOW",lambda: root_window.quit())# Quit
# =============================================================
def window_table_config(root_window,operation): # window
    table = Tk("tables")
    table.resizable(0,0)
    table.geometry("300x300")
    table.configure(background="#1f1f1f")
    #=============if operation == add | create window with additing function table
    if operation == "add":
        table.title("Table creation")
        ttk.Label(table,text="Name of new table",background="#2f2f2f",foreground="white",width=28,anchor="s").pack(anchor="center",pady=5) # Label

        new_table_name = ttk.Entry(table) # TextField of new table

        new_table_name.pack(anchor=S,pady=5)
        ttk.Button(table,text="Create table",width=32,
    command=lambda: (root_connection.query(f"""create table {new_table_name.get()} (`{new_table_name}id` int primary key auto_increment);"""),table.destroy())
    ).place(anchor=S,relx=0.5,rely=0.95)
    #=============if operation == remove, create window with removing function table
    elif operation == "remove":
        table.title("Removing table")

        ttk.Label(table,text="Table name",background="#2f2f2f",foreground="white",width=28,anchor="s").pack(anchor="center",pady=5) # Label

        table_name = ttk.Entry(table)
        table_name.pack(anchor=S,pady=5)

        ttk.Button(table,text="Remove table",width=32,command=lambda:(
                root_connection.query(f"drop table {table_name.get()};" ),
                table.destroy(),
                root_window.deiconify() ) ).place(anchor=S,relx=0.5,rely=0.95)

    table.protocol("WM_DELETE_WINDOW",lambda: (root_window.deiconify(), table.destroy())) # Quit
# =============================================================

def rewriting_arrives(rows,columns,connection):
    """Перезапись массивов"""
    rows.clear()
    columns.clear()
    for x in connection[0]:
        rows.append(x)
    for x in connection[1]:
        columns.append(x[0])
    return (rows,columns)
"""
def window_drop_table(root_window): # window
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
    
    drop_table.protocol("WM_DELETE_WINDOW",lambda: (drop_table.destroy()))# Quit"""