from tkinter import Tk, Frame, Button, Label, Scrollbar, Menu
from tkinter.constants import *
import tkinter.messagebox as messagebox
from tkinter.ttk import Entry,Style,Treeview
from mysql.connector import connect, Error
from subprocess import Popen
from loguru import logger as l


tables = ["managers","clients","pricelist","proposals","performers"]

# constains
app_title = "Комп'ютер-Сервіс"
app_resolution = [720,500]
app_screen = str(app_resolution[0]) + "x" + str(app_resolution[1])
limit = 100

query_clients = """select `client_id` as "{}",`client_name` as "{}", `client_surname` as "{}",
`client_register_date` as "{}",`client_address` as "Адреса клієнта",`client_number_phone` as "{}", manager_manager_id as "{}" from `clients_data` order by client_id ASC LIMIT {};""".format(
    "Номер клієнту","Им'я клієнта","Призвище клієнта","Дата реєстрації клієнта","Номер телефону","Індекс обслуговуючого менеджера",limit)

query_pricelist = """select `list_id` as "{}",`service_price` as "{}",
`repair_price` as "{}",`setup_software_price` as "{}", `new_pc_price` as "{}", `performers_performers_id` as "{}", `manager_manager_id` as "{}" from `pricelist` order by list_id LIMIT {};""".format(
    "Номер послуги","Ціна обслуговування","Ціна ремонту устаткування","Ціна встановлення програмного забезпечення", "Ціна нового пк", "Код виконавця", "Код менеджера",limit)

query_proposals = """select proposal_id as "{}", proposal_type as "{}", proposal_register_date as "{}", performers_performer_id as "{}", clients_data_client_id as "{}"  from proposals order by proposal_id ASC LIMIT {};""".format(
    "Індекс послуги","Вид послуги","Дата замовлення послуги","Індекс виконавця цієї послуги", "Код клієнта-замовника",limit)

query_performers = """select performer_id as "{}",`performer_name` as "{}", `performer_surname` as "{}", performer_number_proposal as "{}", performer_startwork_date as "{}" from performers order by performer_id ASC LIMIT {};""".format(
    "Індекс виконавця","Ім'я виконавця","Прізвище виконавця","Номер виконуючого замовлення","Початок виконання замовлення",limit) # Наименнование колонок

query_managers = """SELECT manager_id as "{}", manager_name as "{}", manager_surname as "{}" FROM manager order by manager_id ASC LIMIT {};""".format(
    "Індекс менеджера","Ім'я менеджера","Прізвище менеджера",limit)

query_clients_desc = query_clients.replace("ASC","DESC")
query_managers_desc = query_managers.replace("ASC","DESC")
query_pricelist_desc = query_pricelist.replace("ASC","DESC")
query_proposals_desc = query_proposals.replace("ASC","DESC")
query_performers_desc = query_performers.replace("ASC","DESC")