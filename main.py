# module de base
import asyncio

# modules discords
import discord
from discord.ext import commands, tasks

# modules cogs
from cogs.epicgames_hearstone import check
from cogs.cogs_instant_gaming import ig_task
from datas import datas

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.one_piece_quiz.cogs_quiz")
        await bot.load_extension("cogs.cogs_roue.roue")
        await bot.load_extension("cogs.cogs_spy_fall.spyfall")
        await bot.load_extension("cogs.cogs_instant_gaming.ig")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)
    general_check.start()


@bot.tree.command(name="delete_ussop_message")
async def delete_ussop_message(interaction: discord.Interaction):
    async for message in interaction.channel.history(limit=200):
        # TODO remove bot_id from config file (bot.user.id)
        if message.author.id == datas.BOT_ID:
            await message.delete()
    await interaction.response.send_message("done", delete_after=2)


async def hs_check() -> None:
    try:
        maj_hs = await check.maj_hearstone()
    except Exception as e:
        print("hearstone check failed: ")
        print(e)
        return
    if not maj_hs:
        return

    print(maj_hs)
    hearstone_channel = bot.get_channel(datas.HEARSTONE_CHANNEL)
    if not hearstone_channel:
        print(f"failed to find hearstone channel of id: {datas.HEARSTONE_CHANNEL}")
        return
    if not isinstance(hearstone_channel, discord.TextChannel):
        print(
            f"was expecting a channel of type text but got: {type(hearstone_channel).__name__} for hearstone channel of id: {datas.HEARSTONE_CHANNEL}"
        )
        return

    await hearstone_channel.send(f"<@&{datas.HEARSTONE_ROLE}>")
    await hearstone_channel.send(
        f"nouvelle maj hearstone : {maj_hs.title}\n{maj_hs.url}"
    )


async def epic_check() -> None:
    try:
        new_games, should_mention = await check.new_games_epicgames()
    except Exception as e:
        print("epic game error: ")
        print(e)
        return

    if not new_games:
        return

    print(new_games)
    if new_games:
        epic_channel = bot.get_channel(datas.EPIC_GAME_CHANNEL)
        if should_mention:
            await epic_channel.send(f"<@&{datas.EPIC_GAME_ROLE}>")
        for new_game in new_games:
            await epic_channel.send(new_game.title + "\n" + new_game.description)
            await epic_channel.send(new_game.img_link)


async def instant_gaming_check() -> None:
    games_reduce = await ig_task.main()
    ig_channel = bot.get_channel(datas.INSTANT_GAMING_CHANNEL)
    for game in games_reduce:
        await asyncio.sleep(0, 2)
        text = ""
        for user in game.users:
            text += f"<@{user}>"
        await ig_channel.send(
            f"le jeu {game.name} est désomais à {game.price}\n{text}\n{game.link}"
        )


@tasks.loop(hours=1)
async def general_check() -> None:
    await hs_check()
    await epic_check()
    await instant_gaming_check()


bot.run(datas.BOT_TOKEN)
