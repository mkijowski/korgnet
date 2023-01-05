import os
import subprocess
import random
import discord
import sys

from discord.ext import commands
from discord import app_commands

from utils.utils import *

valheim_channel = 818137307844050994

async def setup(bot):
    await bot.add_cog(ValheimCommands(bot))

#@app_commands.has_role('Asgardian')
class ValheimCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #discord frontend for valheim server poweron, only asgardians can run 
    @app_commands.command(name='gjallarhorn', description='Sound the horn, awaken the realm, Korgdall will answer!')
    async def gjallarhorn(self, interaction:discord.Interaction):
        #await dm(member=await ctx.guild.fetch_member(218952310053666816), content=f'{ctx.author} sounded the Gjallarhorn!')
        await log(self.bot, f'{interaction.user} sounded the Gjallarhorn!')
        
        #power on server
        await interaction.response.send_message('The mighty beast Korgnarok has fled! The roots of Korggdrasil once again allow passage to Korghalla! All Korghallan\'s may check the fate of this world with `!gramr`.')
        command = '/home/mkijowski/git/korgnet/scripts/gjallarhorn.sh boot'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout

        await log(self.bot, response)

    #@valheim_restart.error
    #async def gjallarhorn_error(self, ctx, error):
        #if isinstance(error, commands.CheckFailure):
            #korgheim = self.bot.get_channel(valheim_channel)
            #await ctx.send(f'This is not the rainbow bridge, you can only sound the `!gjallarhorn` in {korgheim.mention}!')
        #else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            #print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    #discord frontend for valheim status checker
    @app_commands.command(name='gramr', description='Sigurd summons me to battle! Check the status of Korghalla.')
    async def gramr(self, interaction:discord.Interaction):
        await interaction.response.send_message(f'{interaction.user} pulls the mighty Gramr from the trunk of the great Barnstokkr, its ring pierces the myst.  If anyone is in Korghalla surely they will need your aid!')
    
        command = '/home/mkijowski/git/korgnet/scripts/gjallarhorn.sh check_status'
        response = subprocess.run(command.split(' '), capture_output=True, text=True).stdout
    
        await interaction.response.send_message(response)
        await log(self.bot, response) 
    
    #@check_server.error
    #async def gramr_error(self, ctx, error):
        #if isinstance(error, commands.CheckFailure):
            #korgheim = self.bot.get_channel(valheim_channel)
            #await ctx.send(f'This is not the rainbow bridge, you can only wield the `!gramr` in {korgheim.mention}!')
        #else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            #print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
