#module de base
import asyncio

#modules discords
import discord
from discord.ext import commands, tasks

#modules cogs
from cogs.epicgames_hearstone import check
from cogs.cogs_instant_gaming import ig_task
from datas import datas

bot=commands.Bot(command_prefix="!", intents=discord.Intents.all())


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
        if message.author.id==datas.BOT_ID:
            await message.delete()
    await interaction.response.send_message("done",delete_after=2)

@tasks.loop(hours=1)
async def general_check() -> None:
    #get hs datas
    try:
        maj_hs = await check.maj_hearstone()
    except Exception as e:
        print("hearstone error: ")
        print(e)
        maj_hs = False
    print(maj_hs)

    #get epic games datas
    try:
        new_games, should_mention = await check.new_games_epicgames()   
    except Exception as e:
        print("epic game error: ")
        print(e)
        new_games = False
    print(new_games)

    #epic game
    if new_games:
        epic_channel= bot.get_channel(datas.EPIC_GAME_CHANNEL)
        if should_mention:
            await epic_channel.send(f"<@&{datas.EPIC_GAME_ROLE}>")
        for new_game in new_games:
            await epic_channel.send(new_game.title+"\n"+new_game.description)
            await epic_channel.send(new_game.img_link)
    #hearstone
    if maj_hs:
        hearstone_channel= bot.get_channel(datas.HEARSTONE_CHANNEL)
        await hearstone_channel.send(f"<@&{datas.HEARSTONE_ROLE}>")
        await hearstone_channel.send(f"nouvelle maj hearstone : {maj_hs.title}\n{maj_hs.url}")
    #instant gaming
    games_reduce = await ig_task.main()
    ig_channel = bot.get_channel(datas.INSTANT_GAMING_CHANNEL)
    for game in games_reduce:
        await asyncio.sleep(0,2)
        text=""
        for user in game.users:
            text+=f"<@{user}>"
        await ig_channel.send(f"le jeu {game.name} est désomais à {game.price}\n{text}\n{game.link}")

bot.run(datas.BOT_TOKEN)