from cogs.cogs_instant_gaming import database, ig_db

async def transfert():
    print("yop")
    for game in await database.game_database():
        print(game.price)
        game.price = float(game.price[:-1])
        await ig_db.add_game(game)