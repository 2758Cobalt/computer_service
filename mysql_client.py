from init import *
from getpass import getpass
sys('cls')


def connection_init(query=str("")):
    try:
        with connect(
            host="localhost",
            user="root",
            password="Umsf_sqltutor",
            database="test_db"
        
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for info in cursor:
                    print(info)
            return connection
        
    except Error as e: # Error panel
        print(e)



