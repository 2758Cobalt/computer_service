from init import *

sys_execute_arrive = []

class MySql_connection:
    def __init__(self,connection_data):
        self.connection_data = connection_data
    def change_data(self,user,host,password,database):
        self.connection_data.insert(0,user)
        self.connection_data.insert(1,host)
        self.connection_data.insert(2,password)
        self.connection_data.insert(3,database)
        return self.connection_data
    def connect(self,query=""):
        try:
            self.connection = connect(
                user=self.connection_data[0],
                host=self.connection_data[1][:9],
                port=self.connection_data[1][-4:],
                password=self.connection_data[2],
                database=self.connection_data[3])
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    for info in cursor:
                        print(info)
                        sys_execute_arrive.append(info)
                return (sys_execute_arrive,cursor.description)
            finally:
                self.connection.close()
        except Error as e:
            print(e)
            if (e.errno != -1):messagebox.showerror("Error",e)
