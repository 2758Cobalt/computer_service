from init import *
from mysql_client import *
    

def window():
    new_window = Tk("database_connection")
    new_window.resizable(0,0)
    new_window.geometry("300x300")
    new_window.title("Connect")
    for idx,x in enumerate(["Користувач","Хост","Пароль","База даних"]):
        Label(new_window,text=x,width=16,anchor="s").grid(row=idx,column=0,pady=5)# LabelElement

    user = ttk.Entry(new_window)
    host = ttk.Entry(new_window)
    password = ttk.Entry(new_window,show="*")
    database = ttk.Entry(new_window)
    
    user.insert(0,"Cobalt") # default
    host.insert(0,"localhost:2525")
    
    ttk.Button(new_window,text="Підключитися",width=32,command=lambda: (connection_init("",host.get(),user.get(),password.get(),database.get()), new_window.destroy() )  ).place(anchor=S,relx=0.5,rely=0.95)
    
    user.grid(row=0,column=1,pady=5) # user field
    host.grid(row=1,column=1,pady=5) # host field
    password.grid(row=2,column=1,pady=5) # passowrd field
    database.grid(row=3,column=1,pady=5) # database field
    
root = Tk("main")
root.title(app_title)
root.geometry(app_screen)
root.configure(background="#1f1f1f")

test = [("Tom", 38, "tom@email.com"),
        ("Bob", 42, "bob@email.com"),
        ("Sam", 28, "sam@email.com")]
columns = ("name", "age", "email")

tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(fill=BOTH, expand=1)

# определяем заголовки
tree.heading("name", text="Имя",anchor=W)
tree.heading("age", text="Возраст",anchor=W)
tree.heading("email", text="Email",anchor=W)

# добавляем данные
for person in test:
    tree.insert("", END, values=person)
    
file_menu = Menu()
file_menu.add_cascade(label="Connect to database",command=lambda: window())# messagebox.showinfo("Database", "Option connect to db")

frame = Frame(root,bg="#3f3f3f")
frame.pack(expand=1,anchor=N,fill=X)

ttk.Button(root,text="Exit",width=16,command=lambda: exit()).pack(anchor=SE)







root.config(menu=file_menu)
root.mainloop()

#messagebox.showinfo("title", "desc")