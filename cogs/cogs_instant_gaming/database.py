import pickle

DATA_FILE = 'test.data'

class Game:
    def __init__(self,name,price,image,link):
        self.name = name
        self.price = price
        self.image = image
        self.link = link
        self.versions = []
        self.users = []

async def new_database(game):
    """
    écrase la base de donné avec le jeu donné en paramêtre 
    """
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump([game])

async def game_database():
    """
    retourne tous les jeux dans la base de données
    """
    with open(DATA_FILE,'rb') as f:
        result = pickle.Unpickler(f).load()
    return result

async def newgame_dtb(game):
    """
    ajoute le jeu à la base de donnéeS
    """
    found = False
    database = await game_database()
    for game_dtb in database:
        if sorted(game_dtb.versions)==sorted(game.versions):
            if game.users[0] in game_dtb.users:
                return
            game_dtb.users.append(game.users[0])
            found = True
            break
    if not found:
        database.append(game)
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(database)

async def delete_game(game_name):
    game_find = False
    games = await game_database()
    for game in games:
        if game.name==game_name:
            game_find=True
            games.remove(game)
            break
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(games)
    return game_find

async def update_game(game_find):
    """
    update le jeu dans la base de donné et renvoi si cela a réussis ou échoué
    """
    find=False
    games = await game_database()
    for game in games:
        if game.name == game_find.name:
            find=True
            games.remove(game)
            games.append(game_find)
            break
    with open(DATA_FILE,'wb') as f:
        pickle.Pickler(f).dump(games)
    return find