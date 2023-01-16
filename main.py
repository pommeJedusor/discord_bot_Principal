#module de base
import json, requests

#modules discords
import discord
from discord.ext import commands, tasks

#modules cogs
from cogs.epicgames_hearstone import check
from cogs.one_piece_quiz import quiz
from datas import datas


bot=commands.Bot(command_prefix="!", intents=discord.Intents.all())
perso=""
MY_GUILD = discord.Object(id=datas.GUIL_ID)




@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)
    general_check.start()


@tasks.loop(hours=1)
async def general_check():
    maj_hs = await check.maj_hearstone()
    new_game = await check.new_games_epicgames()   
    print(maj_hs)
    print(new_game) 
    if new_game:
        pomme= bot.get_channel(datas.epicgame_channel)
        await pomme.send(f"<@&{datas.role_epicgame}>")
        for new_game in new_game:
            await pomme.send(new_game['title']+"\n"+new_game['description'])
            await pomme.send(new_game['image'])
    if maj_hs:
        pomme= bot.get_channel(datas.hearstone_channel)
        await pomme.send(f"<@&{datas.role_hearstone}>")
        await pomme.send(f"nouvelle maj hearstone : {maj_hs['title']}\n{maj_hs['url']}")


@bot.tree.command(name="quiz_one_piece",description="permet de participer à un quiz")
async def quiz_one_piece(interaction: discord.Interaction):
    global perso
    perso = await quiz.quiz_one_piece()
    await interaction.response.send_message(perso[0])
    perso = perso[1]

@bot.tree.command(name="soluce_one_piece",description="permet de répondre au quiz")
async def soluce_one_piece(interaction: discord.Interaction,reponse:str):
    global perso    
    if await quiz.validator_response_one_piece(reponse,perso):
        await interaction.response.send_message(f"bonne réponse le perso était bel est bien {perso}")
        perso=""
    elif not perso:
        await interaction.response.send_message("pas de quiz en cours")
    else:
        await interaction.response.send_message(f"mauvaise réponse le perso était {perso}")
        perso=""




bot.run(datas.BOT_TOKEN)
