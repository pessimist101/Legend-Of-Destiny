import sqlite3
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
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT playerstats.discordID;""")
        results = cursor.fetchall()
        for player in results:
            if player[1] == ctx.author.id:
                print(" > found in database")
                stats = player[2:]
                return
            else:
                print(" > not in database")
                return False
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Player stats")
        embed.add_field(name="Health", value=stats[0], inline=True)
        embed.add_field(name="Armour", value=stats[1], inline=True)
        embed.add_field(name="Agility", value=stats[2], inline=True)
        embed.add_field(name="Attack", value=stats[3], inline=True)
        embed.add_field(name="Magic", value=stats[4], inline=True)
        await ctx.send(embed=embed)
        cursor.close()
        connection.close()


    # Commands
    @commands.command()
    async def play(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Player stats")
        embed.description(self.loadDescription)
        await ctx.send(embed=embed)
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_author(name="Start game")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/703581212211544144/703655477174599741/unknown.png?width=1442&height=481')
        embed.description()
        await ctx.send(embed=embed)

    @commands.command()
    async def titleart(self, ctx):
        await ctx.send(self.titleArt)

def setup(client):
    client.add_cog(TextAdventure(client))
