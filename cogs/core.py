import discord
from discord.ext import commands

import logging
import configparser

log = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

class Core():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    @commands.is_owner()
    async def stop(self, ctx):
        await self.bot.logout()

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logging.critical(f"ERROR: {exc}")
            await ctx.send(f"{cog} did not load!")
        else:
            logging.info(f"Reloaded: {cog}")
            await ctx.send(f"{cog} successfully loaded!")

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logging.critical(f"ERROR: {exc}")
            await ctx.send(f"{cog} did not unload!")
        else:
            logging.info(f"Reloaded: {cog}")
            await ctx.send(f"{cog} successfully unloaded!")

    @commands.command(name = "reload", hidden = True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logging.critical(f"ERROR: {exc}")
            await ctx.send(f"{cog} did not reload!")
        else:
            logging.info(f"Reloaded: {cog}")
            await ctx.send(f"{cog} successfully reloaded!")

    @commands.command(name = "reloadall", hidden = True)
    @commands.is_owner()
    async def cog_reloadall(self, ctx):
        cogs = config.items("Cogs")

        for cog in cogs:
            if cog[1] == "True":
                try:
                    self.bot.unload_extension(cog[0])
                    self.bot.load_extension(cog[0])
                except Exception as e:
                    exc = '{}: {}'.format(type(e).__name__, e)
                    logging.critical(f"ERROR: {exc}")
                    await ctx.send(f"{cog[0]} did not reload!")
                else:
                    logging.info(f"Reloaded: {cog[0]}")
                    await ctx.send(f"{cog[0]} successfully reloaded!")

def setup(bot):
    bot.add_cog(Core(bot))
