import sqlite3

from datas.datas import DATABASE


def delete() -> None:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("DROP TABLE `hearstone`")
    con.commit()

    cur.close()
    con.close()

def check() -> None:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS `hearstone` (`id` INTEGER PRIMARY KEY, `link` TEXT NOT NULL UNIQUE);")
    connection.commit()

    cursor.close()
    connection.close()

def get_last_maj() -> str|bool:
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

def new_maj(link:str, is_first_maj:bool) -> None:
    if is_first_maj:return first_maj(link)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `hearstone` SET `link` = ?',(link,))
    connection.commit()

    cursor.close()
    connection.close()

def first_maj(link:str) -> None:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `hearstone` (`id`,`link`) VALUES(?,?)',(1,link))
    connection.commit()

    cursor.close()
    connection.close()

check()