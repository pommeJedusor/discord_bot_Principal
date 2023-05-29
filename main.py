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
MY_GUILD = discord.Object(id=datas.GUIL_ID)


@bot.event
async def on_ready():
    try:
        await bot.load_extension('cogs.one_piece_quiz.cogs_quiz')
        await bot.load_extension('cogs.cogs_roue.roue')
        await bot.load_extension('cogs.cogs_spy_fall.spyfall')
        await bot.load_extension('cogs.cogs_instant_gaming.ig')
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)
    general_check.start()


@bot.tree.command(name="delete_ussop_message")
async def delete_ussop_message(interaction:discord.Interaction):
    async for message in interaction.channel.history(limit=200):
        if message.author.id==992095372090540214:
            await message.delete()
    await interaction.response.send_message("done",delete_after=2)

@tasks.loop(hours=1)
async def general_check():
    maj_hs = await check.maj_hearstone()
    new_game = await check.new_games_epicgames()   
    print(maj_hs)
    print(new_game) 
    if new_game:
        epic_channel= bot.get_channel(datas.epicgame_channel)
        await epic_channel.send(f"<@&{datas.role_epicgame}>")
        for new_game in new_game:
            await epic_channel.send(new_game['title']+"\n"+new_game['description'])
            await epic_channel.send(new_game['image'])
    if maj_hs:
        hearstone_channel= bot.get_channel(datas.hearstone_channel)
        await hearstone_channel.send(f"<@&{datas.role_hearstone}>")
        await hearstone_channel.send(f"nouvelle maj hearstone : {maj_hs['title']}\n{maj_hs['url']}")


bot.run(datas.BOT_TOKEN)