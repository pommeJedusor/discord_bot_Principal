import sqlite3

#from datas.file_db import DATABASE
DATABASE = "datas/database.db"

class Game:
    def __init__(self,id,name,price,image,link):
        self.id = id
        self.name = name
        self.price = price
        self.image = image
        self.link = link
        self.versions = []
        self.users = []

def check():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()



    #créer la table game
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `games_ig` (
        `game_id` INTEGER PRIMARY KEY, 
        `name` TEXT NOT NULL, 
        `price` INTEGER NOT NULL, 
        `image` TEXT NOT NULL, 
        `link` TEXT NOT NULL
        )""")
    connection.commit()

    #créer la table versions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `versions_ig` (
        `version_id` INTEGER PRIMARY KEY,
        `link_version` TEXT NOT NULL,
        `game_ig` INTEGER NOT NULL,
        FOREIGN KEY(`game_ig`) REFERENCES `games_ig`(`game_id`)
        )""")
    connection.commit()

    #créer la table user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users_ig` (
        `user_ig_id` INTEGER PRIMARY KEY,
        `game_ig` INTEGER NOT NULL,
        `user_id` INTEGER NOT NULL,
        FOREIGN KEY(`game_ig`) REFERENCES `games_ig`(`game_id`)
        )
    """)
    connection.commit()

    cursor.close()
    connection.close()

def create_versions(game):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.executemany("INSERT INTO `versions_ig`(`version_id`,`link_version`,`game_ig`) VALUES(?,?,?)",[(None,version,game.id) for version in game.versions])
    connection.commit()

    cursor.close()
    connection.close()



def create_game(game):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO `games_ig`(`game_id`,`name`,`price`,`image`,`link`) VALUES(?,?,?,?,?)",(None, game.name, game.price, game.image, game.link))
    connection.commit()

    cursor.execute("""
        SELECT `game_id`
        FROM `games_ig`
        WHERE `name` = ?
    """,(game.name,))
    results = cursor.fetchall()
    game_id = results[-1][0]
    game.id = game_id

    cursor.close()
    connection.close()

def create_user(user_id,game_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO `users_ig`
        (`user_ig_id`,`game_ig`,`user_id`)
        VALUES(?,?,?)
    """,(None,game_id,user_id))
    connection.commit()
    
    cursor.close()
    connection.close()

def add_game(game):
    #vérifie si le jeu eet ses versions sont déjà dans la base de données
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
            SELECT `game_id`, `link_version`
            FROM `versions_ig`
            INNER JOIN  `games_ig` on `versions_ig`.`game_ig` = `games_ig`.`game_id`
            WHERE `name` = ?
        """,(game.name,))

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    games_match = []
    
    for result in results:
        find = False
        for game_match in games_match:
            if game_match[0]==result[0]:
                find=True
                game_match[1].append(result[1])

        if not find:
            games_match.append([result[0],[result[1]]])

    #férifie si les jeux trouvés match parfaitement
    already_exists = False
    for game_match in games_match:
        if sorted(game_match[1]) == sorted(game.versions):
            already_exists = True
            game.id = game_match[0]
    
    #si le jeu n'éxiste pas encore dans db le créer
    if not already_exists:
        create_game(game)
        create_versions(game)
        create_user(game.users[0],game.id)
    
    else:
        create_user(game.users[0],game.id)
    




def all_games():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT `game_id`, `name`, `price`, `image`, `link`
        FROM `games_ig`
        """)
    games = []
    games_table = cursor.fetchall()
    for game_table in games_table:
        game_table
        id, name, price, image, link = game_table
        game_table = Game (id,name,price,image,link)
        games.append(game_table)
    
    #récup les users
    for game in games:
        cursor.execute("""
            SELECT `user_id`
            FROM `users_ig`
            WHERE `game_ig` = ?
        """,(game.id,))
        users = cursor.fetchall()
        game.users = [user[0] for user in users]

    #récup les versions
    for game in games:
        cursor.execute("""
            SELECT `link_version`
            FROM `versions_ig`
            WHERE `game_ig` = ?
        """,(game.id,))
        versions = cursor.fetchall()
        game.versions = [version[0] for version in versions]


    cursor.close()
    connection.close()

    return games

def delete_game(game_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    #supprime de la table games_ig
    cursor.execute('DELETE FROM `games_ig` WHERE `game_id` = ?',(game_id,))
    connection.commit()

    #supprime de la table versions_ig
    cursor.execute('DELETE FROM `versions_ig` WHERE `game_ig` = ?',(game_id,))
    connection.commit()

    #supprime de la table games_ig
    cursor.execute('DELETE FROM `users_ig` WHERE `game_ig` = ?',(game_id,))
    connection.commit()


    cursor.close()
    connection.close()

def update_price(game_id,game_price):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('UPDATE `games_ig` SET `price` = ? WHERE `game_id` = ?',(game_price,game_id))
    connection.commit()
    
    cursor.close()
    connection.close()

check()