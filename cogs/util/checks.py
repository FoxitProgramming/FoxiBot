import discord
from discord.ext import commands

def is_enabled(option):
    def predicate(ctx):
        return option == "True"
    return commands.check(predicate)
