import re
import subprocess
import aiofiles
import discord

from datetime import datetime


#Make logging available
async def log(client, string, timestamp=True):
    # Log to stdout
    timestamp_string = ''
    if timestamp:
        timestamp_string = f'[{str(datetime.now())[:-7]}]'
    print(timestamp_string + ' ' + string)

    # Log to channel
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == 'bot-logs':
                await channel.send(string)

    # Log to file
    try:
        async with aiofiles.open('log', mode='r') as f:
            previous_logs = await f.readlines()
    except FileNotFoundError:
        previous_logs = []

    async with aiofiles.open('log', mode='w') as f:
        for line in previous_logs:
            await f.write(line.strip() + '\n')
        await f.write(timestamp_string + ' ' + string + '\n')


#easier direct messages
async def dm(member, content):
    channel = await member.create_dm()
    await channel.send(content)


#confirmation checker, did you really mean to restart?
async def confirmation(client, ctx, confirm_string='confirm'):
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


def git_update():
    command = 'git pull'
    result = subprocess.run(command.split(' '), capture_output=True, text=True)


def is_in_channel(channel_id):
    async def predicate(ctx):
        await log(client, f'Checking if {ctx.channel.id} is correct')
        return ctx.channel and ctx.channel.id == channel_id
    return commands.check(predicate)
