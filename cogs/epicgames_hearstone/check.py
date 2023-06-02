import requests, json

import datas.datas as datas

from cogs.epicgames_hearstone import hs_epic_db as db

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

    return db.new_games(free_games)


async def maj_hearstone():
    url2="https://hearthstone.blizzard.com/fr-fr/api/blog/articleList/?page=1&pageSize=1&tagsList[]=patch"
    requete=requests.get(url2)
    print("hearstone")
    print(requete)
    requet_hearstone=json.loads(requete.content)
    last_maj_hearstone_title=requet_hearstone[0]['title']
    last_maj_hearstone_url = requet_hearstone[0]["defaultUrl"]
    with open(datas.hearstone_file,"r") as f:
        last_maf_file = json.loads(f.readline())
    if not last_maj_hearstone_url in last_maf_file:
        with open(datas.hearstone_file,"w") as f:
            f.write(json.dumps([last_maj_hearstone_url]))
        return {"title":last_maj_hearstone_title,"url":last_maj_hearstone_url}
    return None