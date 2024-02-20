import sqlite3
from tkinter import *
from tkinter import ttk


connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()


root = Tk()
root.title("test_users")
root.geometry("500x200")


cursor.execute("SELECT name FROM Users")
users = cursor.fetchall()
list_users = []
for item in users:
    for word in item:
        list_users.append(word)

combobox = ttk.Combobox(values=list_users)
combobox.pack(anchor=NW, padx=6, pady=6)


def selected(event):
    selection = combobox.get()

    cursor.execute(f'SELECT Users.name, Folders.name FROM Users '
                   f'RIGHT JOIN U_F ON U_F.user_id=Users.id '
                   f'RIGHT JOIN Folders ON Folders.id=U_F.folder_id '
                   f'WHERE Users.name="{selection}"')
    by_user = cursor.fetchall()
    columns = ("Users.name", "Folders.name")
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)
    sb = Scrollbar(tree, orient=VERTICAL)
    sb.pack(side=RIGHT, fill=Y)

    tree.config(yscrollcommand=sb.set)
    sb.config(command=tree.yview)
    tree.heading("Users.name", text="user")
    tree.heading("Folders.name", text="folder")
    # добавляем данные
    for part in by_user:
       tree.insert("", END, values=part)

combobox.bind("<<ComboboxSelected>>", selected)

root.mainloop()
