import sqlite3
import discord
from discord.ext import commands
import json
import asyncio
import random

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
                await ctx.send("Sorry fam, I couldn't find you in the archives :(")
                continue
        embed = discord.Embed(colour=discord.Colour(0xdbc036))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=f"{ctx.author.name}'s Stats!")
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

        ### Time to pick people's stats! ###
        stats_list = ['armour', 'agility', 'attack', 'magic'] # What stats to include?
        number_dict = {'1️⃣': 'one', '2️⃣': 'two', '3️⃣': 'three', '4️⃣': 'four', '5️⃣': 'five'} # What is each emoji called?

        for stat in stats_list: # For every stat in the list, make a message asking how much people have...
            embedObject = discord.Embed(colour=discord.Colour(0xdbc036), description=f"How much {stat} do you have, <@{ctx.author.id}>?")
            messageObject = await ctx.send(embed=embedObject) # Send that message.

            # For every single emoji in the number_dict, add a reaction to the prior message.
            for emoji in number_dict:
                await messageObject.add_reaction(f"{emoji}")

            # Predicate/condition to be used later. Check the user is the original author and it's the same message.
            def reaction_info_check(reaction, user):
                return user == ctx.author and reaction.message.id == messageObject.id

            # Pause/wait for the user to react with an emoji that meets the above condition.
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)

            # Okay, the user has reacted with an emoji, let us find out which one!
            if reaction.emoji in number_dict:
                await ctx.send(f"You have selected {number_dict[reaction.emoji]} points in your {stat} stat.")

        # After user has picked their stats, run the $mystats command for them.
        await self.mystats.callback(self=self, ctx=ctx)
        await self.room_encounter.callback(self=self, ctx=ctx)


    # Commands
    @commands.command()
    async def room_encounter(self, ctx, rooms_visited=[]):
        print(f'Rooms visited = {rooms_visited}')
        if rooms_visited == []:
            print("Generating room list")
            room_list = list(range(1,21))
            current_room = random.choice(room_list)
        elif len(rooms_visited) > 0:
            print("Using old rooms list")
            room_list = rooms_visited
            if len(room_list) < 10:
                current_room = 'boss'
            else:
                current_room = random.choice(room_list)
        else:
            raise ValueError(f"Exceptional state, room encounter has invalid 'rooms visited': {rooms_visited}")
        print(f'Current room = {current_room}')
        print(f'Rooms list = {room_list}')


        room_description = open(f'rooms/room{current_room}.txt').read()
        embed = discord.Embed(colour=discord.Colour(0xdbc036), description=room_description, title=f"Room {current_room}")
        embed.set_author(name="Text Adventure!")
        messageObject = await ctx.send(embed=embed)

        ### Time to pick the next room! ###
        next_move = {'👈': random.choice(room_list), '👆': random.choice(room_list), '👉': random.choice(room_list)}

        for emoji in next_move:
            await messageObject.add_reaction(f"{emoji}")

        # Predicate/condition to be used later. Check the user is the original author and it's the same message.
        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id

        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)

        if reaction.emoji in next_move:
            await ctx.send(f"You have decided to walk to room {next_move[reaction.emoji]}...")

        room_list.remove(current_room)

        await self.room_encounter.callback(self=self, ctx=ctx, rooms_visited=room_list)

def setup(client):
    client.add_cog(TextAdventure(client))
