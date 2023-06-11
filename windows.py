from init import *
from mysql_client import *

root_connection = MySql_connection(connection_data=[]) # default | test

connect_config = ("user","localhost:3306","","") # Default variable

tables_text = ["clients","managers","pricelist","proposals","performers","view_1","view_2"]
    
def entry_check(entries):
    try:
        for element in entries:
            if element == "": raise Exception("Entry is empty")
    except Exception as e:
        l.error(e)
        messagebox.showwarning("Помилка","Всі або декілька полів порожні!")

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
    try:
        connect_button = Button(new_window, text="Підключитися до бази даних", width=32, command=lambda: (
            root_connection.change_data(user=user.get(), host=host.get(), password=password.get(), database=database.get()),
            root_connection.connect(),
            new_window.destroy(),
            root_window.deiconify()
        ))
        Label(new_window,text="Хост треба вводити разом з портом!\nПриклад запису: 127.0.0.1:3306,\nде 127.0.0.1 - хост\n3306 - порт", background="#2f2f2f", foreground="white").place(anchor=S, relx=0.5, rely=0.8)
        connect_button.place(anchor=S, relx=0.5, rely=0.95)
    except Exception as e:
        print(e.errno)
        messagebox.showerror("test","desc")
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
        l.error(f"Error overwriting data")
# =============================================================

def add_item(table_name):
    try: 
        # Создаем новое окно
        window = Tk("Додавання елементу")
        window.resizable(0, 0)
        window.title(f"Таблиця: {table_name}")
        window.geometry("512x256+256+256")
        window.configure(background="#2f2f2f")
        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
        
        add_button = Button(window, text="Додати запис до таблиці", width=24) 

        if table_name == tables_text[0]: # Clients
            
            client_columns = ["Ім'я та прізвище клієнту", "Дата реєстрації", "Адреса клієнта", "Номер телефону"]
            
            for idx, label_text in enumerate(client_columns):
                label = Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
                
                client_name_entry = Entry(window, width=32) # Client name/surname entry
                client_reg_date_entry = Entry(window, width=18, justify='center')
                client_address_entry = Entry(window, width=18, justify='center')
                client_number_phone = Entry(window, width=18)
                
                for idx, entry in enumerate([client_name_entry, client_reg_date_entry, client_address_entry, client_number_phone]):
                    entry.grid(row=idx, column=1, pady=5)  # client name and surname

                # Add button command
                add_button.configure(command=lambda: (
                    entry_check([client_name_entry.get(), client_reg_date_entry.get(), client_address_entry.get(), client_number_phone.get()]),
                    root_connection.query(f"""INSERT INTO `clients` (client_name, client_surname, client_register_date, client_address, client_number_phone)
                        VALUES
                        ('{client_name_entry.get().split()[0]}', '{client_name_entry.get().split()[1]}',
                        '{client_reg_date_entry.get()}', 
                        '{client_address_entry.get()}', '{client_number_phone.get()}')""",True),
                    window.destroy()
                ))

        elif table_name == tables_text[1]: # Manager
            # Manager name/surname entry
            Label(window, text="Ім'я та прізвище менеджера", background="#4f4f4f",foreground="white").grid(row=0, column=0, padx=10, pady=5)
            Label(window, text="Індекс клієнта", background="#4f4f4f",foreground="white").grid(row=1, column=0, padx=10, pady=5)
            
            m_name_entry = Entry(window, width=32) # manager name and surname
            m_client_id_entry = Entry(window, width=32) # manager name and surname
            
            m_name_entry.grid(row=0, column=1, padx=10, pady=5)
            m_client_id_entry.grid(row=1, column=1, padx=10, pady=5)

            # Add button command
            add_button.configure(command=lambda: (
                entry_check([m_name_entry.get(),m_client_id_entry.get()]),
                root_connection.connect(),

                root_connection.query(f"""INSERT INTO `manager` (manager_name, manager_surname, `clients_client_id`) 
                    VALUES ('{m_name_entry.get().split()[0]}','{m_name_entry.get().split()[1]}', {m_client_id_entry.get()})""",True),
                window.destroy()
            ))

        elif table_name == tables_text[2]: # Pricelist
            
            pricelist_labels = ["Індекс листа","Ціна за доставку обладнання", "Ціна за ремонт", "Ціна за налаштування ПЗ", "Ціна за новий пк", "Індекс виконавця","Код замовлення"]
        
            for idx, label_text in enumerate(pricelist_labels):
                Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
            
            pl_id_entry = Entry(window, width=8, justify='center')
            pl_shipping_entry = Entry(window, width=8, justify='center')
            pl_repair_entry = Entry(window, width=8, justify='center')
            pl_setup_soft_entry = Entry(window, width=8, justify='center')
            pl_new_pc = Entry(window, width=8, justify='center')
            pl_performer_id = Entry(window, width=8, justify='center')
            pl_proposal_id = Entry(window, width=8, justify='center')
            
            for idx, entry_p in enumerate([pl_id_entry,pl_shipping_entry, pl_repair_entry, pl_setup_soft_entry, pl_new_pc, pl_performer_id, pl_proposal_id]):
                entry_p.grid(row=idx, column=1, padx=10, pady=5)
            
            # Add button command
            add_button.configure(command=lambda: (
                entry_check([pl_shipping_entry.get(),pl_repair_entry.get(),pl_setup_soft_entry.get(),pl_new_pc.get(),
                            pl_performer_id.get(),pl_proposal_id.get()]),
                root_connection.connect(),
                root_connection.query(f"""INSERT INTO `pricelist` 
                (`list_id`,`shipping_price`, `repair_price`, `setup_software_price`, `new_pc_price`, `performers_performer_id`, `proposals_proposal_id`) 
                VALUES 
                ({pl_id_entry.get()}, {pl_shipping_entry.get()}, {pl_repair_entry.get()}, {pl_setup_soft_entry.get()}, {pl_new_pc.get()},{pl_performer_id.get()}, {pl_proposal_id.get()});
                """,True),
                window.destroy()
            ))

        elif table_name == tables_text[3]: # Proposals

            proposals_labels = ["Індекс замовлення","Послуга","Дата реєстрації замовлення","Індекс менеджера"]
            pr_types = ["Ремонт","Встановлення ПЗ","Новий PC","Достака обладнання"]
            for idx, label_text in enumerate(proposals_labels):
                Label(window, text=label_text, background="#4f4f4f",foreground="white").grid(row=idx, column=0, padx=10, pady=5)

            pr_id_entry = Entry(window, width=10, justify='center')
            pr_type_combo = Combobox(window, textvariable="Ремонт", values=pr_types, state="readonly")
            pr_type_combo.current(0)
            pr_reg_date_entry = Entry(window, width=24, justify='center')
            pr_manager_id_entry = Entry(window, width=8, justify='center')

            for idx, entry in enumerate([pr_id_entry,pr_type_combo,pr_reg_date_entry,pr_manager_id_entry]):
                entry.grid(row=idx, column=1, padx=10, pady=5)

            # Add button command
            add_button.configure(command=lambda: (
                entry_check([pr_id_entry,pr_type_combo.get(),pr_reg_date_entry.get(),pr_manager_id_entry.get()]),
                root_connection.connect(),
                root_connection.query(f"""INSERT INTO `proposals` 
                (`proposal_id`,`proposal_type`, `proposal_register_date`, `manager_manager_id`) 
                VALUES 
                ('{pr_id_entry.get()}','{pr_type_combo.get()}', '{pr_reg_date_entry.get()}', '{pr_manager_id_entry.get()}');""",True),
                window.destroy()
            ))

        elif table_name == tables_text[4]: # Perfomers
            performers_columns = ["Індекс виконавця","Ім'я та прізвище виконавця","Код замовлення","Початок виконання замовлення"]
            
            per_id_entry = Entry(window, width=12) # Performer id
            per_name_entry = Entry(window, width=12) # Performer name and surname
            per_number_proposal_entry = Entry(window, width=12) # Performer num to code entry
            per_startwork_date_entry = Entry(window, width=18) # Performer startwork date entry
            
            for idx, label_text in enumerate(performers_columns):
                Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
            
            for idx, entry in enumerate([per_id_entry,per_name_entry,per_number_proposal_entry,per_startwork_date_entry]):
                entry.grid(row=idx, column=1, padx=10, pady=5)

            # Add button command
            add_button.configure(command=lambda: (
                entry_check([per_name_entry.get(),per_number_proposal_entry.get(),per_startwork_date_entry.get()]), # EntryField Check
                root_connection.connect(),
                root_connection.query(f"""INSERT INTO `performers` 
                (`performer_id`,`performer_name`,`performer_surname`,`performer_number_proposal`, `performer_startwork_date`) 
                VALUES 
                ('{per_id_entry.get()}','{per_name_entry.get().split()[0]}', '{per_name_entry.get().split()[1]}',
                {per_number_proposal_entry.get()}, '{per_startwork_date_entry.get()}');""",True),
                window.destroy() # Window Destroy
            ))
        
        add_button.place(anchor=S, relx=0.5, rely=0.95)

    except Exception as e: 
        l.warning("Entry is empty")
        print(e)

# =============================================================

def delete_item(table_name):
    try:
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
                entry_check([client_id_entry.get()]),
                root_connection.connect(),
                root_connection.query(f"""delete from `clients` 
                    where client_id = {client_id_entry.get()}""",True),
                window.destroy()
            ))

        elif table_name == tables_text[1]: # Manager

            Label(window, text="Введіть індекс(id) менеджера", background="#4f4f4f", foreground="white").grid(row=0, padx=10, pady=5)
            
            manager_id_entry = Entry(window)
            manager_id_entry.grid(row=0, column=1, padx=10, pady=5)  # client name and surname
            
            delete_button.configure(command=lambda: (
                entry_check([manager_id_entry.get()]),
                root_connection.connect(),
                root_connection.query(f"""delete from `manager` 
                    where manager_id = {manager_id_entry.get()}""",True),
                window.destroy()
            ))

        elif table_name == tables_text[2]: # Pricelist
        
            label = Label(window, text="Індекс листу", background="#4f4f4f", foreground="white")
            label.grid(row=0, column=0, padx=10, pady=5)
            
            pricelist_listid = Entry(window, width=10, justify='center')
            pricelist_listid.grid(row=0, column=1, padx=10, pady=5)
            
            # Delete button
            delete_button.configure(command=lambda: (
                entry_check([[pricelist_listid.get()]]),
                root_connection.connect(),
                root_connection.query(f"""delete from `pricelist` 
                    where list_id = {pricelist_listid.get()}
                """,True),
                window.destroy()
            ))

        elif table_name == tables_text[3]: # Proposals
            
            label = Label(window, text="Індекс замовлення", background="#4f4f4f", foreground="white")
            label.grid(row=0, column=0, padx=10, pady=5)
            
            proposals_id = Entry(window, width=10, justify='center')
            proposals_id.grid(row=0, column=1, padx=10, pady=5)
            
            # Delete button
            delete_button.configure(command=lambda: (
                entry_check([proposals_id.get()]),
                root_connection.connect(),
                root_connection.query(f"""delete from `proposals` 
                    where proposal_id = {proposals_id.get()}
                """,True),
                window.destroy()
            ))

        elif table_name == tables_text[4]: # Performers
            label = Label(window, text="Індекс виконавця", background="#4f4f4f", foreground="white")
            label.grid(row=0, column=0, padx=10, pady=5)
            
            performers_id = Entry(window, width=10, justify='center')
            performers_id.grid(row=0, column=1, padx=10, pady=5)
            
            # Delete button
            delete_button.configure(command=lambda: (
                entry_check([performers_id.get()]),
                root_connection.connect(),
                root_connection.query(f"""delete from `performers` 
                    where performer_id = {performers_id.get()}
                """,True),
                window.destroy()
            ))

        delete_button.place(anchor=S, relx=0.5, rely=0.95)
    except Exception: l.warning("Entry is empty")
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
        client_columns = ["Індекс клієнта","Ім'я та прізвище клієнту", "Дата реєстрації", "Адреса клієнта", "Номер телефону"]
    
        for idx, label_text in enumerate(client_columns):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        client_id_entry = Entry(window, width=32) # Client name/surname entry
        client_name_entry = Entry(window, width=32) # Client name/surname entry
        client_reg_date_entry = Entry(window, width=18, justify='center')
        client_address_entry = Entry(window, width=18, justify='center')
        client_number_phone = Entry(window, width=18)
        
        for idx, entry in enumerate([client_id_entry,client_name_entry, client_reg_date_entry, client_address_entry, client_number_phone]):
            entry.grid(row=idx, column=1, pady=5)  # client name and surname

        edit_button.configure(command=lambda: (
            entry_check([client_id_entry.get(),client_name_entry.get(),client_reg_date_entry.get(),client_address_entry.get(),client_number_phone.get()]),
            root_connection.connect(),
            root_connection.query(f"""UPDATE `clients` SET `client_name` = '{client_name_entry.get().split()[0]}',
                                `client_surname` = '{client_name_entry.get().split()[1]}',
                                `client_register_date` = '{client_reg_date_entry.get()}',
                                `client_address` = '{client_address_entry.get()}',
                                `client_number_phone` = '{client_number_phone.get()}' WHERE `client_id` = {client_id_entry.get()};""",True),
            window.destroy() 
        ))

    elif table_name == tables_text[1]: # Manager
        
        for idx, label_text in enumerate(["Введіть індекс(id) менеджера","Им'я та прізвище менеджера","Індекс клієнта"]):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)

        manager_id_entry = Entry(window)
        manager_name_entry = Entry(window, width=32) # manager name and surname
        manager_client_id_entry = Entry(window, width=32) # client_id
        
        for idx, entry in enumerate([manager_id_entry,manager_name_entry,manager_client_id_entry]):
            entry.grid(row=idx, column=1, padx=10, pady=5)  
        
        edit_button.configure(command=lambda: (
            entry_check([manager_id_entry.get(),manager_name_entry.get()]),
            root_connection.connect(),
            root_connection.query(f"""UPDATE `manager` SET `manager_name` = '{manager_name_entry.get().split()[0]}',
                                `manager_surname` = '{manager_name_entry.get().split()[1]}',
                                `clients_client_id` = '{manager_client_id_entry.get()}' WHERE (`manager_id` = '{manager_id_entry.get()}');""",True),
            window.destroy() 
        ))
    
    elif table_name == tables_text[2]: # Pricelist
        pricelist_labels = ["Індекс листа","Ціна за доставку обладнання", "Ціна за ремонт", "Ціна за налаштування ПЗ", "Ціна за новий пк", "Індекс виконавця","Індекс менеджеру"]
    
        for idx, label_text in enumerate(pricelist_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)

        pricelist_id_entry = Entry(window, width=10, justify='center')
        pl_shipping_entry = Entry(window, width=10, justify='center')
        pricelist_repair_entry = Entry(window, width=10, justify='center')
        pricelist_setup_soft_entry = Entry(window, width=18, justify='center')
        pricelist_new_pc = Entry(window, width=18, justify='center')
        pricelist_performer_id = Entry(window, width=18, justify='center')
        pl_proposals_id = Entry(window, width=18, justify='center')
        
        for idx, entry in enumerate([pricelist_id_entry,pl_shipping_entry, pricelist_repair_entry, pricelist_setup_soft_entry, pricelist_new_pc, pricelist_performer_id, pl_proposals_id]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
        
        # Add button command
        edit_button.configure(command=lambda: (
            entry_check([pricelist_id_entry.get(),pl_shipping_entry.get(),pricelist_repair_entry.get(),pricelist_setup_soft_entry.get(),pricelist_new_pc.get(),pricelist_performer_id.get(),pl_proposals_id.get()]),
            root_connection.connect(),
            root_connection.query(f"""UPDATE `pricelist` SET `shipping_price` = '{pl_shipping_entry.get()}',
                                `repair_price` = '{pricelist_repair_entry.get()}', `setup_software_price` = '{pricelist_setup_soft_entry.get()}',
                                `new_pc_price` = '{pricelist_new_pc.get()}', `performers_performer_id` = '{pricelist_performer_id.get()}',
                                `proposals_proposal_id` = '{pl_proposals_id.get()}' 
                                WHERE (`list_id` = '{pricelist_id_entry.get()}');""",True),
            window.destroy()
        ))
    
    elif table_name == tables_text[3]: # Proposals
        for idx, label_text in enumerate(["Індекс замовлення","Послуга","Дата реєстрації замовлення","Індекс менеджера"]):
            Label(window, text=label_text, background="#4f4f4f", foreground="white").grid(row=idx, column=0, padx=10, pady=5)
        
        proposals_id = Entry(window, width=10, justify='center')
        proposals_type = Entry(window, width=20)
        proposals_date = Entry(window, width=18, justify='center')
        proposals_manager_id = Entry(window, width=10, justify='center')

        for idx, entry in enumerate([proposals_id,proposals_type,proposals_date,proposals_manager_id]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
        
        # Edit button
        edit_button.configure(command=lambda: (
            entry_check([proposals_id.get(),proposals_type.get(),proposals_date.get(),proposals_manager_id.get()]),
            root_connection.connect(),
            root_connection.query(f"""UPDATE `proposals` SET 
                `proposal_type` = '{proposals_type.get()}',
                `proposal_register_date` = '{proposals_date.get()}',
                `manager_manager_id` = '{proposals_manager_id.get()}'
                WHERE (`proposal_id` = '{proposals_id.get()}');""",True),
            window.destroy()
        ))
    
    elif table_name == tables_text[4]: # Performers
        
        performers_labels = ["Індекс виконавця","Ім'я та прізвище виконавця","Код замовлення","Початок виконання замовлення"]
            
        per_id_entry = Entry(window, width=12) # Performer id
        per_name_entry = Entry(window, width=12) # Performer name and surname
        per_number_proposal_entry = Entry(window, width=12) # Performer num to code entry
        per_startwork_date_entry = Entry(window, width=18) # Performer startwork date entry
        
        for idx, label_text in enumerate(performers_labels):
            label = Label(window, text=label_text, background="#4f4f4f", foreground="white")
            label.grid(row=idx, column=0, padx=10, pady=5)
        
        for idx, entry in enumerate([per_id_entry,per_name_entry,per_number_proposal_entry,per_startwork_date_entry]):
            entry.grid(row=idx, column=1, padx=10, pady=5)
        # Add button command
        edit_button.configure(command=lambda: (
            entry_check([per_id_entry.get(),per_name_entry.get(),per_number_proposal_entry.get(),per_startwork_date_entry.get()]),
            root_connection.connect(),
            root_connection.query(f"""UPDATE `performers` SET 
                            `performer_name` = '{per_name_entry.get().split()[0]}',
                            `performer_surname` = '{per_name_entry.get().split()[1]}',
                            `performer_number_proposal` = {per_number_proposal_entry.get()},
                            `performer_startwork_date` = '{per_startwork_date_entry.get()}' 
                            WHERE (`performer_id` = '{per_id_entry.get()}');""",True),
            window.destroy()
        ))

    edit_button.place(anchor=S, relx=0.5, rely=0.95)
