from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk
from Pmw import Balloon
from os import  system as sys
from mysql.connector import connect, Error

connect_config = ("Cobalt","localhost:2525","Umsf_sqltutor","course_database") # Default variable

# Clean console
sys('cls')


# constains
app_title = "Комп'ютер-Сервіс"
app_resolution = [800,600]
app_screen = str(app_resolution[0]) + "x" + str(app_resolution[1])
"""
Docs | Rules
1. Комментарии кода пишутся с отступом (# comment), а участки закоммент. кода - без отсупа (#code);
2. Название переменных оформляется : удобное название _ названием виджета (variable_menu, variable_table, variable_frame);
3. Переменные с параметрами (title,width) оформляются также, как в правиле (2.);
4. Для отделения целых блоков используется #========== разделитель с одинаковой длинной, сверху и снизу блока (куска кода);
5. Язык программы по-умолчанию eng. На этапе разработки, комментарии должны быть переведены на eng.
"""

"""

TOP (по умолчанию, выравнивается по верхней стороне контейнера), 
BOTTOM (выравнивание по нижней стороне), 
LEFT (выравнивание по левой стороне), 
RIGHT (выравнивание по правой стороне).

Noth(север - вверх), 
South (юг - низ), 
East (восток - правая сторона), 
West (запад - левая сторона),
Center (по центру). Например, значение nw указывает на верхний левый угол

NW  N   NE
W   C   E
SW  S   SE

"""

query_clients = """select `client_id` as "Номер клієнту",`client_name` as "Им'я клієнта",
`client_surname` as "Призвище клієнта",`client_code` as "Код клієнта",
`client_register_date` as "Дата реєстрації клієнта" from `clients-data`"""

query_pricelist= """select `list_id` as "Номер листа",`service_price` as "Ціна обслуговування",
`repair_price` as "Ціна ремонту устаткування",`setup_software_price` as "Ціна встановлення програмного забезпечення" 
from `price-list`"""
