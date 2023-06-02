import sqlite3

from datas.file_db import DATABASE

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

    cursor.execute('INSERT OR IGNORE INTO `epic_games` (`id`, `name`, `is_last`) VALUES(?,?,?)',(cursor.lastrowid, name, is_last))
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

    #récup les jeux qu'ont le même noms que ceux qui sont actuellement gratuits
    games = []
    for game_name in free_games:
        cursor.execute("SELECT `name`, `is_last` FROM `epic_games` WHERE `name` = ? ",(game_name["title"],))
        result = cursor.fetchone()
        if result:
            games.append(result)

    #si pas de nouveau jeu retourne rien
    new_free_games = []
    for free_game in free_games:
        if not (free_game["title"],1) in games:
            new_free_games.append(free_game)
    """
    if not new_free_games:
        return False, False"""

    #vérifie si il y a un jeu qui n'as pas déjà été gratuit
    mention = True
    if len(games)==len(free_games):
        mention = False

    #mais tous les jeux en non last
    cursor.execute("UPDATE `epic_games` SET `is_last` = 0 WHERE `is_last` = 1")
    connection.commit()

    #update les nouveaux jeux gratuits si ils étaient déjà dans la base de données
    for game in games:
        cursor.execute("UPDATE `epic_games` SET `is_last` = 1 WHERE `name` = ?",(game[0],))
        connection.commit()

    #ajoute les nouveaux jeux
    for free_game in new_free_games:
        if not (free_game["title"],0) in games:
            new_games = (None, free_game["title"], 1)
            cursor.execute('INSERT INTO `epic_games` (`id`, `name`, `is_last`) VALUES(?,?,?)',new_games)
            connection.commit()
    
    
    connection.close()
    return new_free_games, mention

check()