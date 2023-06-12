from init import *
from mysql_client import *
from windows import *

l.add("log/debug-{time}.log", format="{file} {time:H:m:s} {message}", level="TRACE", rotation="50 KB") # Logger
l.info("<--------------Start logging--------------->") # Message for start log

class App:
    def __init__(self):
        self.root = Tk("main")
        self.root.title(app_title)
        self.root.geometry(app_screen)
        
        self.sys_rows = [] # Table rows
        self.sys_columns = [] # Table columns
        self.current_table = None # Current selected table
        
        # Menu
        self.file_menubar = Menu(self.root)
        
        # Cascade
        self.menu_tabs_labels = ["Менеджери","Клієнти","Прайслист","Замовлення","Виконавці","     ","Працівники сервісу","Сума до сплати"]
        self.menu_commands = [
            (self.menu_tabs_labels[0], query_managers, tables[0]),
            (self.menu_tabs_labels[1], query_clients, tables[1]),
            (self.menu_tabs_labels[2], query_pricelist, tables[2]),
            (self.menu_tabs_labels[3], query_proposals, tables[3]),
            (self.menu_tabs_labels[4], query_performers, tables[4]),
        ]
        
        for label, query, command in self.menu_commands:
            self.file_menubar.add_cascade(label=label, command=lambda q=query, c=command: self.menu_action(q, c))

        self.file_menubar.add_cascade(label="     ",state='disabled')
        
        self.file_menubar.add_cascade(label=self.menu_tabs_labels[6], command=lambda:self.menu_action(query_view_workers,tables[5]))
        self.file_menubar.add_cascade(label=self.menu_tabs_labels[7], command=lambda:self.menu_action(query_view_summary,tables[6]))

        # Frames
        self.main_frame = Frame(self.root, bg="#3f3f3f")
        self.upper_btn_frame = Frame(self.root, bg="#3f3f3f")
        self.buttons_frame = Frame(self.upper_btn_frame, bg="#ff6f4f")
        self.lower_buttons_frame = Frame(self.main_frame, bg="#4f4f4f")
        
        # Tables
        self.root_table = Table(self.main_frame, self.sys_columns, self.sys_rows)
        self.name_table = Label(self.main_frame, text="Таблиця не вибрана", background="#4f4f4f", foreground="white")
        
        # Sort buttons
        self.lower_text = ["Сортувати за зростанням", "Сортувати за спаданням", "limit"]
        self.sort_asc = Button(self.lower_buttons_frame, text=self.lower_text[0], width=len(self.lower_text[0]), command=lambda: self.sort("ASC")).grid(row=0, column=0, padx=5, pady=5)
        self.sort_desc = Button(self.lower_buttons_frame, text=self.lower_text[1], width=len(self.lower_text[1]), command=lambda: self.sort("DESC")).grid(row=0, column=1, padx=5, pady=5)

        # Pack
        Label(self.upper_btn_frame, text="Панель керування", background="#4f4f4f", foreground="white").pack(anchor=N)
        self.upper_btn_frame.pack(expand=1, anchor=N, fill=X, pady=10, padx=10)
        self.buttons_frame.pack(expand=1, anchor=N, fill=X, pady=10, padx=10)
        self.main_frame.pack(expand=1, anchor='center', fill=BOTH, pady=10, padx=20)
        self.name_table.pack(anchor=N, pady=5)
        self.root_table.pack(fill=X, padx=5, pady=5)
        self.lower_buttons_frame.pack(fill=BOTH, padx=5)
        
        # Buttons
        self.buttons_collection = ["Підключитися до бази даних", "Додати новий запис", "Видалити запис", "Змінити запис", "Довідка"]
        
        self.reconnect_btn = Button(self.buttons_frame, text=self.buttons_collection[0], width=len(self.buttons_collection[0]), command=lambda: window_connection(self.root))
        self.add_item_btn = Button(self.buttons_frame, state="disabled", text=self.buttons_collection[1], width=len(self.buttons_collection[1]), command=lambda: add_item(self.current_table))
        self.remove_item_btn = Button(self.buttons_frame, state="disabled", text=self.buttons_collection[2], width=len(self.buttons_collection[2]), command=lambda: delete_item(self.current_table))
        self.edit_item_btn = Button(self.buttons_frame, state="disabled", text=self.buttons_collection[3], width=len(self.buttons_collection[3]) + 2, command=lambda: edit_item(self.current_table))
        self.info = Button(self.buttons_frame, text=self.buttons_collection[4], width=len(self.buttons_collection[4]) + 2, command=lambda: Popen(['start','doc.pdf'],shell=True))
        
        for column, button in enumerate([self.reconnect_btn, self.add_item_btn, self.edit_item_btn, self.remove_item_btn, self.info]):
            
            button.grid(row=0, column=column, ipadx=10, padx=5, pady=5, sticky=EW)
        
        # Configure
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_session()) # Event for close window
        self.root.config(menu = self.file_menubar)
        self.root.configure(background="#2f2f2f")
        self.root.mainloop()
        
    def menu_action(self, q_query, cmd):
        """Взаємодія з меню"""
        for btn in [self.add_item_btn, self.remove_item_btn, self.edit_item_btn]:
            btn.configure(state="normal")
        
        rewriting_arrays(self.sys_rows, self.sys_columns, root_connection.query(q_query))
        
        for x in range(len(tables)):
            if cmd == tables[x]:
                self.current_table = tables[x]
        
        self.name_table.configure(text=f"Обрана таблиця: \"{self.current_table}\"")
        self.root_table.refresh_table()

        return self.current_table
    
    def sort(self, type_sort):
        """Сортування таблиць"""
        if self.current_table == None:
            messagebox.showwarning("Увага","Таблиця не вибрана")
        else:
            query_map = {
                "ASC": {
                    tables_text[0]: query_clients,
                    tables_text[1]: query_managers,
                    tables_text[2]: query_pricelist,
                    tables_text[3]: query_proposals,
                    tables_text[4]: query_performers,
                    tables_text[5]: query_view_workers,
                    tables_text[6]: query_view_summary
                },
                "DESC": {
                    tables_text[0]: query_clients_desc,
                    tables_text[1]: query_managers_desc,
                    tables_text[2]: query_pricelist_desc,
                    tables_text[3]: query_proposals_desc,
                    tables_text[4]: query_performers_desc,
                    tables_text[5]: query_view_workers_desc,
                    tables_text[6]: query_view_summary_desc
                }
            }
            
            if type_sort in query_map:
                if self.current_table in query_map[type_sort]:
                    query = query_map[type_sort][self.current_table]
                    rewriting_arrays(self.sys_rows, self.sys_columns, root_connection.query(query))
                else:
                    l.warning("Sort is invalid")
                    messagebox.showerror("Помилка", "Сортувати не можливо, таблиці не існує")
            else:
                l.warning("Table has't been selected")
                messagebox.showerror("Помилка", "Таблиця не вибрана")
        
        self.root_table.refresh_table()
    
    def close_session(self):
        try:
            
            l.info("Session is closed")
            self.root.quit()
        except Error as e:
            l.error(f"Error {e}")
            self.root.quit()
        

if __name__ == "__main__":
    App()