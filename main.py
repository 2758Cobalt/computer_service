from init import *
from mysql_client import *
from core import *
root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")



file_menu = Menu()
file_menu.add_cascade(label="Connect to database",command=window_connection)# messagebox.showinfo("Database", "Option connect to db")

frame = Frame(root,bg="#3f3f3f")
frame.pack(expand=1,anchor=N,fill=X)

ttk.Button(root,text="Exit",width=16,command=lambda: exit()).pack(anchor=SE)

#ttk.Button(root,text="Refresh",width=16,command=).pack(anchor=NE) # refresh






root.config(menu=file_menu)
root.mainloop()

#messagebox.showinfo("title", "desc")