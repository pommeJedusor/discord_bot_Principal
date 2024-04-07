import sqlite3

from datas.datas import DATABASE

def check_db():
    """vérifie si la database éxiste sinon la crée"""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('create table if not exists `locations` (`id_location` INTEGER PRIMARY KEY, `name_location` varchar(65) not null unique);')
    connection.commit()

    cursor.close()
    connection.close()

def get_locations():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM `locations`')
    locations = cursor.fetchall()

    cursor.close()
    connection.close()
    return [location[1] for location in locations]

def add_location(name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `locations` (`id_location`, `name_location`) VALUES(?,?)',(cursor.lastrowid, name))
    connection.commit()
    
    cursor.close()
    connection.close()

def delete_location(name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM `locations` WHERE `name_location` = ?',(name,))
    connection.commit()
    
    cursor.close()
    connection.close()

def rename_location(old_name, new_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `locations` SET `name_location` = ? WHERE `name_location` = ?',(new_name,old_name))
    connection.commit()
    
    cursor.close()
    connection.close()

def see_locations():
    for location in get_locations():
        print(location)

check_db()