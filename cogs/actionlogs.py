import discord
from discord.ext import commands

import logging
import configparser
import datetime

from .util import checks

log = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

class ActionLogs:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, ctx):

        if config.get("ActionLogs","al_join_messages_enabled") == "False":
            logging.info("Join messages disabled")
            return

        room_id = config.get("ActionLogs", "al_join_room")
        room = discord.utils.get(ctx.guild.text_channels, id = int(room_id))

        if room == None:
            logging.warning("Join room specified in config doesn't exist.")
            return

        message = discord.Embed(description = f"{ctx.mention} welcome to the server!", colour=0xE55F25)
        message.set_footer(text = "Have a nice stay!")
        message.set_author(name = "Member joined!", icon_url = ctx.avatar_url)
        message.timestamp = datetime.datetime.now()

        await room.send(embed = message)

    async def on_member_remove(self, ctx):

        if config.get("ActionLogs","al_leave_messages_enabled") == "False":
            logging.info("Leave messages disabled")
            return

        room_id = config.get("ActionLogs", "al_leave_room")
        room = discord.utils.get(ctx.guild.text_channels, id = int(room_id))

        if room == None:
            logging.warning("Leave room specified in config doesn't exist.")
            return

        message = discord.Embed(description = f"{ctx.mention} left the server...", colour=0x3ba3e6)
        message.set_footer(text = "Bye bye!")
        message.set_author(name = "Member left!", icon_url = ctx.avatar_url)
        message.timestamp = datetime.datetime.now()

        await room.send(embed = message)

    async def on_message_edit(self, before, after):

        if config.get("ActionLogs","al_edit_message_enabled") == "False":
            logging.info("Edit messages disabled")
            return

        room_id = config.get("ActionLogs", "al_edit_room")
        room = discord.utils.get(after.guild.text_channels, id = int(room_id))

        if room == None:
            logging.warning("Edit room specified in config doesn't exist.")
            return

        if before.content == after.content:
            return

        message = discord.Embed(description = f"**Message Edited in {after.channel.mention}.**", colour=0x9233d4)
        message.set_footer(text = f"ID: {after.id}")
        message.timestamp = datetime.datetime.now()
        message.set_author(name = after.author.display_name, icon_url = after.author.avatar_url)
        message.add_field(name = "Before", value = before.content, inline = False)
        message.add_field(name = "After", value = after.content, inline = False)

        await room.send(embed=message)

def setup(bot):
    bot.add_cog(ActionLogs(bot))
