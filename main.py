import os
import random
import urllib.request
import re
import datetime
import string
import math
import discord
import asyncio
import youtube_dl
import lavalink
import operator
import time

from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup
from Logger import Logger as Log

# Importing background functionality

from customfunctions import *

# Importing the cogs

from dnd import DnD
from dndlobby import DnDLobby
from ciphers import Ciphers
from music import Music

# Global variables


lobby = False
lobby_host = ""
lobby_members = {}
lobby_locked = False

# Operator dict

operator_dict = {"+": operator.add, "-": operator.sub, "/": operator.floordiv, "*": operator.mul}



if __name__ == "__main__":
    
    # To ensure it can be shutdown if it causes any problems to the raspi

    time.sleep(15)

    # This gets the path of the file being executed

    path_str = os.path.dirname(os.path.realpath(__file__))

    # Load Token

    load_dotenv(os.path.join(path_str, "Token.env"))

    # Configure bot tokens

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("GUILD_TOKEN")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)
        
        
    # Calls the logger once to initialize it as well as sets the cogs up

    logger = Log()
    
    
    # Background tasks


    @bot.event
    async def game_presence():
        """Changes the status of the game, which the bot is playing"""
        await bot.wait_until_ready()

        games = ["DnD - Helper", "Listening to you", "Write '!help' for help", "Insulting you"]

        while not bot.is_closed():
            status = random.choice(games)

            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(status, type=3))
            await asyncio.sleep(15)


    bot.loop.create_task(game_presence())


    # Bot events (Bot is subclass of client and handles things a bit differently)


    @bot.event
    async def on_message(message):
        """Reacts to a user message to the bot"""
        ...


    @bot.event
    async def on_ready():
        """Sends a message to the Bots Host in order to verify its activation"""
        print(f"{bot.user.name} has connected to Discord!")


    """
    @bot.event
    async def on_member_update(ctx, after):
        chance = random.choice([1, 2, 3])
        if str(after.status) == "online":
            if chance == 2:
                with open(os.path.abspath("insults.txt"), "r") as f:
                    insult_list = f.read().split('|')
                insult = random.choice(insult_list)
                # logger.log(f"Insult given {ctx.nick} to . This is todays { insult")
                print(f"Insulted {ctx.display_name}")
                await ctx.send(insult)
    """


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")


    # Adds the cog to the register


    bot.add_cog(Ciphers())
    bot.add_cog(DnDLobby())
    bot.add_cog(DnD())

    # Runs the bot

    bot.run(TOKEN)
