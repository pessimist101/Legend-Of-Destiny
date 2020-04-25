import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)

client = commands.Bot(command_prefix = config['prefix'])

@client.event
async def on_ready():
    print('I\'m ready!')
    await client.get_channel(config['logChannel']).send('I\'m ready!')

@client.command()
async def load(ctx, extension):
    if ctx.author.id in config['authorisedUsers']:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('{} loaded'.format(extension))
        print('{} loaded'.format(extension))
    else:
        await ctx.send('You are not an authorised user. If you believe this is a mistake please contact <@377212919068229633>')
        return

@client.command()
async def unload(ctx, extension):
    if ctx.author.id in config['authorisedUsers']:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('{} unloaded'.format(extension))
        print('{} unloaded'.format(extension))
    else:
        await ctx.send('You are not an authorised user. If you believe this is a mistake please contact <@377212919068229633>')
        return

@unload.error
async def unloadError(ctx, error, extension):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('{} does not exist'.format(extension))

@client.command()
async def reload(ctx, extension):
    if ctx.author.id in config['authorisedUsers']:
        client.reload_extension(f'cogs.{extension}')
        await ctx.send('{} reloaded'.format(extension))
        print('{} reloaded'.format(extension))
    else:
        await ctx.send('You are not an authorised user. If you believe this is a mistake please contact <@377212919068229633>')
        return

@client.command()
async def snuggle_reload(ctx):
    if ctx.author.id in config['authorisedUsers']:
        os.system("tmux new-session -d -s shta; tmux send-keys -t shta 'python3 /home/shta/SHTAbot/bot.py'")

        await ctx.send('bye fam')
        exit()
    else:
        await ctx.send('You are not an authorised user. If you believe this is a mistake please contact <@377212919068229633>')
        return

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config['token'])
