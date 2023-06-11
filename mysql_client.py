from init import *

sys_execute_arrive = []

class MySql_connection:
    def __init__(self,connection_data):
        self.connection_data = connection_data
        self.status = False
        
    def change_data(self,user,host,password,database):
        self.connection_data.insert(0,user)
        self.connection_data.insert(1,host)
        self.connection_data.insert(2,password)
        self.connection_data.insert(3,database)
        return self.connection_data
    
    def connect(self):
        try:
            self.connection = connect(
                user=self.connection_data[0],
                host=self.connection_data[1][:9],
                port=self.connection_data[1][-4:],
                password=self.connection_data[2],
                database=self.connection_data[3])
            self.status = True
            l.info(f"Login...\n{self.connection_data}") # Log connect

        except Error as e:
            l.error(f"{e} \nCode: {e.errno}") # Log error
            if e.errno == 2003: # Host Failed
                l.error("Host is failed") # Log error
                messagebox.showerror("Помилка","Невірно ведений хост!")
            
            elif e.errno == 1045: # User or Passowrd Failed
                l.error("User or password is failed") # Log error
                messagebox.showerror("Помилка","Невірно ведене ім'я користувача або пароль. Перевірте введені дані")
                
            elif e.errno == 1049: # Database Failed 
                l.error(f"Database name is failed") # Log error
                messagebox.showerror("Помилка","Введеної бази даних не існує на сервері.\nМожливо назва бази введена неправильно")
                

    def query(self,query="",commit=False):
        sys_execute_arrive.clear()
        if self.status == False: 
            l.error("Database has't been connected")
            messagebox.showerror("Помилка","База даних не підключена.\nОновити табилицю неможливо")
        else:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    l.info(f"Query: {query}")
                    for info in cursor:
                        sys_execute_arrive.append(info) # Answer
                    cursor.close()
                    self.connection.commit()
                return (sys_execute_arrive,cursor.description)

            except Error as e:
                l.error(e)
                
                if e.errno == 1406:
                    l.error(f"Data too long") # Log error
                    messagebox.showerror("Помилка","Перевірте правильність даних")
                
                elif e.errno == 1265:
                    l.error(f"Data truncated") # Log error
                    messagebox.showerror("Помилка","У полі \"Послуга\" задана не існуюча послуга")
                
                else: messagebox.showerror("Помилка",e)
    

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple(),):
        super().__init__(parent)
        style = Style()
        style.configure("Treeview",background="red",foreground="black",rowheight=50, fieldbackground="white")
        table = Treeview(self, show="headings", selectmode="browse")
        style.theme_use("alt")
        scrollbar_x = Scrollbar(self, orient=HORIZONTAL,command=table.xview) # horizontal scrollbar
        scrollbar_y = Scrollbar(self,command=table.yview) # vertical scrollbar
        table.configure(xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        table.pack(expand=True, fill='both')

        self.table = table
        self.headings = headings
        self.rows = rows

    def refresh_table(self):
        try:
            self.table.delete(*self.table.get_children())
            self.table["columns"] = self.headings
            for header in self.headings:
                self.table.heading(header,text=header,anchor="center")
                self.table.column(header,anchor="center")
            for row in self.rows:
                self.table.insert('','end',values=row)

        except Exception as e:
            l.error(e)
            messagebox.showwarning("Увіга","Виникла помилка при оновлені таблиці")
