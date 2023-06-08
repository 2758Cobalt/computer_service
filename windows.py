from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=[]) # default | test

connect_config = ("Cobalt","localhost:2525","Umsf_sqltutor","computer_service") # Default variable

tables_text = ["clients","managers","pricelist","proposals","performers"]

# =============================================================
def window_connection(root_window): # window
    # Скрываем корневое окно
    root_window.withdraw()

    # Создаем новое окно
    new_window = Tk("database_connection")
    new_window.resizable(0, 0)
    new_window.geometry("300x300+256+256")
    new_window.title("Підключення")
    new_window.configure(background="#1f1f1f")

    # Метки для полей ввода
    labels = ["Користувач", "Хост", "Пароль", "База даних"]
    for idx, label_text in enumerate(labels):
        label = Label(new_window, text=label_text, background="#2f2f2f", foreground="white", width=16, anchor="s")
        label.grid(row=idx, column=0, pady=5)

    # Поля ввода
    user = Entry(new_window)
    host = Entry(new_window)
    password = Entry(new_window, show="*")
    database = Entry(new_window)

    # Заполняем поля ввода значениями по умолчанию
    for idx, entry in enumerate([user, host, password,database] ):
        entry.insert(0, connect_config[idx])
        entry.grid(row=idx, column=1, pady=5)

    # Кнопка для подключения к базе данных
    connect_button = Button(new_window, text="Підключитися до бази даних", width=32, command=lambda: (
        root_connection.change_data(user=user.get(), host=host.get(), password=password.get(), database=database.get()),
        root_connection.connect(),
        new_window.destroy(),
        root_window.deiconify()
    ))
    Label(new_window,text="Хост треба вводити разом з портом!\nПриклад запису: 127.0.0.1:3306,\nде 127.0.0.1 - хост\n3306 - порт", background="#2f2f2f", foreground="white").place(anchor=S, relx=0.5, rely=0.8)
    connect_button.place(anchor=S, relx=0.5, rely=0.95)

    # Обработчик закрытия окна
    new_window.protocol("WM_DELETE_WINDOW", lambda: root_window.quit())


# =============================================================

def rewriting_arrays(rows, columns, connection):
    """Перезапись массивов"""
    try:
        rows[:] = connection[0]  # Используем срез для перезаписи значений в rows
        columns[:] = [x[0] for x in connection[1]]  # Используем генератор списка для перезаписи значений в columns
        return rows, columns
    
    except Exception as e:
        l.warning(f"Error overwriting data")
# =============================================================

def add_item(table_name):
    # Создаем новое окно
    window = Tk("Додавання елементу")
    window.resizable(0, 0)
    window.title(f"Таблиця: {table_name}")
    window.geometry("512x256+256+256")
    window.configure(background="#2f2f2f")
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    
    add_button = Button(window, text="Додати запис до таблиці", width=24) 
    
    if table_name == tables_text[0]: # Clients
        
        client_labels = ["Ім'я та прізвище клієнту", "Дата реєстрації", "Адреса клієнта","Номер телефону", "Індекс обслуговуючого мереджера"]
        
        for idx, label_text in enumerate(client_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        if table_name == "clients":
            # Client name/surname entry
            client_name_entry = Entry(window, width=32)
            client_reg_date_entry = Entry(window, width=18, justify='center')
            client_address_entry = Entry(window, width=18, justify='center')
            client_number_phone = Entry(window, width=18)
            client_manager_id_entry = Entry(window, justify='center')
            
            for idx, entry in enumerate([client_name_entry, client_reg_date_entry, client_address_entry, client_number_phone, client_manager_id_entry]):
                entry.grid(row=idx, column=1, pady=5)  # client name and surname

            # Add button command
            add_button.configure(command=lambda: (
                root_connection.query(f"""insert into clients_data (client_name, client_surname, client_register_date, client_address, client_number_phone, manager_manager_id)
                    values
                    (\"{client_name_entry.get().split()[0]}\", \"{client_name_entry.get().split()[1]}\",
                    \"{client_reg_date_entry.get()}\", 
                    \"{client_address_entry.get()}\", \"{client_number_phone.get()}\", {int(client_manager_id_entry.get())})"""), # Получение данных из полей _entry методом get()
            ))
    
    elif table_name == tables_text[1]: # Manager
        # Manager name/surname entry
        Label(window, text="Ім'я та прізвище менеджера", background="#4f4f4f",foreground="white").grid(row=0, column=0, padx=10, pady=5)
        
        manager_name_entry = Entry(window, width=32) # manager name and surname
        
        manager_name_entry.grid(row=0, column=1, padx=10, pady=5)  

        # Add button command
        add_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""insert into `manager` (manager_name,manager_surname) 
                values
                (\"{manager_name_entry.get().split()[0]}\",
                \"{manager_name_entry.get().split()[1]}\")"""),
            window.destroy()
        ))

    elif table_name == tables_text[2]: # Price-list
        
        pricelist_labels = ["Ціна за доставку обладнання", "Ціна за ремонт", "Ціна за налаштування ПЗ", "Ціна за новий пк", "Індекс виконавця","Індекс менеджеру"]
    
        for idx, label_text in enumerate(pricelist_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)
        
        pricelist_service_entry = Entry(window, width=10, justify='center')
        pricelist_repair_entry = Entry(window, width=10, justify='center')
        pricelist_setup_soft_entry = Entry(window, width=18, justify='center')
        pricelist_new_pc = Entry(window, width=18, justify='center')
        pricelist_performer_id = Entry(window, width=18, justify='center')
        pricelist_manager_id = Entry(window, width=18, justify='center')
        
        for idx, entry_p in enumerate([pricelist_service_entry, pricelist_repair_entry, pricelist_setup_soft_entry, pricelist_new_pc, pricelist_performer_id, pricelist_manager_id]):
            entry_p.grid(row=idx, column=1, padx=10, pady=5)
        
        # Add button command
        add_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""INSERT INTO `price-list` 
            (`service_price`, `repair_price`, `setup_software_price`, `new_pc_price`, `performers_performers_id`, `manager_manager_id`) 
            VALUES 
            ({pricelist_service_entry.get()}, {pricelist_repair_entry.get()}, {pricelist_setup_soft_entry.get()}, {pricelist_new_pc.get()},{pricelist_performer_id.get()}, {pricelist_manager_id.get()});
            """),
            window.destroy()
        ))

    elif table_name == tables_text[3]: # Proposals

        proposals_labels = ["Замовлення","Дата реєстрації замовлення","Індекс виконавця","Індекс клієнту"]

        for idx, label_text in enumerate(proposals_labels):
            label = Label(window, text=label_text, background="#4f4f4f",foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)

        proposals_type_entry = Entry(window, width=24)
        proposals_reg_date_entry = Entry(window, width=18, justify='center')
        proposals_id_entry = Entry(window, width=16)
        proposals_client_id_entry = Entry(window, width=16)

        for idx, entry in enumerate([proposals_type_entry,proposals_reg_date_entry,proposals_id_entry,proposals_client_id_entry]):
            entry.grid(row=idx, column=1, padx=10, pady=5)

        # Add button command
        add_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""INSERT INTO `proposals` 
            (`proposals_type`, `proposals_register_data`, `performers_performers_id`, `clients_data_client_id`) 
            VALUES 
            (\"{proposals_type_entry.get()}\", \"{proposals_reg_date_entry.get()}\", {proposals_id_entry.get()}, {proposals_client_id_entry.get()});
            """),
            window.destroy()
        ))

    elif table_name == tables_text[4]: # Perfomers
        performers_labels = ["Код замовлення","Початок виконання замовлення"]
        
        performers_num_to_code_entry = Entry(window, width=12) # Performer num to code entry
        performers_startwork_date_entry = Entry(window, width=18) # Performer startwork date entry
        
        for idx, label_text in enumerate(performers_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)
        
        for idx, entry in enumerate([performers_num_to_code_entry,performers_startwork_date_entry]):
            entry.grid(row=idx, column=1, padx=10, pady=5)

        # Add button command
        add_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""INSERT INTO `performers` 
            (`performers_num_to_clientcode`, `performers_startwork_date`) 
            VALUES 
            ({performers_num_to_code_entry.get()}, {performers_startwork_date_entry.get()});
            """),
            window.destroy()
        ))
    

    add_button.place(anchor=S, relx=0.5, rely=0.95)

# =============================================================

def delete_item(table_name):
    # Создаем новое окно
    window = Tk("Видалення елементу")
    window.resizable(0, 0)
    window.title(f"Таблиця: {table_name}")
    window.geometry("512x256+256+256")
    window.configure(background="#2f2f2f")
    
    delete_button = Button(window, text="Видалити запис з таблиці") # delete button
    
    if table_name == tables_text[0]: # Clients

        Label(window, text="Введіть індекс(id) клієнту", background="#4f4f4f", foreground="white").grid(row=0, padx=10, pady=5)
        
        client_id_entry = Entry(window)
        client_id_entry.grid(row=0, column=1, padx=10, pady=5)  # client name and surname
        
        # Delete button
        delete_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""delete from `clients_data` 
                where client_id = {client_id_entry.get()}"""),
            window.destroy()
        ))

    elif table_name == tables_text[1]: # Manager

        Label(window, text="Введіть індекс(id) менеджера", background="#4f4f4f", foreground="white").grid(row=0, padx=10, pady=5)
        
        manager_id_entry = Entry(window)
        manager_id_entry.grid(row=0, column=1, padx=10, pady=5)  # client name and surname
        
        delete_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""delete from `manager` 
                where manager_id = {manager_id_entry.get()}"""),
            window.destroy()
        ))

    elif table_name == tables_text[2]: # Price-list
    
        label = Label(window, text="Індекс листу", background="#4f4f4f", foreground="white")
        label.grid(row=0, column=0, padx=10, pady=5)
        
        pricelist_listid = Entry(window, width=10, justify='center')
        pricelist_listid.grid(row=0, column=1, padx=10, pady=5)
        
        # Delete button
        delete_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""delete from `price-list` 
                where list_id = {pricelist_listid.get()}
            """),
            window.destroy()
        ))

    elif table_name == tables_text[3]: # Proposals
        
        label = Label(window, text="Індекс замовлення", background="#4f4f4f", foreground="white")
        label.grid(row=0, column=0, padx=10, pady=5)
        
        proposals_id = Entry(window, width=10, justify='center')
        proposals_id.grid(row=0, column=1, padx=10, pady=5)
        
        # Delete button
        delete_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""delete from `proposals` 
                where proposals_id = {proposals_id.get()}
            """),
            window.destroy()
        ))

    elif table_name == tables_text[4]: # Performers
        label = Label(window, text="Індекс виконавця", background="#4f4f4f", foreground="white")
        label.grid(row=0, column=0, padx=10, pady=5)
        
        performers_id = Entry(window, width=10, justify='center')
        performers_id.grid(row=0, column=1, padx=10, pady=5)
        
        # Delete button
        delete_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""delete from `performers` 
                where performers_id = {performers_id.get()}
            """),
            window.destroy()
        ))

    delete_button.place(anchor=S, relx=0.5, rely=0.95)

# =============================================================

def edit_item(table_name):
    # Создаем новое окно
    window = Tk("Зміна елементу")
    window.resizable(0, 0)
    window.title(f"Таблиця: {table_name}")
    window.geometry("512x256+256+256")
    window.configure(background="#2f2f2f")
    
    edit_button = Button(window, text="Змінити запис у таблиці") # edit button
    
    if table_name == tables_text[0]: # Clients
        client_labels = ["Індекс клієнта", "Им'я та прізвище клієнта", "Код клієнта", "Дата реєстрації", "Номер телефону", "Індекс мереджера"]
        
        for idx, label_text in enumerate(client_labels):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        # Client name/surname entry
        client_id_entry = Entry(window, width=16,justify='center')
        client_name_entry = Entry(window, width=32)
        client_code_entry = Entry(window, width=10, justify='center')
        client_reg_date_entry = Entry(window, width=18, justify='center')
        client_number_phone = Entry(window, width=18)
        client_manager_id_entry = Entry(window, justify='center')
        
        for idx, entry in enumerate([client_id_entry,client_name_entry, client_code_entry, client_reg_date_entry, client_number_phone, client_manager_id_entry]):
            entry.grid(row=idx, column=1, pady=5)  # client name and surname

        edit_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""UPDATE `clients_data` SET `client_name` = '{client_name_entry.get().split()[0]}',
                                `client_surname` = '{client_name_entry.get().split()[1]}', `client_code`={client_code_entry.get()},
                                `client_register_date` = '{client_reg_date_entry.get()}', `client_number_phone` = '{client_number_phone.get()}',
                                `manager_manager_id` = '{client_manager_id_entry.get()}' WHERE (`client_id` = '{client_id_entry.get()}');"""), # Получение данных из полей _entry методом get()
            window.destroy() 
        ))

    elif table_name == tables_text[1]: # Manager
        
        for idx, label_text in enumerate(["Введіть індекс(id) менеджера","Им'я та прізвище менеджера"]):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)

        manager_id_entry = Entry(window)
        manager_name_entry = Entry(window, width=32) # manager name and surname
        
        for idx, entry in enumerate([manager_id_entry,manager_name_entry]):
            entry.grid(row=idx, column=1, padx=10, pady=5)  
        
        edit_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""UPDATE `manager` SET `manager_name` = '{manager_name_entry.get().split()[0]}',
                                `manager_surname` = '{manager_name_entry.get().split()[1]}' WHERE (`manager_id` = '{manager_id_entry.get()}');"""),
            window.destroy() 
        ))
    
    elif table_name == tables_text[2]: # Price-list
        pricelist_labels = ["Індекс листа","Ціна за доставку обладнання", "Ціна за ремонт", "Ціна за налаштування ПЗ", "Ціна за новий пк", "Індекс виконавця","Індекс менеджеру"]
    
        for idx, label_text in enumerate(pricelist_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)

        pricelist_id_entry = Entry(window, width=10, justify='center')
        pricelist_service_entry = Entry(window, width=10, justify='center')
        pricelist_repair_entry = Entry(window, width=10, justify='center')
        pricelist_setup_soft_entry = Entry(window, width=18, justify='center')
        pricelist_new_pc = Entry(window, width=18, justify='center')
        pricelist_performer_id = Entry(window, width=18, justify='center')
        pricelist_manager_id = Entry(window, width=18, justify='center')
        
        for idx, entry in enumerate([pricelist_id_entry,pricelist_service_entry, pricelist_repair_entry, pricelist_setup_soft_entry, pricelist_new_pc, pricelist_performer_id, pricelist_manager_id]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
        
        # Add button command
        edit_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""UPDATE `price-list` SET `service_price` = '{pricelist_service_entry.get()}',
                                `repair_price` = '{pricelist_repair_entry.get()}', `setup_software_price` = '{pricelist_setup_soft_entry.get()}',
                                `new_pc_price` = '{pricelist_new_pc.get()}', `performers_performers_id` = '{pricelist_performer_id.get()}',
                                `manager_manager_id` = '{pricelist_manager_id.get()}' 
                                WHERE (`list_id` = '{pricelist_id_entry.get()}');"""),
            window.destroy()
        ))
    
    elif table_name == tables_text[3]: # Proposals
        for idx, label_text in enumerate(["Індекс замовлення","Тип замовлення","Дата реєстрації замовлення","Індекс виконавця","Індекс замовника"]):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        proposals_id = Entry(window, width=10, justify='center')
        proposals_type = Entry(window, width=20)
        proposals_date = Entry(window, width=18, justify='center')
        proposals_performers_id = Entry(window, width=10, justify='center')
        proposals_client_id = Entry(window, width=10, justify='center')

        for idx, entry in enumerate([proposals_id,proposals_type,proposals_date,proposals_performers_id,proposals_client_id]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
        
        # Edit button
        edit_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""UPDATE `proposals` SET `proposals_type` = '{proposals_type.get()}', `proposals_register_data` = '{proposals_date.get()}',
                `performers_performers_id` = '{proposals_performers_id.get()}', `clients_data_client_id` = '{proposals_client_id}'
                WHERE (`proposals_id` = '{proposals_id}');"""),
            window.destroy()
        ))
    
    elif table_name == tables_text[4]: # Performers
        for idx, label_text in enumerate(["Індекс виконавця","Код замовника","Дата початку виконання"]):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        performers_id = Entry(window, width=10, justify='center')
        performers_clientcode = Entry(window, width=10, justify='center')
        performers_startwork = Entry(window, width=18, justify='center')
        
        for idx, entry in enumerate([performers_id,performers_clientcode,performers_startwork]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
    
        # Edit button
        edit_button.configure(command=lambda: (
            root_connection.connect(),
            root_connection.query(f"""UPDATE `performers` SET `performers_num_to_clientcode` = '{performers_clientcode.get()}',
                                `performers_startwork_date` = '{performers_startwork.get()}' 
                                WHERE (`performers_id` = '{performers_id.get()}');"""),
            window.destroy()
        ))
    
    edit_button.place(anchor=S, relx=0.5, rely=0.95)