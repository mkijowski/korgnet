#!/opt/anaconda3/bin/python 
import os
import subprocess
import random
import discord
import sys
import aiofiles

from dotenv import load_dotenv
from discord.ext import commands
from time import sleep, time
from datetime import datetime
from utils import *

#get environment info
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
client = commands.Bot(command_prefix='!')
start_time = time()


@client.event
async def on_ready():
    # Startup status
    await client.change_presence(activity=discord.Game('Booting'), status=discord.Status.dnd)

    # Start logging
    await log(client, '\n\n\n\n\n###################################')
    await log(client, '# BOT STARTING FROM FULL SHUTDOWN #')
    await log(client, '###################################')
    
    # Startup status
    await client.change_presence(activity=discord.Game('Building servers'), status=discord.Status.idle)

    # Load all cogs
    await client.change_presence(activity=discord.Game(f'Loading Cogs'), status=discord.Status.idle)
    for file in os.listdir('Cogs'):
        if not file.startswith('__') and file.endswith('.py'):
            try:
                client.load_extension(f'Cogs.{file[:-3]}')
                await log(client, f'Loaded cog: {file[:-3]}')
            except commands.errors.NoEntryPointError:
                pass
    
    for guild in client.guilds:
        await log(client, '{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})')

    # Show the bot as online
    await client.change_presence(activity=discord.Game('Not quite asleep...'), status=discord.Status.online, afk=False)
    await log(client, 'Bot is online')

    
    # Print startup duration
    await log(client, '#########################')
    await log(client, '# BOT STARTUP COMPLETED #')
    await log(client, '#########################\n')
    await log(client, f'Started in {round(time() - start_time, 1)} seconds')


#welcome
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! My name is korgnet and I try my best to keep things tidy around here.\n'
        f'Eventually I will learn all sorts of tricks, but for now I just welcome people to my house!\n'
        f'If I learn a new trick I\'ll brag about it in my instructions channel.\n'
    )


#error events
@client.event
async def on_command_error(ctx, error):
    author, message = ctx.author, ctx.message.content

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required arguement')
        await ctx.send_help()
        await log(client, f'{author} attempted to run `{message}` but failed because they were missing a required argument')

    elif isinstance(error, commands.MissingRole):
        await ctx.send('Missing role')
        await log(client, f'{author} attempted to run `{message}` but failed because they were missing a required role')

    elif isinstance(error, commands.CommandNotFound):
        await log(client, f'{author} attempted to run `{message}` but failed because the command was not found')

    else:
        await ctx.send(f'Unexpected error: {error}')
        await log(client, f'{author} attempted to run `{message}` but failed because of an unexpected error: {error}')


if __name__ == '__main__':
    # Run bot from key given by command line argument
    client.run(TOKEN)
