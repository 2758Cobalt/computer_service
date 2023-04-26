from init import *

sys_execute_arrive = []

class MySql_connection:
    def __init__(self,connection_data):
        self.connection_data = connection_data
        self.columns = []
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
        except Error as e:
            print(e)
            if (e.errno != -1):messagebox.showerror("Error",e)

    def get_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("show tables;")
            for info in cursor:
                self.columns.append(info)
            return self.columns

    def query(self,query=""):
        
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
            finally:
                self.connection.close()
