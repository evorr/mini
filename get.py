from winsys import fs  # through pip
import os
import easygui  # pip install easygui
import sqlite3


def get_folder():
    folder = easygui.diropenbox(title='Какую папку выбрать')
    return folder


def get_id_from_db(cursor, table, value):
    cursor.execute(f'SELECT id FROM {table} WHERE name="{value}"')
    result_user = cursor.fetchone()
    if not result_user:
        cursor.execute(f'INSERT INTO {table} (name) VALUES (?);', (f'{value}',))
        cursor.execute(f'SELECT id FROM {table} WHERE name="{value}"')
        result_user = cursor.fetchone()
    id_by_value = result_user[0]
    return id_by_value


def start():
    base_dir = get_folder()

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Users ('
                   'id INTEGER PRIMARY KEY, '
                   'name TEXT NOT NULL)')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Folders ('
                   'id INTEGER PRIMARY KEY,'
                   'name TEXT NOT NULL) ')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS U_F ('
                   'id INTEGER PRIMARY KEY,'
                   'user_id INTEGER, '
                   'folder_id INTEGER, '
                   'FOREIGN KEY (user_id)  REFERENCES Users (id),'
                   'FOREIGN KEY (folder_id)  REFERENCES Folders (id))'
                   )
    connection.commit()

    result_tuple = os.walk(base_dir)
    for i in result_tuple:
        for part in fs.dir(i[0]).security().dacl:

            result_user = get_id_from_db(cursor, 'Users', part.trustee)
            result_folder = get_id_from_db(cursor, 'Folders', i[0])
            cursor.execute(f'SELECT id FROM U_F WHERE user_id="{result_user}" AND folder_id="{result_folder}"')
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO U_F (user_id, folder_id) VALUES (?, ?);', (result_user, result_folder,))
                connection.commit()

    connection.close()

    easygui.msgbox('Ready')


if __name__ == '__main__':
    start()
