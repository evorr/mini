from winsys import fs #through pip
import os
import easygui #pip install easygui
import sqlite3


base_dir = easygui.diropenbox(title='Какую папку выбрать')


connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Users ('
               'id INTEGER PRIMARY KEY, '
               'name TEXT NOT NULL)')
connection.commit()
cursor.execute('CREATE TABLE IF NOT EXISTS Folders ('
               'id INTEGER PRIMARY KEY,'
               'name TEXT NOT NULL, '
               'user_id INTEGER, '
               'FOREIGN KEY (user_id)  REFERENCES users (id))')
connection.commit()


result_tuple = os.walk(base_dir)
for i in result_tuple:
    for part in fs.dir(i[0]).security().dacl:
        cursor.execute(f'SELECT id FROM Users WHERE name="{part.trustee}"')
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.execute('INSERT INTO Users (name) VALUES (?);', (f'{part.trustee}', ))
            cursor.execute(f'SELECT id FROM Users WHERE name="{part.trustee}"')
            results = cursor.fetchone()

        cursor.execute('INSERT INTO Folders (name, user_id) VALUES (?, ?);', (f'{i[0]}', results[0][0], ))
        connection.commit()

connection.close()

easygui.msgbox('Ready')
