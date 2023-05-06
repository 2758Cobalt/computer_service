from init import *
from mysql_client import *
from windows import *


def refresh_event(query_command):
    """Используется для привязки отправки запроса после срабатывания кнопки кнопки"""

    rewriting_arrays(sys_rows,sys_columns,root_connection.query(query_command)) # rewriting arrays

    root_table.refresh() # refresh

#=================================
root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")
#=================================

sys_rows = [] # table rows
sys_columns = [] # table columns

#=============Menu================
file_menu = Menu(root) # window menu bar


#=============add_cascade=========
file_menu.add_cascade(label="Файл",command=lambda: refresh_event(query_pricelist))

tabs_nb = ttk.Notebook(root)

#=============Frame===============
main_frame = Frame(tabs_nb,bg="#2f2f2f") # main frame
clients_frame = Frame(tabs_nb,bg="#2f2f2f") # clients frame
order_frame = Frame(tabs_nb,bg="#2f2f2f") # order frame
delivery_frame = Frame(tabs_nb,bg="#2f2f2f") # delivery frame
works_frame = Frame(tabs_nb,bg="#2f2f2f") # delivery frame

buttons_frame = Frame(root,bg="#3f3f3f")


window_connection(root) # Callback window of connection


#=============Table===============
root_table = Table(main_frame,sys_columns,sys_rows)

#============package==============
main_frame.pack(expand=1,anchor='center',fill=BOTH,pady=20,padx=20) # main frame

root_table.pack(fill=BOTH,expand=1,padx=10,pady=10) # Table

tabs_nb.pack(expand=1,fill=BOTH) # tab

buttons_frame.pack(expand=1,anchor='center',fill=BOTH,pady=20,padx=10) # main btn frame

tabs_nb.add(main_frame,text="Прайс-лист")
tabs_nb.add(clients_frame,text="Клієнти")
tabs_nb.add(order_frame,text="Прийняття заяв")
tabs_nb.add(delivery_frame,text="Доставлення устаткування")
tabs_nb.add(works_frame,text="Виїздні роботи")
#============button===============

ttk.Button(buttons_frame,text="Оновити таблицю",width=32,command=lambda: refresh_event(query_pricelist)
).grid() # Refresh

ttk.Button(buttons_frame,text="Відключитися",width=32,command=lambda: (root_connection.connection.close(), root.quit())
).grid(column=1,row=0) # Disconnect


#============binds================
#Balloon(root).bind(,"")


#=================================
root.protocol("WM_DELETE_WINDOW",lambda:(root_connection.connection.close(),root.quit()))
root.config(menu=file_menu)
root.mainloop()
#=================================


#table_menu = Menu(tearoff=0) # rmb functional menu :25
#etest_menu = Menu(root,tearoff=0) :26
#etest_menu.add_command(label="test"):34
#file_menu.add_cascade(label="Test",menu=etest_menu):35
#file_menu.add_cascade(label="Connect to another database",command=lambda: window_connection(root)) :39