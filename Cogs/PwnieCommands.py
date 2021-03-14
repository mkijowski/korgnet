import os
import subprocess
import random
import discord

from discord.ext import commands
from time import sleep, time
from datetime import datetime
from utils import *


def setup(bot):
    bot.add_cog(PwnieCommands(bot))

class PwnieCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #discord frontend for pwnieland server poweron, only l337 can run 
    @commands.command(name='redpill', help='Free your mind.')
    @commands.has_role('l337')
    async def valheim_restart(self, ctx):
        #alert Matt and log command run
        await dm(member=await ctx.guild.fetch_member(218952310053666816), content=f'{ctx.author} took the red pill!')
        await log(self.bot, f'{ctx.author} took the red pill!')
        
        #power on server
        await ctx.send('My l337tle pwnies are getting ready to play!')
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh mlpboot'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout

        await log(self.bot, response)


    #discord frontend for pwnie status checker
    @commands.command(name='exit', help='I know kung fu!')
    @commands.has_role('l337')
    async def check(self, ctx):
        await ctx.send(f'{ctx.author} is calling all agents that need an exit!')
    
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh check_mlp_status'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout
    
        await ctx.send(response)
        await log(self.bot, response) 
