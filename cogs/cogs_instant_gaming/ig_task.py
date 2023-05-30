from cogs.cogs_instant_gaming import database, scrap

async def main():
    final_games = []
    games = await database.game_database()
    for game in games:
        price = await scrap.get_price(game)
        if float(game.price[:-1]) > price:
            game.price = str(price)+"€"
            await database.update_game(game)
            final_games.append(game)
        elif float(game.price[:-1]) < price:
            game.price = str(price)+"€"
            await database.update_game(game)
    return final_games