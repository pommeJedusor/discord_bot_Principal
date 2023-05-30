import discord
from discord.ext import commands
from cogs.one_piece_quiz import quiz

class quize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="One_Piece_quiz",description="permet de participer à un quiz")
    async def quiz_one_piece(self,interaction: discord.Interaction):
        global perso
        perso = await quiz.quiz_one_piece_request()
        await interaction.response.send_message(perso[0])
        perso = perso[1]

    @discord.app_commands.command(name="One_Piece_soluce",description="permet de répondre au quiz")
    async def soluce_one_piece(self,interaction: discord.Interaction,reponse:str):
        global perso    
        if await quiz.validator_response_one_piece(reponse,perso):
            await interaction.response.send_message(f"bonne réponse le perso était bel est bien {perso}")
            perso=""
        elif not perso:
            await interaction.response.send_message("pas de quiz en cours")
        else:
            await interaction.response.send_message(f"mauvaise réponse le perso était {perso}")
            perso=""

async def setup(bot):
    global perso
    perso = ""
    await bot.add_cog(quize(bot))