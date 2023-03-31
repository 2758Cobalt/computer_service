from init import *
import mysql_client as m

def gettext():
    sys('cls')
    print("Команда:\n" + output.get("1.0",END) + "\n\n-=-=-=-=-=-=-\n")
    m.connection_init(output.get("1.0",END))

root = Tk()
root.title(app_title)
root.geometry(app_resolution)
root.configure(background="#1f1f1f")

label = ttk.Label(text="Test_mode").pack(side=TOP,anchor=NW)

btn = ttk.Button(text="Execute",command=lambda: gettext()).pack(side=TOP,anchor=NE)

btn = ttk.Button(text="clear",command=lambda: sys('cls')).pack(side=TOP,anchor=NE)

output = Text()
output.pack(fill=BOTH,expand=1)



root.mainloop()