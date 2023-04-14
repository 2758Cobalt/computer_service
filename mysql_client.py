from init import *
from getpass import getpass

def connection_init(query=str(""),_host=str("localhost:2525"),_user=str("Cobalt"),_password=str("Umsf_sqltutor"),_database=str("world")):
    execute_arrive = []
    try:
        with connect(
            host=_host[:9],
            port=_host[-4:],
            user=_user,
            password=_password,
            database=_database
        
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for info in cursor:
                    print(info)
                    execute_arrive.append(info)
            return execute_arrive
        
    except Error as e: # Error panel
        print(e)
        if (e.errno != -1):
            messagebox.showerror("Error",e)
