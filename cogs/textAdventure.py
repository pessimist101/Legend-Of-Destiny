import discord
from discord.ext import commands
import json

class TextAdventure(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.statsConfig = json.load(open('stats.json', 'r'))

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready cog online')


    # Commands
    @commands.command()
    async def mystats(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Player stats")
        embed.add_field(name="Health", value=self.statsConfig['playerstats']['health'], inline=True)
        embed.add_field(name="Armour", value=self.statsConfig['playerstats']['armour'], inline=True)
        embed.add_field(name="Agility", value=self.statsConfig['playerstats']['agility'], inline=True)
        embed.add_field(name="Attack", value=self.statsConfig['playerstats']['attack'], inline=True)
        embed.add_field(name="Magic", value=self.statsConfig['playerstats']['magic'], inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(TextAdventure(client))
