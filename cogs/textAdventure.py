import discord
from discord.ext import commands
import json

class TextAdventure(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.statsConfig = json.load(open('stats.json', 'r'))
        self.config = json.load(open('config.json', 'r'))
        self.loadDescription = open('LoadDescription.txt').read()
        self.titleArt = open('Title.txt').read()


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready cog online')
        await self.client.get_channel(self.config['logChannel']).send(titleArt)
        await self.client.get_channel(self.config['logChannel']).send(loadDescription)
        print(self.titleart)


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

    # Commands
    @commands.command()
    async def play(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Player stats")
        embed.description(self.loadDescription)
        await ctx.send(embed=embed)
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Player stats")
        embed.description(self.titleart)
        await ctx.send(embed=embed)

    @commands.command()
    async def titleart(self, ctx):
        await ctx.send(self.titleArt)

def setup(client):
    client.add_cog(TextAdventure(client))
