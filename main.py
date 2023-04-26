from init import *
from mysql_client import *
from core import *


root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")


file_menu = Menu(root)
file_menu.add_cascade(label="Подключение к базе данных",command=window_connection) # messagebox.showinfo("Database", "Option connect to db")
file_menu.add_cascade(label="Прайс-лист")


ttk.Label(text="Текущая таблица").pack(anchor=NW,pady=5,padx=5)


tables = ["book"]

table_selection = ttk.Combobox(root,values=tables)
table_selection.current(0)
table_selection.pack(anchor=NW,pady=5,padx=5)


query_show = (f"select * from {table_selection.get()}")
sys_rows= [] # list rows in table
sys_columns = [] # list columns(headers) in table

sys_widget_table = Table(root,sys_columns,sys_rows)
sys_widget_table.pack(fill=BOTH,expand=1,padx=10,pady=20)

frame = Frame(root,bg="#3f3f3f")
frame.pack(expand=1,anchor=S,fill=BOTH,pady=10,padx=10)




ttk.Button(frame,text="Оновити таблицю",width=32,# refresh
           command=lambda: 
               (rewriting_arrives( sys_rows,
                      sys_columns,
                      root_connection.query(query_show)),
                sys_widget_table.refresh())
).pack(anchor=S,pady=10)



root.config(menu=file_menu)
root.mainloop()