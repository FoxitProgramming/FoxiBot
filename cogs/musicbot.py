import discord
from discord.ext import commands

import logging
import configparser

from .util import checks

log = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

class MusicBot:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = "music", aliases = ["m"])
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Availiable commands are join, queue, skip, clearlist")

    @music.command(name = "join", aliases = ["j"])
    async def join(self, ctx):
        if not(ctx.author.voice):
            await ctx.send("You need to be in a voice channel for me to join!")
            return

        await ctx.author.voice.channel.connect()

def setup(bot):
    bot.add_cog(MusicBot(bot))
