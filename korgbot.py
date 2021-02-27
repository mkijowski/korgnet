#!/opt/anaconda3/bin/python 
import os
import subprocess
import random
import discord
import sys

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

##### ================== #####
##### MEMEBER MANAGEMENT #####
##### ================== #####

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

##### ================== #####
##### VALHEIM MANAGEMENT #####
##### ================== #####

@client.command(name='gjallarhorn', help='Sound the horn, Korgdall will answer! If you fear the world of Korhalla has ended, fear not (but wait 2 minutes).')
@commands.has_role('Asgardian')
async def valheim_restart(ctx):
    #alert Matt
    odin = client.get_user(218952310053666816)
    await odin.send('Someone sounded the Gjallarhorn!')

    command = '/home/ubuntu/korgnarok.sh'
    await ctx.send('The mighty beast Korgnarok has been spotted! Backing up the world of Korghalla. Odin will return the world to order in 2 minutes.')
    await ctx.send('All Korghallan\'s may check the fate of this world with `!gramr`.')
    result = subprocess.run(command.split(' '), capture_output=True, text=True)
    response=korghalla_status()
    await ctx.send(response)
    if 'Korgnarok' in response:
        await odin.send('Korgnarok has won, your script has failed!')
    else:
        await odin.send('Korghalla has risen from the ashes!')

@client.command(name='gramr', help='Sigurd summons me to battle! Check the status of Korghalla.')
@commands.has_role('Korghallan')
async def check(ctx):
    response=korghalla_status()
    await ctx.send(response)
    


def korghalla_status():
    command = 'sudo systemctl status valheimserver.service'
    result = subprocess.run(command.split(' '), capture_output=True, text=True)
    if 'Active' in result.stdout:
        return 'Hrungnir hungers warrior, go out and slay that troll!'
    else:
        return 'Korghalla has fallen, Korgnarok is upon us!'


##### ================== #####
##### SERVER MANAGEMENT  #####
##### ================== #####


@client.command(name='restart', help='Git pulls any new code and restarts discord bot.')
@commands.has_role('Asgardian')
async def restart(ctx):
    if await confirmation(ctx):
        await ctx.send('Restarting...')
        command = 'git pull'
        result = subprocess.run(command.split(' '), capture_output=True, text=True)
        os.execv(sys.argv[0], sys.argv)

async def confirmation(ctx, confirm_string='confirm'):
    # Ask for confirmation
    await ctx.send(f'Enter `{confirm_string}` to confirm action')

    # Wait for confirmation
    msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    if msg.content == confirm_string:
        await ctx.send(f'Action confirmed, executing')
        return True
    else:
        await ctx.send(f'Confirmation failed, terminating execution')
        return False


client.run(TOKEN)

