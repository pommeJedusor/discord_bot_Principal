import requests, random

async def quiz_one_piece_request():
    url = "https://api.api-onepiece.com/characters"
    datas = requests.get(url).json()
    personnage_id = random.randint(1,len(datas))
    url_perso = f"https://api.api-onepiece.com/characters/{personnage_id}"
    datas_perso = requests.get(url_perso).json()
    fruit = "n'as pas de fruit du démon"
    if datas_perso["fruit_id"]:
        datas_perso["fruit_id"] = requests.get(f"https://api.api-onepiece.com/fruits/"+str(datas_perso["fruit_id"])).json()
        fruit = f"a le {datas_perso['fruit_id']['french_name']}"
    crew = "n'as pas de crew"
    if datas_perso["crew_id"]:
        datas_perso["crew_id"] = requests.get(f"https://api.api-onepiece.com/crews/"+str(datas_perso["crew_id"])).json()
        crew = f"fait partie de {datas_perso['crew_id']['french_name']}"
    age=""
    if not datas_perso['age']=="":
        age = f"as {datas_perso['age']}, "
    size=""
    if not datas_perso['size']=="":
        size = f"fait {datas_perso['size']}, "
    life = f'est {datas_perso["status"]}'
    return f"le personnage {fruit}, {size}{age}{crew} et {life}", datas_perso['french_name']

async def validator_response_one_piece(reponse,perso):
    for word in reponse.lower().split(" "):
        if word in perso.lower().split(" "):
            return True
    return False