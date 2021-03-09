import os
import subprocess
import random
import discord
import sys


from discord.ext import commands
from time import sleep, time
from datetime import datetime
from utils import *

def setup(bot):
    bot.add_cog(ServerManagement(bot))

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # server restart command, also runs a git pull so that it will update the server before restarting.
    @commands.command(name='restart', help='Git pulls any new code and restarts discord bot.')
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        if await confirmation(self.bot, ctx):
            await ctx.send('Restarting...')
            command = 'git pull'
            result = subprocess.run(command.split(' '), capture_output=True, text=True)
            os.execv(sys.argv[0], sys.argv)
