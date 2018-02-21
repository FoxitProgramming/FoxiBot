import discord
from discord.ext import commands

import logging
import configparser

import asyncio

config = configparser.ConfigParser()
config.read("config.ini")

bot = commands.Bot(command_prefix = commands.when_mentioned_or(*["fb/","!"]), description = config.get("General", "bot_desc"))
log = logging.getLogger()

def startup():
    startLogging()

    token = config.get("General", "bot_token")
    cogs = config.items("Cogs")

    for cog in cogs:
        try:
            bot.load_extension(cog[0])
            log.info(f"Extension loaded: {cog[0]}")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logging.warning(f"Failed to load extension {cog[0]}.\n{exc}")

    if token == None:
        logging.critical("Token must be set in config to log in!")
        sys.exit(1)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(bot.start(token))
    except discord.LoginFailure:
        logging.critical("Invalid token")
        loop.run_until_complete(bot.logout())
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected. Quitting...")
        loop.run_until_complete(bot.logout())
    except Exception as exc:
        logging.critical("Fatal Exception", exc_info=exc)
        loop.run_until_complete(bot.logout())
    finally:
        log.info("Logged out and closed websocket.")

def startLogging():
    log.setLevel(logging.INFO)

    handler = logging.FileHandler(filename = "FoxiBot.log", encoding = "utf-8", mode="w")
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    log.addHandler(handler)

@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name="fb/help for help!"))
    log.info("Connected, FoxiBot online!")
    log.debug(f"Logged in as: {bot.user.name} with ID {bot.user.id}.")

if __name__ == "__main__":
    startup()
