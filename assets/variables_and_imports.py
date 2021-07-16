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
import configparser
import ast

from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup

from assets.logger import Logger as Log

################################################
# Global variables
################################################

# Install path
install_path = os.path.dirname(os.path.abspath(__file__))

# Operator dict
operator_dict = {"+": operator.add, "-": operator.sub, "/": operator.floordiv, "*": operator.mul}
