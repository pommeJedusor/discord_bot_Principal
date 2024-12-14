import sqlite3

from datas.datas import DATABASE


class EpicGamesGames:
    def __init__(self, title: str, description: str, img_link: str) -> None:
        self.title = title
        self.description = description
        self.img_link = img_link

    @staticmethod
    def get_last_games() -> list[str]:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT `name` FROM `epic_games_games` WHERE `is_last` = 1")
        games = cursor.fetchall()

        cursor.close()
        connection.close()
        return [game[0] for game in games]

    @staticmethod
    def unlast_all() -> None:
        """
        deactivate is_last for all games
        """
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE `epic_games_games` SET `is_last` = 0 WHERE `is_last` = 1"
        )
        connection.commit()

        cursor.close()
        connection.close()

    @staticmethod
    def add_game(name: str, is_last: bool = True) -> None:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO `epic_games_games` (`id`, `name`, `is_last`) VALUES(?,?,?)",
            (None, name, is_last),
        )
        connection.commit()

        cursor.close()
        connection.close()

    @staticmethod
    def set_game_as_last(name: str) -> None:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE `epic_games_games` SET `is_last` = 1 WHERE `name` = ?", (name,)
        )
        connection.commit()

        cursor.close()
        connection.close()

    @staticmethod
    def init():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS epic_games_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                is_last INTEGER NOT NULL
            );
        """
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()
