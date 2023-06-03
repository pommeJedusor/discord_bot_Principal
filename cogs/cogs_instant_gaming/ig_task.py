from cogs.cogs_instant_gaming import scrap, ig_db

async def main():
    final_games = []
    games = await ig_db.all_games()
    for game in games:
        price = await scrap.get_price(game)
        if game.price > price:
            game.price = price
            await ig_db.update_price(game.id,game.price)
            final_games.append(game)
        elif game.price < price:
            game.price = price
            await ig_db.update_price(game.id,game.price)
    return final_games