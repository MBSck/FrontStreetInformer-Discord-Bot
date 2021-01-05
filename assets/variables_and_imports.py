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

from assets.logger import Logger as Log

################################################
# Global variables
################################################

lobby = False
lobby_host = ""
lobby_members = {}
lobby_locked = False

# Operator dict

operator_dict = {"+": operator.add, "-": operator.sub, "/": operator.floordiv, "*": operator.mul}