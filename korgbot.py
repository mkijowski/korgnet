# bot.py
import os
import random
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! My name is korgnet and I try my best to keep things tidy around here.\n'
        f'Eventually I will learn all sorts of tricks, but for now I just welcome people to my house!\n'
        f'If I learn a new trick I\'ll brag about it in my instructions channel.\n'
    )


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@client.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Are those gummy bears wrapped in a fruit roll-up?',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@client.command(name='whoisit', help='Release the hound')
async def bork(ctx):
    griff_pics = [
            'griff1.jpg', 
            'griff2.jpg',
            'griff3.jpg',
            'griff4.jpg',
            'griff5.jpg',
            'griff6.jpg',
            'griff7.jpg',
            'griff8.jpg',
            'griff9.jpg',
            'griff10.jpg',
            'griff11.jpg',
            ]
    picture = './griff/' + random.choice(griff_pics)
    await ctx.send(file=discord.File(picture))
    await ctx.send('Bark! Bork!')

client.run(TOKEN)
