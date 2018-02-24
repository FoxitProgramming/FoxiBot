import discord
from discord.ext import commands

import logging
import configparser
import asyncio

from .util import checks

log = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

class TempRooms:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="createroom", aliases=["room","r"])
    async def create_room(self, ctx, name = None, num = None):
        if not(ctx.author.voice):
            log.info(f"{ctx.author} tried creating a room without being in a voice channel.")
            await ctx.send("You must be in a voice channel to use that command!")
            return

        if not(name):
            name = f"{ctx.author.display_name}'s Room"

        if not(num):
            num = 0
        try:
            num = abs(int(num))
            if num > 15:
                num = 15
        except:
            ctx.send("No valid number provided")
            return

        category = discord.utils.get(ctx.guild.categories, id = int(config.get("TempRooms","tr_create_category")))

        room = await ctx.guild.create_voice_channel(name = name, category = category)
        await ctx.author.move_to(room)
        asyncio.sleep(1)
        await room.edit(user_limit = num)
        await room.set_permissions(ctx.author, create_instant_invite = True)
        await ctx.send(f"Created room {name}, with space for {num} people.")
        log.info(f"{ctx.author} created room {name} with space for {num} people.")

    @commands.command(name = "cleanrooms", aliases = ["cr"])
    async def clean_rooms(self, ctx):
        category = discord.utils.get(ctx.guild.categories, id = int(config.get("TempRooms","tr_create_category")))
        for channel in category.channels:
            if len(channel.members) > 0:
                return

            await channel.delete()
            log.info(f"{before.channel} deleted.")

    @commands.command(name = "invite", aliases = ["i"])
    async def invite(self, ctx, users = None):
        if not(ctx.author.voice):
            await ctx.send("You need to be in a voice channel to do that")
            return

        if not(ctx.author.voice.channel.category.id == int(config.get("TempRooms","tr_create_category"))):
            await ctx.send("You need to be in a custom room to do that!")
            return

        try:
            users = ctx.message.mentions
        except:
            await ctx.send("You need to tag users to invite!")
            return

        userstring = ", ".join(user.name for user in users)

        for user in users:
            await ctx.author.voice.channel.set_permissions(user, connect = True)

        await ctx.send(f"{userstring} now has access to join {ctx.author.voice.channel}")

    async def on_voice_state_update(self, member, before, after):
        if not(before.channel):
            return

        if not(before.channel.category.id == int(config.get("TempRooms","tr_create_category"))):
            return

        if len(before.channel.members) > 0:
            return

        await before.channel.delete()
        log.info(f"{before.channel} deleted.")

def setup(bot):
    bot.add_cog(TempRooms(bot))
