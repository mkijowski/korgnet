#!/opt/anaconda3/bin/python 
import os
import subprocess
import random
import discord
import sys

from dotenv import load_dotenv
from discord.ext import commands

#get environment info
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

#summon a Griffindork
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

#discord frontend for valheim server reboot.  This backs up the world and restarts the service.
#The korgnarok.sh script has two, one minute hardcoded wait timers to be sure the service stops 
#and starts.  Checks the status of the server at the end and if down DM's Odin(kijowski) 
@client.command(name='gjallarhorn', help='Sound the horn, Korgdall will answer! If you fear the world of Korhalla has ended, fear not (but wait 2 minutes).')
@commands.has_role('Asgardian')
async def valheim_restart(ctx):
    #alert Matt
    odin = client.get_user(218952310053666816)
    channel = await odin.create_dm()
    await channel.send('Someone sounded the Gjallarhorn!')

    command = '/home/ubuntu/git/korgnet/gjallarhorn.sh boot'
    await ctx.send('The mighty beast Korgnarok has fled! The roots of Korggdrasil once again allow passage to Korghalla!')
    #await ctx.send('All Korghallan\'s may check the fate of this world with `!gramr`.')
    result = subprocess.run(command.split(' '), capture_output=True, text=True)

#discord frontend for valheim status checker
@client.command(name='gramr', help='Sigurd summons me to battle! Check the status of Korghalla.')
@commands.has_role('Korghallan')
async def check(ctx):
    command = '/home/ubuntu/git/korgnet/gjallarhorn.sh check_status'
    await ctx.send('You pull the mighty Gramr from the trunk of the great Barnstokkr, its ring pierces the myst.  If anyone is in Korghalla surely they will need your aid!')
    odin = client.get_user(218952310053666816)
    channel = await odin.create_dm()
    await channel.send('Someone wielded Gramr!')
    result = subprocess.run(command.split(' '), capture_output=True, text=True)
    response=result.stdout
    await ctx.send(response)
    

##### ================== #####
##### SERVER MANAGEMENT  #####
##### ================== #####


# server restart command, also runs a git pull so that it will update the server before restarting.
@client.command(name='restart', help='Git pulls any new code and restarts discord bot.')
@commands.has_permissions(administrator=True)
async def restart(ctx):
    if await confirmation(ctx):
        await ctx.send('Restarting...')
        command = 'git pull'
        result = subprocess.run(command.split(' '), capture_output=True, text=True)
        os.execv(sys.argv[0], sys.argv)

#confirmation checker, did you really mean to restart?
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

