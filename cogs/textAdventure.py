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
                return
            else:
                print(" > not in database")
                continue
        #embed = discord.Embed(colour=discord.Colour(0xdbc036))
        #embed.set_author(name="Player stats")
        #embed.add_field(name="Health", value=stats[0], inline=True)
        #embed.add_field(name="Armour", value=stats[1], inline=True)
        #embed.add_field(name="Agility", value=stats[2], inline=True)
        #embed.add_field(name="Attack", value=stats[3], inline=True)
        #embed.add_field(name="Magic", value=stats[4], inline=True)
        #await ctx.send(embed=embed)
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

        # part 2 the reckoning
        embedObject = discord.Embed(colour=discord.Colour(0xdbc036), description=f"How much armour do you have, {ctx.author}?")
        messageObject = await ctx.send(embed=embedObject)

        await messageObject.add_reaction("1️⃣")
        await messageObject.add_reaction("2️⃣")
        await messageObject.add_reaction("3️⃣")
        await messageObject.add_reaction("4️⃣")
        await messageObject.add_reaction("5️⃣")


        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            if reaction.emoji == '1️⃣':
                ctx.send("You selected one")
            elif reaction.emoji == '2️⃣':
                ctx.send("You selected two")
            elif reaction.emoji == '3️⃣':
                ctx.send("You selected three")
            elif reaction.emoji == '4️⃣':
                ctx.send("You selected four")
            elif reaction.emoji == '5️⃣':
                ctx.send("You selected five")

                # await self.PlayerProfile.callback(self=self, ctx=ctx, player=self.playerObject.UUID, edit=True, messageObject=messageObject)

    @commands.command()
    async def restart(self, ctx):
        pass

def setup(client):
    client.add_cog(TextAdventure(client))
