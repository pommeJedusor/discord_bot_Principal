import sqlite3

DATABASE = "datas/database.db"

def delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("DROP TABLE `file`")
    con.commit()

    cur.close()
    con.close()

def check_db():
    """vérifie si la database éxiste sinon la crée"""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('create table if not exists `file` (`id` INTEGER PRIMARY KEY,`name_file` VARCHAR(65) UNIQUE, `file_path` TEXT);')
    connection.commit()

    cursor.close()
    connection.close()

def add_file(name, file_path):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `file` (`id`, `name_file`, `file_path`) VALUES(?,?,?)',(cursor.lastrowid, name, file_path))
    connection.commit()
    
    cursor.close()
    connection.close()

def get_path(name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT `file_path` FROM `file` WHERE `name_file` = ?',(name,))
    file_path = cursor.fetchone()

    cursor.close()
    connection.close()

    if not file_path:
        file_path = input(f"le path de {name} non trouvé\nveuillez l'entrez s'il vous plait\n")
        add_file(name,file_path)
    else:
        file_path = file_path[0]
    return file_path

def get_all_path():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM `file`')
    paths = cursor.fetchall()

    cursor.close()
    connection.close()
    for path in paths:
        print(path)

def change_path(name, new_path):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `file` SET `file_path` = ? WHERE `name_file` = ?',(new_path,name))
    connection.commit()
    
    cursor.close()
    connection.close()

check_db()