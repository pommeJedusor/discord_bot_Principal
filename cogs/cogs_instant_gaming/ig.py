import discord
from discord.ext import commands
from discord import app_commands

from cogs.cogs_instant_gaming import scrap, database

class DropdownVersions(discord.ui.Select):
    def __init__(self,bot,game,versions):
        self.bot = bot
        self.versions = versions
        self.all_versions = scrap.get_versions(game.link)

        options=[]
        compteur = 0
        for version in self.all_versions:
            options.append(discord.SelectOption(label=version[-50:],value=compteur))
            compteur+=1

        super().__init__(placeholder="choisissez la version du jeu", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        version = self.all_versions[int(self.values[0])]
        if version in self.versions:
            self.versions.remove(version)
        else:
            self.versions.append(version)
        text = "les versions séléctionnées:\n"
        for version in self.versions:
            text+=f"{version}\n"
        await interaction.response.edit_message(content=text)

class DropdownViewVersions(discord.ui.View):
    def __init__(self,bot,games_find):
        super().__init__()
        self.versions = []
        self.game = games_find
        self.add_item(DropdownVersions(bot,games_find,self.versions))
    
    @discord.ui.button(label="valider")
    async def validate(self,interaction:discord.Interaction, button:discord.Button):
        await interaction.response.edit_message(content="je réfléchit",view=None)
        self.game.versions = self.versions
        self.game.users.append(interaction.user.id)
        self.game.price = str(await scrap.get_price(self.game))+"€"
        await database.newgame_dtb(self.game)
        await interaction.edit_original_response(content=f"{self.versions}",view=None)



class Dropdown(discord.ui.Select):
    def __init__(self,bot,games_find):
        self.bot = bot
        self.games_find = games_find

        options=[]
        compteur = 0
        for game in games_find:
            options.append(discord.SelectOption(label=game.name,value=compteur))
            compteur+=1

        super().__init__(placeholder="choisissez la version du jeu", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="je réfléchit",view=None)
        game_name = self.options[int(self.values[0])].label
        games_find = [game for game in self.games_find if game.name==game_name]
        view=DropdownViewVersions(self.bot,games_find[0])
        await interaction.edit_original_response(content=f"choisisser les versions qui vous intéressent",view=view)

class DropdownView(discord.ui.View):
    def __init__(self,bot,games_find):
        super().__init__()

        self.add_item(Dropdown(bot,games_find))

class InstantGaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="ig_ajouter_jeu",description="permet d'ajouter un jeu à la liste")
    async def add_game(self,interaction:discord.Interaction,name:str):
        await interaction.response.defer(ephemeral=True)
        games = await scrap.get_games(name=name,number=10)
        if games==[]:
            await interaction.edit_original_response(content="jeu non trouvé veuillez vérifier l'orhtographe",view=None)
        else:
            view = DropdownView(self.bot,games)
            await interaction.edit_original_response(content="choisissez votre jeu",view=view)

    @app_commands.command(name="ig_voir_jeux",description="permet de voir les jeux dont on suit l'activité des prix")
    async def games_ig(self,interaction:discord.Interaction):
        games = await database.game_database()
        text="vos jeux:\n"
        for game in games:
            if interaction.user.id in game.users:
                if game.price=="1000€":
                    text+=f"{game.name}: hors stock\n"
                else:
                    text+=f"{game.name}: {game.price}\n"
        await interaction.response.send_message(text,ephemeral=True)

    @app_commands.command(name="ig_supprimer_jeu",description="permet de supprimer un jeu de ceux que l'on suit")
    async def delete_game(self,interaction:discord.Interaction,name:str):
        find = False
        games = await database.game_database()
        for game in games:
            if game.name==name and interaction.user.id in game.users:
                find = True
                the_game = game

        if not find:
            await interaction.response.send_message("jeux non trouvé")
        else:
            await database.delete_game(the_game.name)
            if not the_game.users == [interaction.user.id]:
                the_game.users.remove(interaction.user.id)
                await database.newgame_dtb(the_game)
            await interaction.response.send_message(f"le jeu {the_game.name} a été supprimé avec succès",ephemeral=True)

        




async def setup(bot):
    await bot.add_cog(InstantGaming(bot))