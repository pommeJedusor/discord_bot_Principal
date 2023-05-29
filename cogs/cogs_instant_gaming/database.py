import pickle

DATA_FILE = 'test.data'

class Game:
    def __init__(self,name,price,discount,image,link):
        self.name = name
        self.price = price
        self.discount = discount
        self.image = image
        self.link = link
        self.versions = []
        self.users = []

def new_database(game):
    """
    écrase la base de donné avec le jeu donné en paramêtre 
    """
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump([game])

def game_database():
    """
    retourne tous les jeux dans la base de donnéesS
    """
    with open(DATA_FILE,'rb') as f:
        result = pickle.Unpickler(f).load()
    return result

def newgame_dtb(game):
    """
    ajoute le jeu à la base de donnéeS
    """
    database = game_database()
    database.append(game)
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(database)

def delete_game(game_name):
    game_find = False
    games = game_database()
    for game in games:
        if game.name==game_name:
            game_find=True
            games.remove(game)
            break
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(games)
    return game_find

def update_game(game_find):
    """
    update le jeu dans la base de donné et renvoi si cela a réussis ou échoué
    """
    find=False
    games = game_database()
    for game in games:
        if game.name == game_find.name:
            find=True
            games.remove(game)
            games.append(game_find)
            break
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(games)
    return find