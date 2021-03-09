import random
import discord
import os

from discord.ext import commands

def setup(bot):
    bot.add_cog(MemberCommands(bot))

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(ctx):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            'Are those gummy bears wrapped in a fruit roll-up?',
            'Cool. Cool cool cool cool cool cool cool, \nno doubt no doubt no doubt no doubt.'
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)


    #summon a Griffindork
    @commands.command(name='whoisit', help='Release the hound')
    async def bork(ctx):
        picture = './griff/' + random.choice(os.listdir('./griff/'))
        await ctx.send(file=discord.File(picture))
        await ctx.send('Bark! Bork!')
        