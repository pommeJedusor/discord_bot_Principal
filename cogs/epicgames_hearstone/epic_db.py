import sqlite3

from datas.datas import DATABASE

def delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("DROP TABLE `epic_games`")
    con.commit()

    cur.close()
    con.close()

def check():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS `epic_games` (`id` INTEGER PRIMARY KEY, `name` TEXT NOT NULL UNIQUE, `is_last` INTEGER );")
    con.commit()

    cur.close()
    con.close()


def get_games():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM `epic_games`')
    games = cursor.fetchall()

    cursor.close()
    connection.close()

    for game in games:
        print(game)

def get_last_games():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('SELECT `name` FROM `epic_games` WHERE `is_last` = 1')
    games = cursor.fetchall()

    cursor.close()
    connection.close()
    return [game[0] for game in games]

def add_game(name, is_last):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO `epic_games` (`id`, `name`, `is_last`) VALUES(?,?,?)',(None, name, is_last))
    connection.commit()
    
    cursor.close()
    connection.close()

def desactivate():
    """
    desactive is_last de tous les jeux
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `epic_games` SET `is_last` = 0 WHERE `is_last` = 1 ')
    connection.commit()
    
    cursor.close()
    connection.close()

def new_games(free_games):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    #games that have been free some time ago
    new_free_games = []
    old_free_games = []
    current_free_games = []
    for free_game in free_games:
        #search the game in the db
        cursor.execute("SELECT `is_last` FROM `epic_games` WHERE `name` = ? ",(free_game["title"],))
        result = cursor.fetchone()

        if not result:
            new_free_games.append(free_game)
        elif not result[0]:
            old_free_games.append(free_game)
        elif result[0]:
            current_free_games.append(free_game)

    #if there is a free game that has never been free
    mention = bool(new_free_games)

    #reset "last value" in db
    cursor.execute("UPDATE `epic_games` SET `is_last` = 0 WHERE `is_last` = 1")
    connection.commit()

    #set "last value" in db
    for game in (old_free_games+current_free_games):
        cursor.execute("UPDATE `epic_games` SET `is_last` = 1 WHERE `name` = ?",(game["title"],))
        connection.commit()

    #add new free games
    for free_game in new_free_games:
        new_game = (None, free_game["title"], 1)
        cursor.execute('INSERT INTO `epic_games` (`id`, `name`, `is_last`) VALUES(?,?,?)',new_game)
        connection.commit()
    
    
    connection.close()
    return (old_free_games+new_free_games), mention

check()