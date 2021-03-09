import os
import subprocess
import random
import discord

from discord.ext import commands
from time import sleep, time
from datetime import datetime

def setup(bot):
    bot.add_cog(ServerManagement(bot))

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # server restart command, also runs a git pull so that it will update the server before restarting.
    @commands.command(name='restart', help='Git pulls any new code and restarts discord bot.')
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        if await confirmation(ctx):
            await ctx.send('Restarting...')
            command = 'git pull'
            result = subprocess.run(command.split(' '), capture_output=True, text=True)
            os.execv(sys.argv[0], sys.argv)


    #confirmation checker, did you really mean to restart?
    async def confirmation(self, ctx, confirm_string='confirm'):
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
