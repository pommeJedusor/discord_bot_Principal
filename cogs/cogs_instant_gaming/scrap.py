import requests
from bs4 import BeautifulSoup

from cogs.cogs_instant_gaming.database import Game
#from database import Game

URL = "https://www.instant-gaming.com/fr/rechercher/?query="

HEADERS = {'authority': 'www.instant-gaming.com',
'method': 'GET',
'path': '/fr/rechercher/?query=cult',
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'deflate',
'accept-language': 'fr-FR,fr;q=0.9',
'cache-control': 'max-age=0',
'cookie': 'ig_tz=Europe%2FBrussels; cf_chl_2=b73deb2853cad0b; cf_clearance=DunTSnAETSiMEAEthsCLdoN51STkAR.pSjiGKB83p6s-1684787335-0-160; ig_location=fr; PHPSESSID=41b97e4a4b2fcd4111bad91cca658a95',
'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'sec-gpc': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}



def get_versions(link):
    r = requests.get(url = link,headers=HEADERS)
    #print(r)
    soup = BeautifulSoup(r.text,'html.parser')
    try:
        list_version = soup.find('div',{'class':'choices'})
        versions = list_version.find('ul',{'class':'list'})
        versions = list_version.find('select',{'id':'platforms-choices'})
        versions = versions.findAll('option')
        versions = [version['data-href'] for version in versions]
        return versions
    except AttributeError:
        return [link]


def get_games(name, number):
    """
    retourne une lisre de number jeux les plus probable avec le nom
    """
    #request
    url = URL+name
    r = requests.get(url=url,headers=HEADERS)
    #print(r)

    #parsage
    soup = BeautifulSoup(r.text,'html.parser')
    all_games = soup.find('div',{'class':'search listing-games'})
    games = all_games.findAll('div',{'class':'item force-badge categoryBest'})
    games.extend(all_games.findAll('div',{'class':'item force-badge'}))
    #print(f"nb games: {len(games)}")

    #compilation des jeux
    Games=[]

    for game in games:
        price = game.find('div',{'class':'price'})
        if price:
            price=price.text
        name = game.find('span',{'class':'title'}).text
        discount = game.find('div',{'class':'discount'})
        if discount:
            discount=discount.text
        image = game.find('img',{'class':'picture'})['data-src']
        link = game.find('a',{'class':'cover video'})
        if not link:
            link = game.find('a',{'class':'cover'})
        link = link['href']
        Games.append(Game(name,price,image,link))

    return Games[:number]

def get_price(game):
    """
    retourne le prix de la version la moins chère
    """
    prices_versions = []
    for version in game.versions:
        r = requests.get(url=version,headers=HEADERS)
        print(version)
        soup = BeautifulSoup(r.text,'html.parser')
        stock = soup.find('div',{'class':'stock'})
        if stock:
            print("en stock")
            price = soup.find('div',{'class':'total'}).text
            print(price)
            prices_versions.append(float(price[:-1]))
        else:
            print("pas en stock")
    return min(prices_versions)