from init import *
from mysql_client import *
from windows import *

# course work

def refresh_event(query_command):
    if table_textfield.get() == "" or None: 
        messagebox.showwarning("Error","TextField \"current table\" is empty!\nEnter table name")
        table_textfield.focus() # Focus on field
    else:rewriting_arrives(sys_rows,sys_columns,root_connection.query(query_command))
    
    root_table.refresh()

def get_mouse(event):
    x = event.x_root
    y = event.y_root
    
    table_menu.post(x,y)

#=================================
root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")
#=================================
sys_rows = [] # Список, який містить рядки таблиці
sys_columns = [] # Список, який містить колонки таблиці

file_menu = Menu(root) # window menu bar
table_menu = Menu(tearoff=0) # rmb menu
frame = Frame(root,bg="#2f2f2f")
tb_select_frame = Frame(root,bg="#2f2f2f") # Table selection frame
table_textfield = ttk.Entry(tb_select_frame) # TextField (Entry)
root_table = Table(root,sys_columns,sys_rows) # root table
#etest_menu = Menu(root,tearoff=0)
window_connection(root) # Callback window of connection

#etest_menu.add_command(label="test")
#file_menu.add_cascade(label="Test",menu=etest_menu)

file_menu.add_cascade(label="Connect to another database",command=lambda: window_connection(root)) # Menu bar

table_menu.add_command(label="Add new table",command=lambda: window_table_config(root,"add"))
table_menu.add_command(label="Remove table",command=lambda: window_table_config(root,"remove"))
#=================================
ttk.Label(tb_select_frame,text="Current table",background="#2f2f2f",foreground="white").grid() # Label

table_textfield.grid(row=1,pady=5,padx=5)
table_textfield.bind("<Button-3>",get_mouse)

tb_select_frame.pack(expand=1,anchor=NW,pady=5,padx=5)
#=================================

root_table.pack(fill=BOTH,expand=1,padx=10,pady=20) # Table

ttk.Label(text="Elements",background="#2f2f2f",foreground="white").pack(anchor=N)

frame.pack(expand=1,anchor='center',pady=20,padx=20) # root frame

ttk.Button(frame,text="Update table",width=32,command=lambda: refresh_event(f"select * from {table_textfield.get()}") # Update
).grid(row=0,column=0,pady=30,padx=10)
ttk.Button(root,text="Disconnect from the database",width=32,command=lambda: (root_connection.connection.close(), root.quit())).pack(anchor=S,pady=20) # Disconnect


#=================================
root.protocol("WM_DELETE_WINDOW",lambda:(root_connection.connection.close(),root.quit()))
root.config(menu=file_menu)
root.mainloop()
#=================================
