from cogs.epicgames_hearstone import hs_db, epic_db
from datas import datas
import json

with open(datas.hearstone_file, 'r') as f:
    maj = json.loads(f.read())[0]
with open(datas.epicgame_file, 'r') as f:
    games = json.loads(f.read())


hs_db.delete()
hs_db.check()

epic_db.delete()
epic_db.check()

hs_db.first_maj(maj)
epic_db.new_games([{"title":game} for game in games])