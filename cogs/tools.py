import discord
from discord.ext import commands

import logging
import configparser

from .util import checks

log = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

class Tools:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "purge", aliases = ["clear","prg"])
    @checks.is_enabled(config.get("Tools","tl_purge_enabled"))
    async def purge(self, ctx, *, num: int):
        try:
            number = await ctx.message.channel.purge(limit = abs(num)+1)
            logging.info(f"Purged {len(number)} messages in {ctx.message.channel.name}.")
        except Exception as e:
            logging.info(f"Purge in {ctx.message.channel.name} unsuccessful.")

    @commands.command(name = "userinfo", aliases = ["ui","whois"])
    @checks.is_enabled(config.get("Tools","tl_userinfo_enabled"))
    async def userinfo(self, ctx, *, user = None):
        if user:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(name)
            if not user:
                user = ctx.guild.get_member(int(name))
            if not user:
                user = self.bot.get_user(int(name))
            if not user:
                await ctx.send(f"Could not find user: {name}")
        else:
            user = ctx.message.author

        message = discord.Embed(timestamp = ctx.message.created_at, colour = user.top_role.colour)
        message.add_field(name="User ID", value = user.id, inline = True)
        message.add_field(name='Nick', value=user.nick, inline=True)
        message.add_field(name='Highest Role', value=user.top_role, inline=True)
        message.add_field(name='Game', value=user.game, inline=False)
        message.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        message.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        message.set_author(name=user, icon_url= user.avatar_url)

        await ctx.send(embed = message)

    @commands.command(name = "serverinfo", aliases = ["si", "server"])
    @checks.is_enabled(config.get("Tools","tl_serverinfo_enabled"))
    async def serverinfo(self, ctx):
        server = ctx.guild

        if server == None:
            return

        roles = ", ".join(i.name for i in server.role_hierarchy)

        message = discord.Embed(timestamp = ctx.message.created_at, colour = 0x33c739)
        message.add_field(name="Server ID", value = server.id, inline=True)
        message.add_field(name="Owner", value = server.owner, inline = True)
        message.add_field(name="Members", value = len(server.members), inline = True)
        message.add_field(name="Region", value = server.region, inline = True)
        message.add_field(name="Roles", value = roles, inline = False)
        message.set_author(name = server.name, icon_url = server.icon_url)

        await ctx.send(embed = message)

def setup(bot):
    bot.add_cog(Tools(bot))
