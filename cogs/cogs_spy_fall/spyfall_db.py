import sqlite3

DATABASE = "datas/spyfall.db"

def check_db():
    """vérifie si la database éxiste sinon la crée"""
    connection = sqlite3.connect("DATABASE")
    cursor = connection.cursor()

    cursor.execute('create table if not exists `locations` (`id_location` INTEGER PRIMARY KEY AUTOINCREMENT, `name_location` varchar(65) not null unique);')
    connection.commit()
    connection.close()

def get_locations():
    connection = sqlite3.connect("DATABASE")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM `locations`')
    locations = cursor.fetchall()

    connection.close()
    return [location[1] for location in locations]

def add_location(name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `locations` (`name_location`) VALUES(?)',(name,))
    connection.commit()
    connection.close()

def see_locations():
    for location in get_locations():
        print(location)

check_db()