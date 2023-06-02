import sqlite3

DATABASE = "datas/database.db"


def delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("DROP TABLE `hearstone`")
    con.commit()

    cur.close()
    con.close()

def check():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS `hearstone` (`id` INTEGER PRIMARY KEY, `link` TEXT NOT NULL UNIQUE);")
    connection.commit()

    cursor.close()
    connection.close()

def get_last_maj():
    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT `link` FROM `hearstone`')
        maj = cursor.fetchall()

        cursor.close()
        connection.close()
        return maj[0][0]
    except IndexError:
        return False

def new_maj(link):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `hearstone` SET `link` = ?',(link,))
    connection.commit()

    cursor.close()
    connection.close()

def first_maj(link):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `hearstone` (`id`,`link`) VALUES(?,?)',(1,link))
    connection.commit()

    cursor.close()
    connection.close()

check()