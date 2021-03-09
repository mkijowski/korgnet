import os
import subprocess
import random
import discord

from discord.ext import commands
from time import sleep, time
from datetime import datetime
from utils import *

def setup(bot):
    bot.add_cog(ValheimCommands(bot))

class ValheimCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    #discord frontend for valheim server poweron, only asgardians can run 
    @commands.command(name='gjallarhorn', help='Sound the horn, Korgdall will answer! \
        \b\bIf you fear the world of Korhalla has ended, fear not (but wait 2 minutes).')
    @commands.has_role('Asgardian')
    async def valheim_restart(self, ctx):
        #alert Matt
        await dm(member=ctx.guild.fetch_member(218952310053666816), content='Someone sounded the Gjallarhorn!')

        #power on server
        await ctx.send('The mighty beast Korgnarok has fled! The roots of Korggdrasil once again allow passage to Korghalla!')
        await ctx.send('All Korghallan\'s may check the fate of this world with `!gramr`.')
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh boot'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout

        await log(response)


    #discord frontend for valheim status checker
    @commands.command(name='gramr', help='Sigurd summons me to battle! Check the status of Korghalla.')
    @commands.has_role('Korghallan')
    async def check(self, ctx):
        await ctx.send('You pull the mighty Gramr from the trunk of the great Barnstokkr, \
            \b\b\bits ring pierces the myst.  If anyone is in Korghalla surely they will need your aid!')
    
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh check_status'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout
    
        await ctx.send(response)
        await log(response) 
