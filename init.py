from tkinter import Tk, Frame, Button, Label, Scrollbar, Menu, StringVar
from tkinter.constants import *
import tkinter.messagebox as messagebox
from tkinter.ttk import Entry,Style,Treeview,Combobox
from mysql.connector import connect, Error
from subprocess import Popen
from loguru import logger as l


tables = ["managers","clients","pricelist","proposals","performers","view_1","view_2"]

# constains
app_title = "Комп'ютер-Сервіс"
app_resolution = [820,500]
app_screen = str(app_resolution[0]) + "x" + str(app_resolution[1]) # resolution
limit = 100 # limit

query_clients = """SELECT `client_id` AS "{}",`client_name` AS "{}", `client_surname` AS "{}",
`client_register_date` AS "{}",`client_address` AS "Адреса клієнта",`client_number_phone` AS "{}" from `clients` order by client_id ASC LIMIT {};""".format(
    "Номер клієнту","Им'я клієнта","Призвище клієнта","Дата реєстрації клієнта","Номер телефону",limit)

query_managers = """SELECT `manager_id` AS "{}", `manager_name` AS "{}", `manager_surname` AS "{}", `clients_client_id` AS "{}" FROM manager order by manager_id ASC LIMIT {};""".format(
    "Індекс менеджера","Ім'я менеджера","Прізвище менеджера","Індекс клієнта",limit)

query_pricelist = """SELECT `list_id` AS "{}",`shipping_price` AS "{}",
`repair_price` AS "{}",`setup_software_price` AS "{}", `new_pc_price` AS "{}",
`performers_performer_id` AS "{}", `proposals_proposal_id` AS "{}" from `pricelist` order by list_id ASC LIMIT {};""".format(
    "Номер послуги","Ціна доставки обладнання","Ціна ремонту","Ціна встановлення програмного забезпечення", "Ціна нового пк", "Код виконавця","Код замовлення",limit)

query_proposals = """SELECT `proposal_id` AS "{}", `proposal_type` AS "{}", `proposal_register_date` AS "{}", `manager_manager_id` AS "{}" from proposals order by proposal_id ASC LIMIT {};""".format(
    "Індекс послуги","Вид послуги","Дата замовлення послуги","Індекс обслуговуючого менеджера", limit)

query_performers = """SELECT `performer_id` AS "{}",`performer_name` AS "{}", `performer_surname` AS "{}",
`performer_number_proposal` AS "{}", `performer_startwork_date` AS "{}" from performers order by `performer_id` ASC LIMIT {};""".format(
    "Індекс виконавця","Ім'я виконавця","Прізвище виконавця","Номер виконуючого замовлення","Початок виконання замовлення",limit) # Наименнование колонок

query_view_workers = """SELECT * FROM workers ORDER BY `Ім'я менеджера` ASC;"""
query_view_summary = """SELECT * FROM price_summary ORDER BY `Номер оплачуваного замовлення` ASC;"""


query_clients_desc = query_clients.replace("ASC","DESC")
query_managers_desc = query_managers.replace("ASC","DESC")
query_pricelist_desc = query_pricelist.replace("ASC","DESC")
query_proposals_desc = query_proposals.replace("ASC","DESC")
query_performers_desc = query_performers.replace("ASC","DESC")
query_view_workers_desc = query_view_workers.replace("ASC","DESC")
query_view_summary_desc = query_view_summary.replace("ASC","DESC")