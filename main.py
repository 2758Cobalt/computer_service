from init import *
from mysql_client import *
from core import *

root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")


people = [("Tom", 38, "tom@email.com"), ("Sam", 28, "sam@email.com")] # example


file_menu = Menu()
file_menu.add_cascade(label="Connect to database",command=window_connection) # messagebox.showinfo("Database", "Option connect to db")


headers_a = ["col1","col2","col3"]


table_a = ttk.Treeview(root,show="headings")
table_a.pack(fill=BOTH,expand=1,padx=10,pady=20)


frame = Frame(root,bg="#3f3f3f")
frame.pack(expand=1,anchor=N,fill=X)


ttk.Button(frame,text="Refresh",width=16,command=lambda: refresh_table(table=table_a,headers=headers_a,table_data=people) ).pack(anchor=NE) # refresh
ttk.Button(frame,text="Exit",width=16,command=lambda: exit()).pack(anchor=SE)









root.config(menu=file_menu)
root.mainloop()

#messagebox.showinfo("title", "desc")