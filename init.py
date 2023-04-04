from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk
from os import  system as sys
from mysql.connector import connect, Error
#from mysql import


#packages
sys('cls')


# constains
app_title = "app"
app_resolution = "800x600"

"""
TOP (по умолчанию, выравнивается по верхней стороне контейнера), 
BOTTOM (выравнивание по нижней стороне), 
LEFT (выравнивание по левой стороне), 
RIGHT (выравнивание по правой стороне).
"""

"""
Noth(север - вверх), 
South (юг - низ), 
East (восток - правая сторона), 
West (запад - левая сторона),
Center (по центру). Например, значение nw указывает на верхний левый угол

NW  N   NE
W   C   E
SW  S   SE

C-center
"""