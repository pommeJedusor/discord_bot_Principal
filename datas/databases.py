import sqlite3

DATABASE = "datas/database.db"

def delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("DROP TABLE `id`")
    con.commit()

    cur.close()
    con.close()

def check_db():
    """vérifie si la database éxiste sinon la crée"""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('create table if not exists `id` (`id` INTEGER PRIMARY KEY,`name_id` VARCHAR(65) UNIQUE, `true_id` INT NOT NULL);')
    connection.commit()

    cursor.close()
    connection.close()

def add_id(name, id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `id` (`id`, `name_id`, `true_id`) VALUES(?,?,?)',(cursor.lastrowid, name, id))
    connection.commit()
    
    cursor.close()
    connection.close()

def get_id(name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT `true_id` FROM `id` WHERE `name_id` = ?',(name,))
    id = cursor.fetchone()

    cursor.close()
    connection.close()

    if not id:
        id = int(input(f"id de {name} non trouvé\nveuillez l'entrez s'il vous plait\n"))
        add_id(name,id)
    else:
        id = id[0]
    return id

def get_all_ids():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM `id`')
    ids = cursor.fetchall()

    cursor.close()
    connection.close()
    for id in ids:
        print(id)

def change_id(name, new_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `id` SET `true_id` = ? WHERE `name_id` = ?',(new_id,name))
    connection.commit()
    
    cursor.close()
    connection.close()

check_db()