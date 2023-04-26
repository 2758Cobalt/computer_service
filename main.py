from init import *
from mysql_client import *
from windows import *

def refresh_event(query_command):
    rewriting_arrives(sys_rows,sys_columns,root_connection.query(query_command))
    
    root_table.refresh()

#=================================
root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")
#=================================

window_connection(root)



file_menu = Menu(root)
file_menu.add_cascade(label="Підключення до другої бд",command=lambda: window_connection(root))



ttk.Label(text="Обрана таблиця",background="#2f2f2f",foreground="white").pack(anchor=NW,pady=5,padx=5)



table_selection = ttk.Entry(root)
table_selection.pack(anchor=NW,pady=5,padx=5)

sys_rows= [] # Список, який містить рядки таблиці
sys_columns = [] # Список, який містить колонки таблиці


root_table = Table(root,sys_columns,sys_rows)
root_table.pack(fill=BOTH,expand=1,padx=10,pady=20)

ttk.Label(text="Елементи управління",background="#2f2f2f",foreground="white").pack(anchor=N)

frame = Frame(root,bg="#2f2f2f")
frame.pack(expand=1,anchor='center',pady=20,padx=20)



ttk.Button(frame,text="Оновити таблицю",width=32,
           command=lambda: (refresh_event(f"select * from {table_selection.get()}"))
           ).grid(row=0,column=0,pady=30,padx=10)
ttk.Button(frame,text="Додати нову таблицю до бд",width=32,command=lambda: window_create_table(root)).grid(row=0,column=1,pady=30,padx=10)
ttk.Button(frame,text="Видалити таблицю",width=32,command=lambda: window_drop_table(root)).grid(row=0,column=2,pady=30,padx=10)

ttk.Button(root,text="Відключитися від бази даних",width=32,command=lambda: (root_connection.connection.close(), exit())).pack(anchor=S,pady=20) # Disconnect


#=================================
root.config(menu=file_menu)
root.mainloop()
#=================================
