from init import *

root = Tk()
root.title(app_title)
root.geometry(app_resolution)

def get_text():
    print(editor.get()) # test

def button(label="text",command=None,side=TOP,anchor=NW): # test
    return ttk.Button(text=label,command=command).pack(side=side,anchor=anchor)

def label(label="text",side=TOP,anchor=NW):# test
    return ttk.Label(text=label).pack(side=side,anchor=anchor)


editor = Entry()
editor.pack()

button("click",command=get_text,side=BOTTOM,anchor=CENTER)

root.mainloop()