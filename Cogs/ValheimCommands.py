import os
import subprocess
import random
import discord

from discord.ext import commands
from time import sleep, time
from datetime import datetime
from utils import *

valheim_channel = 818137307844050994

def setup(bot):
    bot.add_cog(ValheimCommands(bot))

class ValheimCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #discord frontend for valheim server poweron, only asgardians can run 
    @commands.command(name='gjallarhorn', help='Sound the horn, Korgdall will answer! If you fear the world of Korhalla has ended, fear not (but wait 2 minutes).')
    @commands.has_role('Asgardian')
    @is_in_channel(valheim_channel)
    async def valheim_restart(self, ctx):
        #alert Matt and log command run
        await dm(member=await ctx.guild.fetch_member(218952310053666816), content=f'{ctx.author} sounded the Gjallarhorn!')
        await log(self.bot, f'{ctx.author} sounded the Gjallarhorn!')
        
        #power on server
        await ctx.send('The mighty beast Korgnarok has fled! The roots of Korggdrasil once again allow passage to Korghalla!')
        await ctx.send('All Korghallan\'s may check the fate of this world with `!gramr`.')
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh boot'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout

        await log(self.bot, response)

    @valheim_restart.error
    async def gjallarhorn_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('This is not the rainbow bridge, you can only sound the `!gjallarhorn` in #korgheim !')


    #discord frontend for valheim status checker
    @commands.command(name='gramr', help='Sigurd summons me to battle! Check the status of Korghalla.')
    @commands.has_role('Korghallan')
    @is_in_channel(valheim_channel)
    async def check_server(self, ctx):
        await ctx.send(f'{ctx.author} pulls the mighty Gramr from the trunk of the great Barnstokkr, its ring pierces the myst.  If anyone is in Korghalla surely they will need your aid!')
    
        command = '/home/ubuntu/git/korgnet/scripts/gjallarhorn.sh check_status'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout
    
        await ctx.send(response)
        await log(self.bot, response) 
    
    @check_server.error
    async def gramr_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('This is not the rainbow bridge, you can only wield the `!gramr` in #korgheim !')
