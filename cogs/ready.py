import discord
from discord.ext import commands

class Ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready cog online')
        

    # Commands
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hi!')

def setup(client):
    client.add_cog(Ready(client))