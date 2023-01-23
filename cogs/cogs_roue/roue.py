import discord
from discord import app_commands
from discord.ext import commands

import random

class RoueDeLaGrosseMerde(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roue_de_la_grosse_merde",description="tourner la roue de la grosse merde")
    async def roue_de_la_grosse_merde(self,interaction:discord.Interaction):
        member_filtered = []
        for member in interaction.guild.members:
            if not member.bot and not member.id==309918440791998485:
                member_filtered.append(member)
        alea_number = random.randint(0,len(member_filtered)-1)
        await interaction.response.send_message(f"suspens...",ephemeral=True)
        await interaction.channel.send(f"<@{member_filtered[alea_number].id}>")
        await interaction.channel.send("https://cdn.discordapp.com/attachments/743439125914320986/1066684359165345932/Snapchat-59690717.jpg")


async def setup(bot):
    await bot.add_cog(RoueDeLaGrosseMerde(bot))