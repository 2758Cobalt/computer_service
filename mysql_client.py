from init import *

sys_execute_arrive = []

class MySql_connection:
    def __init__(self,connection_data):
        self.connection_data = connection_data
        self.tables = []
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
            
            with self.connection.cursor() as cursor:
                cursor.execute("show tables")
                for table in cursor:
                    self.tables.append(table[0])
            
        except Error as e:
            print(e)
            if (e.errno != -1):messagebox.showerror("Error",e)

    def query(self,query=""):
        sys_execute_arrive.clear()
        self.tables.clear()
        if self.status == False: return messagebox.showerror("Виключення","База даних не підключена.\nОновити табилицю неможливо")
        else:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    
                    for info in cursor:
                        print(info)
                        sys_execute_arrive.append(info)
                return (sys_execute_arrive,cursor.description)
            except Error as e:
                print(e)
                if (e.errno != -1):messagebox.showerror("Error",e)


class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple(),):
        super().__init__(parent)
        style = ttk.Style()
        style.configure("Treeview",background="silver",foreground="black",rowheight=50,fieldbackground="white")
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        style.theme_use("alt")
        scrollbar_x = Scrollbar(self, orient=HORIZONTAL,command=table.xview) # horizontal scrollbar
        scrollbar_y = Scrollbar(self,command=table.yview) # vertical scrollbar
        table.configure(xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        table.pack(expand=True, fill=BOTH)

        self.table = table
        self.headings = headings
        self.rows = rows

    def refresh(self):
        try:
            self.table.delete(*self.table.get_children())
            self.table["columns"] = self.headings
            for header in self.headings:
                self.table.heading(header,text=header,anchor="center")
                self.table.column(header,anchor="center")
            for row in self.rows:
                self.table.insert('','end',values=row)
        except Exception as e:
            print(e)

    def add_column(self,header="NullHeader"):
        self.headings.append(header)