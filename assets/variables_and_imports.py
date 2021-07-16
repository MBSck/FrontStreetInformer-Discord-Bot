"""This file contains all variables and most of the imports needed for the bot"""

import os               # To access os functionality
import random           # Random numbers
import urllib.request   # For webscraping
import re               # For parsing
import string           # Contains various lists and dicts
import math             # Simply math
import discord          # API for the Discord-Bot
import asyncio          # Asynchronous case handling
import operator         # To parse operators from string
import time             # Time handling
import datetime         # Datetime handling
import configparser     # To parse config-files
import ast
# import lavalink         # For music bot connection functionality

from dotenv import load_dotenv      # To access '.env'-files
from discord.ext import commands    # Command handler from Discord-API
from bs4 import BeautifulSoup       # Webscraping

from assets.logger import Logger as Log # Event logger

################################################
# Global variables
################################################

# Install path
install_path = os.path.dirname(os.path.abspath(__file__))

# Operator dict
operator_dict = {"+": operator.add, "-": operator.sub, "/": operator.floordiv, "*": operator.mul}

# Kung fu list, global variable
kung_fu = ["https://www.youtube.com/watch?v=MCpiNJn0ZZM",
           "https://www.youtube.com/watch?v=bS5P_LAqiVg",
           "https://www.youtube.com/watch?v=-51L1VAJ9Ng"]
