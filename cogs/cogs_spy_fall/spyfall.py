import discord
from discord import app_commands
from discord.ext import commands

import random

from cogs.cogs_spy_fall import spyfall_db

class GameFinish(discord.ui.View):
    def __init__(self, old_self) :
        super().__init__()
        self.bot = old_self.bot
        self.players = old_self.players

    @discord.ui.button(label="recommencer")
    async def restart(self,interaction:discord.Interaction, button:discord.Button):
        await interaction.response.edit_message(content="la game va recommencer",view=ViewLobby(len(self.players),self.bot))

class DropDownVoteSpy(discord.ui.Select):
    def __init__(self,old_self):
        self.bot = old_self.bot
        self.players = old_self.players
        self.location = old_self.location
        self.vote = []

        options = []
        for player in self.players:
            options.append(discord.SelectOption(label=player["user"].name,value=player["user"].name))

        super().__init__(placeholder="votez,... mais qui?", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        #identifie le player
        player_filter = lambda x: x["user"]==interaction.user
        player = list(filter(player_filter,self.players))
        #identifie son précédent vote si existant
        vote_filter = lambda x: x["username_voteur"]==interaction.user.name
        voteur = list(filter(vote_filter,self.vote))
        if player and not voteur:
            self.vote.append({"username_voteur":player[0]["user"].name,"username_voter":self.values[0]})
            if len(self.vote)>=len(self.players):
                #identifie le nombre de vote pour chaque personne
                votes_compteur = []
                for vote in self.vote:
                    is_already_voted=False
                    for vote_compteur in votes_compteur:
                        if vote_compteur["username_voter"]==vote["username_voter"]:
                            vote_compteur["nb_votes"]+=1
                            is_already_voted=True
                    if not is_already_voted:
                        votes_compteur.append({"username_voter":vote["username_voter"],"nb_votes":1})

                #identifie le plus voté et si égalité
                egal = False
                num_plus_elever = 0
                name_most_voted = "personne"
                for vote in votes_compteur:
                    if vote["nb_votes"]>num_plus_elever:
                        egal = False
                        num_plus_elever = vote["nb_votes"]
                        name_most_voted = vote["username_voter"]
                    elif vote["nb_votes"]==num_plus_elever:
                        egal = True
                
                if not egal:
                    player_filter = lambda x: x["user"].name==name_most_voted
                    player = list(filter(player_filter,self.players))
                    impostor_filter = lambda x: x["is_impostor"]
                    impostor = list(filter(impostor_filter,self.players))
                    if player[0]["is_impostor"]:
                        await interaction.response.edit_message(content=f"{name_most_voted} était bien l'imposteur et a perdu la partie,\nle lieu était: {self.location}",view=GameFinish(self))
                    else:
                        await interaction.response.edit_message(content=f"{name_most_voted} a été voté\nmalheureusement, l'imposteur était {impostor[0]['user'].name}\nle lieu était: {self.location}",view=GameFinish(self))
                else:
                    await interaction.response.edit_message(content=f"égalité les votes sont réinitialisés")
                    self.vote=[]
                    

            else:
                await interaction.response.edit_message(content = f"nombre de votes: {len(self.vote)}")
        elif not player:
            await interaction.response.send_message(f"vous n'êtes pas dans la partie",ephemeral=True)
        elif voteur:
            self.vote.remove(voteur[0])
            self.vote.append({"username_voteur":player[0]["user"].name,"username_voter":self.values[0]})
            await interaction.response.send_message(f"{player[0]['user'].name} vous voté désormais pour {self.values[0]}",ephemeral=True)
        


class VoteView(discord.ui.View):
    def __init__(self,old_self):
        super().__init__(timeout=None)
        self.bot = old_self.bot
        self.players = old_self.players
        self.location = old_self.location
        self.add_item(DropDownVoteSpy(self))

class DropDownViewSpy(discord.ui.Select):
    def __init__(self,old_self):
        self.bot = old_self.bot
        self.players = old_self.players
        self.location = old_self.location
        options = []
        locations = spyfall_db.get_locations()
        for location in locations:
            options.append(discord.SelectOption(label=location,value=location))
        super().__init__(placeholder="choisissez votre réponse", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        player_filter = lambda x: x["user"]==interaction.user
        player = list(filter(player_filter,self.players))
        if player and player[0]["is_impostor"] and self.values[0]==self.location:
            await interaction.response.edit_message(content=f"{interaction.user.name} a gagné la partie, le lieu était bel et bien {self.location}",view=GameFinish(self))
        elif not player:
            await interaction.response.send_message(f"vous n'êtes pas dans la partie",ephemeral=True)
        elif not player[0]["is_impostor"]:
            await interaction.response.send_message(f"vous n'êtes pas l'imposteur",ephemeral=True)
        elif not self.values[0]==self.location:
            await interaction.response.edit_message(content=f"{interaction.user.name} a perdu la partie, le lieu était {self.location}",view=GameFinish(self))

class SpyView(discord.ui.View):
    def __init__(self,old_self):
        super().__init__()
        self.bot = old_self.bot
        self.players = old_self.players
        self.location = old_self.location
        self.add_item(DropDownViewSpy(self))

class ViewParty(discord.ui.View):

    def is_a_player(self, user):
        player_filter = lambda x: x["user"]==user
        player = list(filter(player_filter,self.players))
        return True if player else False   


    def set_impostor(self, players):
        x = random.randint(0,len(players)-1)
        final_players = []
        for player in players:
            if x ==0:
                final_players.append({"user":player,"is_impostor":True})
            else:
                final_players.append({"user":player,"is_impostor":False})
            x-=1
        return final_players

    def set_location(self):
        locations = spyfall_db.get_locations()
        return random.choice(locations)

    def __init__(self, players, bot):
        super().__init__(timeout=None)
        self.players=self.set_impostor(players)
        self.location = self.set_location()
        self.vote = 0
        self.voteur = []
        self.bot = bot

    
    @discord.ui.button(label="voir le lieu")
    async def see_location(self,interaction:discord.Interaction, button:discord.Button):
        player_filter = lambda x: x["user"]==interaction.user
        player = list(filter(player_filter,self.players))
        if self.is_a_player(interaction.user) and player[0]["is_impostor"]:
            await interaction.response.send_message(f"vous êtes l'imposteur",ephemeral=True)
        elif not self.is_a_player(interaction.user):
            await interaction.response.send_message(f"vous n'êtes pas dans la partie",ephemeral=True)
        else:
            await interaction.response.send_message(f"le lieu est {self.location}",ephemeral=True)

    @discord.ui.button(label="voter")
    async def voter(self,interaction:discord.Interaction, button:discord.Button):
        if self.is_a_player(interaction.user) and interaction.user.id in self.voteur:
            self.vote-=1
            self.voteur.remove(interaction.user.id)
        elif not self.is_a_player(interaction.user):
            await interaction.response.send_message(f"vous n'êtes pas dans la partie",ephemeral=True)
        else:
            self.vote+=1
            self.voteur.append(interaction.user.id)
        if not self.vote>len(self.players)/2:
            await interaction.response.edit_message(content=f"la partie a commencé\nnombre de votes: {self.vote}")
        else:
            await interaction.response.edit_message(content="les votes sont lancées", view=VoteView(self))


    @discord.ui.button(label="réponse d'éspion")
    async def spy_answer(self,interaction:discord.Interaction, button:discord.Button):
        player_filter = lambda x: x["user"]==interaction.user
        player = list(filter(player_filter,self.players))
        if self.is_a_player(interaction.user) and player[0]["is_impostor"]:
            await interaction.response.edit_message(content=f"{interaction.user.name} l'imposteur pense avoir trouvé le lieu et donne sa réponse d'éspion",view=SpyView(self))
        elif not self.is_a_player(interaction.user):
            await interaction.response.send_message(f"vous n'êtes pas un joueur",ephemeral=True)
        else:
            await interaction.response.send_message(f"vous n'êtes pas imposteur",ephemeral=True)

class ViewLobby(discord.ui.View):
    def __init__(self, nb_players, bot):
        super().__init__(timeout=None)
        self.players=[]
        self.nb_players = nb_players
        self.bot = bot

    @discord.ui.button(label="rejoindre")
    async def rejoindre(self,interaction:discord.Interaction, button:discord.Button):
        if not interaction.user in self.players and not self.nb_players==len(self.players)+1:
            self.players.append(interaction.user)
            await interaction.response.edit_message(content=f"nombre de joueurs = {len(self.players)}")
        elif interaction.user in self.players:
            self.players.remove(interaction.user)
            await interaction.response.edit_message(content=f"nombre de joueurs = {len(self.players)}")
        elif self.nb_players==len(self.players)+1:
            self.players.append(interaction.user)
            first_player = self.players[random.randint(0,len(self.players)-1)]
            await interaction.response.edit_message(content=f"<@{first_player.id}> commence la partie et pose une question à un joueur de son choix\nnombre de votes: 0",view=ViewParty(self.players, self.bot))

class SpyFall(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot

    @app_commands.command(name="lobby_spy_fall",description="pour lancer la partie de spyfall")
    async def lobby_spy_fall(self, interaction:discord.Interaction, nombre_de_joueurs:int):
        await interaction.response.send_message(content = "nombre de joueurs = 0",view=ViewLobby(nombre_de_joueurs,self.bot))


async def setup(bot):
    await bot.add_cog(SpyFall(bot))