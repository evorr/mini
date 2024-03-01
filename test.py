import sqlite3

connection = sqlite3.connect('test_database.db')
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


def get_id_from_db(table, value):
    cursor.execute(f'SELECT id FROM {table} WHERE name="{value}"')
    result_user = cursor.fetchone()
    if not result_user:
        cursor.execute(f'INSERT INTO {table} (name) VALUES (?);', (f'{value}',))
        cursor.execute(f'SELECT id FROM {table} WHERE name="{value}"')
        result_user = cursor.fetchone()
    id_by_value = result_user[0]
    return id_by_value


list_users = ["Two", "Two", "Eleven", "Seven", "Three", "One", "One"]
list_folders = ["/desktop", "/desktop", "/desktop/project/ver_1", "/desktop/project", "/desktop/project", "/desktop/project",
                "/desktop/project"]


for i in range(0, len(list_users)):
    result_user = get_id_from_db('Users', list_users[i])
    result_folder = get_id_from_db('Folders', list_folders[i])

    cursor.execute(f'SELECT id FROM U_F WHERE user_id="{result_user}" AND folder_id="{result_folder}"')
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO U_F (user_id, folder_id) VALUES (?, ?);',(result_user, result_folder, ))
        connection.commit()

connection.close()
