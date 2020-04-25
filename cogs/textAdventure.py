import sqlite3
import discord
from discord.ext import commands
import json
import asyncio

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
        print('Text Adventure cog online')

    # Commands
    @commands.command()
    async def mystats(self, ctx):
        print(ctx.author.id)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("""select * from playerstats where discordID = {};""".format(ctx.author.id))
        results = cursor.fetchall()
        for player in results:
            print(f'checking {player[1]}')
            if player[1] == str(ctx.author.id):
                print(" > found in database")
                stats = player[2:]
                break
            else:
                print(" > not in database")
                continue
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
        embed = discord.Embed(colour=discord.Colour(0xdbc036), description=self.loadDescription)
        embed.set_author(name="Start game")
        embed.set_image(url='https://media.discordapp.net/attachments/703581212211544144/703655477174599741/unknown.png?width=1442&height=481')
        await ctx.send(embed=embed)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO playerstats (discordID,health,armour,agility,attack,magic)
                        VALUES ({},5,5,5,5,5);
        """.format(ctx.author.id))
        connection.commit()
        cursor.close()
        connection.close()

        stats_list = ['armour', 'agility', 'attack', 'magic']
        number_dict = {'1️⃣': 'one', '2️⃣': 'two', '3️⃣': 'three', '4️⃣': 'four', '5️⃣': 'five'}
        # part 2 the reckoning
        for stat in stats_list:
            embedObject = discord.Embed(colour=discord.Colour(0xdbc036), description=f"How much {stat} do you have, <@{ctx.author.id}>?")
            messageObject = await ctx.send(embed=embedObject)

            await messageObject.add_reaction("1️⃣")
            await messageObject.add_reaction("2️⃣")
            await messageObject.add_reaction("3️⃣")
            await messageObject.add_reaction("4️⃣")
            await messageObject.add_reaction("5️⃣")


            def reaction_info_check(reaction, user):
                return user == ctx.author and reaction.message.id == messageObject.id

            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
            for emoji in number_dict:
                if reaction.emoji == emoji:
                    await ctx.send(f"You have selected {number_dict[emoji]} points in your {stat} stat.")

            await self.mystats.callback(self=self, ctx=ctx)

    @commands.command()
    async def restart(self, ctx):
        pass

def setup(client):
    client.add_cog(TextAdventure(client))
