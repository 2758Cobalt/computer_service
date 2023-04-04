from init import *
import mysql_client as m

def get_text(widget):
    m.connection_init(widget.get("1.0",END))

root = Tk()
root.title(app_title)
root.geometry(app_resolution)
root.configure(background="#1f1f1f")

file_menu = Menu()
file_menu.add_cascade(label="Connect to database",command=lambda: messagebox.showinfo("Database", "Option connect to db"))

btn = ttk.Button(text="clear",command=lambda: sys('cls'), padding=20).pack(side=BOTTOM,fill=X,padx= 10,pady=10) # clear

btn = ttk.Button(text="Execute",command=lambda: (sys('cls'), get_text(textfield)) ,padding=20).pack(side=BOTTOM,fill=X,padx= 10,pady=10) # execute



textfield = Text(height=6)
textfield.pack(fill=X,side=BOTTOM,pady=50)

root.config(menu=file_menu)
root.mainloop()