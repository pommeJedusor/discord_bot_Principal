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

def add_game(name,price,image,link):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO `games_ig`(`game_id`,`name`,`price`,`image`,`link`) VALUES(?,?,?,?,?)",(None, name, price, image, link))
    connection.commit()

    cursor.close()
    connection.close()

def get_games_player(user_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT `name`, `price`, `image`, `link_version`, `link`
        FROM `users_ig` 
        INNER JOIN `versions_ig` on `users_ig`.`game_ig` = `versions_ig`.`game_ig`
        INNER JOIN `games_ig` on `users_ig`.`game_ig` = `games_ig`.`game_id`
        WHERE `user_id` = ?""",(user_id,))
    users = cursor.fetchall()

    for user in users:
        print(f"name: {user[0]}\nprice: {user[1]}\nimage: {user[2]}\nlink {user[3]}\nlink: {user[4]}")
        print()

    cursor.close()
    connection.close()

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
        print(game_table)
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



check()