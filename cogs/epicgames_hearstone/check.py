import requests, json

import datas.datas as datas

from cogs.epicgames_hearstone import epic_db as epic_db
from cogs.epicgames_hearstone import hs_db as hs_db

async def new_games_epicgames():
    #récup les jeux gratuits et les stocks dans free_games
    r=requests.get("https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=fr-US&country=BE&allowCountries=BE")
    print("epicgame")
    print(r)
    free_games=[]
    elements=json.loads(r.content)["data"]["Catalog"]["searchStore"]["elements"]
    for element in elements:
        if element["promotions"] and element["promotions"]["promotionalOffers"] and 0==element["price"]["totalPrice"]["discountPrice"]:
            free_games.append({"title":element["title"],"description":element["description"],"image":element["keyImages"][0]['url'],"date de fin":element["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]})

    return epic_db.new_games(free_games)


async def maj_hearstone():
    url2="https://hearthstone.blizzard.com/fr-fr/api/blog/articleList/?page=1&pageSize=1&tagsList[]=patch"
    requete=requests.get(url2)
    print("hearstone")
    print(requete)
    requet_hearstone=json.loads(requete.content)
    last_maj_hearstone_title=requet_hearstone[0]['title']
    last_maj_hearstone_url = requet_hearstone[0]["defaultUrl"]

    
    last_maj_file = hs_db.get_last_maj()
    
    if not last_maj_file:
        hs_db.first_maj(last_maj_hearstone_url)
        return {"title":last_maj_hearstone_title,"url":last_maj_hearstone_url}
    elif not last_maj_hearstone_url == last_maj_file:
        hs_db.new_maj(last_maj_hearstone_url)
        return {"title":last_maj_hearstone_title,"url":last_maj_hearstone_url}
    return None