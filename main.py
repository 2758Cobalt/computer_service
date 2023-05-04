from init import *
from mysql_client import *
from windows import *
# course work
def refresh_event(query_command):
    if table_textfield.get() == "" or None: 
        messagebox.showwarning("Error","TextFielt current table is empty!\nEnter table name")
        table_textfield.focus() # Focus on field
    else:
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
file_menu.add_cascade(label="Connect to another database",command=lambda: window_connection(root)) # Menu bar

ttk.Label(text="Current table",background="#2f2f2f",foreground="white").pack(anchor=NW,pady=5,padx=5) # Label

#=================================
table_menu = Menu(tearoff=0)
table_menu.add_command(label="Add new table")
table_menu.add_command(label="Remove table")

frame_current_table = Frame(root)
table_textfield = ttk.Entry(frame_current_table) # TextField (Entry)

table_textfield.grid(pady=5,padx=5)

Button(frame_current_table,text="Edit",command= lambda:(table_menu.post(128,128))).grid(row=0,column=1,pady=5,padx=5) # Edit
frame_current_table.pack(expand=1,anchor=NW,pady=5,padx=5)
#=================================

sys_rows = [] # Список, який містить рядки таблиці
sys_columns = [] # Список, який містить колонки таблиці


root_table = Table(root,sys_columns,sys_rows)
root_table.pack(fill=BOTH,expand=1,padx=10,pady=20)

ttk.Label(text="Elements",background="#2f2f2f",foreground="white").pack(anchor=N)

frame = Frame(root,bg="#2f2f2f")
frame.pack(expand=1,anchor='center',pady=20,padx=20)


ttk.Button(frame,text="Update table",width=32,
           command=lambda: (refresh_event(f"select * from {table_textfield.get()}"))# Update
).grid(row=0,column=0,pady=30,padx=10)

ttk.Button(frame,text="Add new table",width=32,command=lambda: window_create_table(root)).grid(row=0,column=1,pady=30,padx=10) # New
ttk.Button(frame,text="Remove table",width=32,command=lambda: window_drop_table(root)).grid(row=0,column=2,pady=30,padx=10) # Remove

ttk.Button(root,text="Disconnect from the database",width=32,command=lambda: (root_connection.connection.close(), root.quit())).pack(anchor=S,pady=20) # Disconnect


#=================================
root.config(menu=file_menu)
root.mainloop()
#=================================
