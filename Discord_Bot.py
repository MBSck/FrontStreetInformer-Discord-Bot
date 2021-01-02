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

'''
if not discord.opus.is_loaded():
    """The 'opus' library needs to be loaded in order to do voice stuffs on Discord.
	If this part of the program doesn't run properly,
	make sure you have 'opus.dll' in Windows or 'libopus' installed if on Linux.
	If still you get issues here, replace 'opus' with the directory location of 'opus' in the line below."""
    discord.opus.load_opus('opus')
'''

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

# Global variables


lobby = False
lobby_host = ""
lobby_members = {}
lobby_locked = False

# Operator dict

operator_dict = {"+": operator.add, "-": operator.sub, "/": operator.floordiv, "*": operator.mul}


# Calls the logger once to initialize it as well as sets the cogs up
logger = Log()


# Gets the Nicknames of people


def get_user_nickname(user_id):
    sammy = ["sammy", "fatzkes"]
    julian = ["julian"]
    max = ["max"]
    niclas = ["niclas", "nici"]
    thorsten = ["thorsten", "0013"]

    user_id_dict = {}


# Initalizes time for timed functions


def get_time():
    actual = datetime.datetime.now()
    actual_time = f"{actual.hour}:{actual.minute}:{actual.second}"
    actual_date_time = f"{actual.day}.{actual.month}.{actual.year} at {actual_time}"
    return actual_time, actual_date_time


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


# Bot commands

@bot.command(name="unsub", help="This removes you from any commands that the bot targets you with!"
                                "Can also be a specifiy command with !unsub <command_name>")
async def unsub():
    pass


@bot.command(name="sub", help="This makes the bot torment you again. Can be a specifiy command in form of"
                              "!sub <command_name>")
async def sub():
    pass


"""
@bot.command(name="question", help="Ask the bot questions")
async def question(ctx, *args):
    question_str = ''
    for i in args:
        question_str += ' ' + i

    question_str = question_str[1:]

    if "Max" and "dumm" in question_str:
        await ctx.send("Yes he is!")
"""


@bot.command(name="add.insult", help="This adds an insult for the welcome message")
async def insult_add(ctx, *args):
    insult_str = ''
    for i in args:
        insult_str += ' ' + i

    insult_str = insult_str[1:]
    try:
        with open(os.path.join("insults.txt"), "a") as f:
            f.write(insult_str + '|\n')
            f.close()

        await ctx.send(f"Insult was added, thank you!\n"
                       f"Insult reads:\n '{insult_str}'")

    except ValueError:
        await ctx.send("Please do not use single quotation marks")


@bot.command(name="suggest", help="This makes a suggestion for new bot functionality")
async def suggest(ctx, *args):
    suggestion = ""
    for arg in args:
        if ((arg == ",") or (arg == ".") or (arg == ";") or (arg == "!") or
                (arg == "?") or (arg == ":") or (arg == "-") or (arg == "_") or
                (arg == "(") or (arg == ")") or (arg == "[") or (arg == "]") or
                (arg == "{") or (arg == "}") or (arg == "/") or (arg == "%") or
                (arg == "§") or (arg == "&") or (arg == "'")):
            suggestion += arg
        else:
            suggestion += " " + arg
    suggestion = "'" + suggestion[1:] + "'"
    with open(os.path.join("suggestions.txt"), "a") as f:
        f.write(f"\nThis suggestions has been sent in on {get_time()[1]} by {ctx.message.author} and reads:\n"
                f"{suggestion}\n")
        f.close()
    await ctx.send(f"Suggestion has been recieved at {get_time()[0]}, thank you!")


@bot.command(name="bug", help="This reports bugs so they can be fixed")
async def bug(ctx, *args):
    bugs = ""
    for arg in args:
        if ((arg == ",") or (arg == ".") or (arg == ";") or (arg == "!") or
                (arg == "?") or (arg == ":") or (arg == "-") or (arg == "_") or
                (arg == "(") or (arg == ")") or (arg == "[") or (arg == "]") or
                (arg == "{") or (arg == "}") or (arg == "/") or (arg == "%") or
                (arg == "§") or (arg == "&") or (arg == "'")):
            bugs += arg
        else:
            bugs += " " + arg
    bugs = "'" + bugs[1:] + "'"
    # For Linux
    with open(os.path.join("bug_log.txt"), "a") as f:
        f.write(f"\nThis bug report has been sent in on {get_time()[1]} by {ctx.message.author} and reads:\n"
                f"{bugs}\n")
        f.close()
    await ctx.send(f"The bug report has been recieved at {get_time()[0]}, thank you!")


@bot.command(name="kungfu", help="Nifty stuff about kung fu")
async def kung_fu_write(ctx):
    kung_fu = ["https://www.youtube.com/watch?v=MCpiNJn0ZZM",
               "https://www.youtube.com/watch?v=bS5P_LAqiVg",
               "https://www.youtube.com/watch?v=-51L1VAJ9Ng"]
    response = random.choice(kung_fu)
    await ctx.send(f"As requested something about Kung fu!\n {response}")


@bot.command(name="j.search", help="Looks up Japanese words and Kanji. Uses Jisho as Basis")
async def j_search(ctx, search_term):
    page = urllib.request.urlopen("https://jisho.org/")
    print(page.read())


@bot.command(name="search.airdates", help="Looks for your series latest airdates")
async def search_air_dates(ctx, series_name):
    page = urllib.request.urlopen("http://www.epguides.com/menu/current.shtml")
    soup = BeautifulSoup(page)
    links = []
    for link in soup.findAll("a", attrs={"href": re.compile("^https://")}):
        links.append(link.get("href"))

    print(links)

    for string in links:
        if series_name in string:
            link_search = string

    print(link_search)

    searched_page = urllib.request.urlopen(link_search)
    soup_deeper = BeautifulSoup(searched_page)
    episode_number = soup_deeper.find("td", attrs={"class": "epinfo right"})

    await ctx.send(episode_number)


# Cogs for the sorting of the help information

# DnD - Lobby


class DnDLobby(commands.Cog):
    """DnD commands that enable online gaming with the discord bot"""

    @commands.command(name="lobby.start", aliases=["l.s"])
    async def lobby_start(self, ctx):
        """Starts a DnD lobby"""
        global lobby, lobby_host
        if not lobby:
            lobby_host = ctx.author.name
            lobby_members[ctx.message.author.name] = ctx.message.author.id
            lobby = True

            await ctx.send("> Lobby has been created!")

        else:
            await ctx.send("> There is already another lobby!")

    @commands.command(name="lobby.close", aliases=["l.c"])
    async def lobby_close(self, ctx):
        """Closes a DnD lobby"""
        global lobby, lobby_host, lobby_members
        if lobby:
            if ctx.author.name == lobby_host:
                lobby = False
                lobby_host = ""
                lobby_members.clear()

                await ctx.send("> Lobby has been closed!")

            else:
                await ctx.send("> You do not have permission to do that!")

        else:
            await ctx.send("> There is no lobby active right now!")

    @commands.command(name="lobby.status", aliases=["l.st"])
    async def lobby_status(self, ctx):
        """Checks the status of the lobby"""
        if lobby:
            await ctx.send(f"> There is a lobby online with {str(len(lobby_members))} members.")
        else:
            await ctx.send("> No lobby exists.")

    @commands.command("lobby.lock", aliases=["l.lo"])
    async def lobby_locked(self, ctx):
        """Command for the host locks the lobby"""
        global lobby_locked
        if lobby and ctx.author.name == lobby_host:
            lobby_locked = True
            await ctx.send("> Lobby has been **locked**!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.unlock", aliases=["l.u"])
    async def lobby_unlocked(self, ctx):
        """Command for the host to unlock the lobby"""
        global lobby_locked
        if lobby and ctx.author.name == lobby_host:
            lobby_locked = False
            await ctx.send("> Lobby has been **unlocked**!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.join", aliases=["l.j"])
    async def join_lobby(self, ctx):
        """Joins a DnD lobby"""
        global lobby_members

        if lobby and not lobby_locked:
            if ctx.message.author.name in lobby_members:
                await ctx.send("> You have already joined the lobby.")

            else:
                lobby_members[ctx.message.author.name] = ctx.message.author.id
                message = ""

                for i in lobby_members:
                    message += i + ", "

                message = message[:-2]

                for i, o in lobby_members.items():
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"> {ctx.author.name} has joined the lobby.")

                await ctx.send(f">>> You have joined the lobby!\nWelcome! Members in the lobby:\n{message}")

        else:
            await ctx.send("> There is no lobby to join or it has been locked!")

    @commands.command(name="lobby.leave", aliases=["l.le"])
    async def lobby_leave(self, ctx):
        """Leaves a DnD lobby"""
        global lobby, lobby_members, lobby_host

        if lobby:
            del lobby_members[ctx.author.name]

            for i, o in lobby_members.items():
                user = await ctx.bot.fetch_user(o)

                if ctx.author.name == lobby_host:
                    lobby_host = ""
                    lobby_host = random.choice(lobby_members)
                    await self.lobby_host_change(ctx, lobby_host)

                await user.send(f"> {ctx.author.name} has **left** the lobby.")

            if len(lobby_members) == 0:
                lobby = False

            await ctx.send("> You have left the lobby!")

        else:
            await ctx.send("> You are in no lobby!")

    @commands.command(name="lobby.kick", aliases=["l.k"])
    async def lobby_kick(self, ctx, name):
        """Command for the host locks kicks a member of the lobby"""
        global lobby_members

        if lobby and ctx.author.name == lobby_host:
            if name in lobby_members:
                if name == lobby_host:
                    if len(lobby_members) == 1:
                        await self.lobby_close(ctx)

                    else:
                        await self.lobby_host_change(ctx, random.choice(lobby_members))

            else:
                for i, o in lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == name:
                        del lobby_members[i]
                        await user.send("> You have been **kicked** from the lobby!")

                    else:
                        await user.send(f"> {name} has been **kicked** from the lobby!")

                else:
                    await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.host", aliases=["l.h"])
    async def lobby_host_change(self, ctx, name):
        """Command for the host to change host to another member of the lobby"""
        global lobby_host

        if lobby and ctx.author.name == lobby_host:
            if name in lobby_members:
                lobby_host = name
                for i, o in lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == lobby_host:
                        await user.send("> You are ***already*** the host of the lobby!")

                    elif (i == name) and (name != lobby_host):
                        await user.send("> You have been made **host** of the lobby!")

                    else:
                        await user.send(f"> {name} has been made into the **host** of the lobby!")

            else:
                await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.members", aliases=["l.m"])
    async def lobby_members(self, ctx):
        """Displays the members of the lobby"""
        if lobby:
            if ctx.message.author.name in lobby_members:
                message = ""

                for i in lobby_members:
                    if i == lobby_host:
                        message += "__Host__: " + i + ", "
                    else:
                        message += i + ", "

                message = message[:-2]

                await ctx.send(f">>> Members in the lobby:\n{message}")
        else:
            await ctx.send("> There is no lobby or it has been locked!")


class DnD(commands.Cog):
    """Gameplay functions for DnD"""

    async def get_dice_roll(self, ctx, dice: str = "1d20", *args: str):
        """Gets the dice rolls after user output and calculates its sum"""
        try:
            arg_list = [dice]
            arg_list.extend(args)

            dice_operator_list = []
            multiple_dice_list = []

            for i in arg_list:
                dice_operator_list.extend(re.split('([-+/*])', i))

            for i in dice_operator_list.copy():
                if i == "":
                    dice_operator_list.remove(i)

            second_line = "```"

            if len(dice_operator_list) == 1:

                number_of_dice, die_range = map(int, dice.lower().split('d'))

                result_dice = [str(random.randint(1, die_range)) for _ in range(number_of_dice)]
                second_line += ' + '.join(result_dice)

                if number_of_dice > 1:
                    sum_total = 0
                    for i in result_dice:
                        sum_total += int(i)

                    second_line += f" = {sum_total}"

                multiple_dice_list.append(dice_operator_list[0].lower())

            else:
                sum_total = 0
                if len(dice_operator_list) > 3:
                    second_line += '{'

                for i, o in enumerate(dice_operator_list):
                    if len(dice_operator_list) > 1:
                        if 'd' in o.lower():
                            try:
                                if (dice_operator_list[i+1] != '+') and (dice_operator_list[i+1] != '-') and \
                                        (dice_operator_list[i+1] != '/') and (dice_operator_list[i+1] != '*'):
                                    dice_operator_list.insert(i+1, '+')
                                    dice_operator_list.insert(i+2, '0')

                            except IndexError:
                                dice_operator_list.insert(i+1, '+')
                                dice_operator_list.insert(i+2, '0')

                            if dice_operator_list[i+2] == '0':
                                multiple_dice_list.append(dice_operator_list[i].lower())
                            else:
                                multiple_dice_list.append(f"{dice_operator_list[i].lower()}"
                                                          f"{dice_operator_list[i+1]}{dice_operator_list[i+2]}")

                        if (i == 0) and ((o == '+') or (o == '-') or (o == '/') or (o == '*')):
                            dice_operator_list.insert(0, '1d20')

                            multiple_dice_list.append(f"1d20"
                                                      f"{dice_operator_list[1]}{dice_operator_list[2]}")
                            continue

                    if (o == '+') or (o == '-') or (o == '/') or (o == '*'):
                        try:
                            if len(dice_operator_list) > 3:
                                second_line += "["

                            operator_func = operator_dict[dice_operator_list[i]]

                            number_of_dice_part, die_range_part = map(int, dice_operator_list[i-1].lower().split('d'))

                            result_dice = [str(random.randint(1, die_range_part)) for _ in range(number_of_dice_part)]

                            second_line_part = "(" + ' + '.join(result_dice)

                            sum_total_part = 0
                            for j in result_dice:
                                sum_total_part += int(j)

                            sum_total_part = operator_func(sum_total_part, int(dice_operator_list[i+1]))
                            sum_total += sum_total_part

                            if (dice_operator_list[i] != '*') and (dice_operator_list[i+1] == '0'):
                                second_line_part += f") = {sum_total_part}"
                            else:
                                second_line_part += f") {dice_operator_list[i]} " \
                                                    f"{dice_operator_list[i+1]} = {sum_total_part}"

                            try:
                                if len(dice_operator_list) > 3:
                                    second_line += second_line_part + "] + "
                                else:
                                    second_line += second_line_part
                            except Exception:
                                pass

                        except IndexError:
                            return

                if len(dice_operator_list) > 3:
                    second_line = second_line[:-3] + '}' + f" = {sum_total}"

            second_line += "```"
            first_line = ', '.join(multiple_dice_list) + ":\n"
            result = first_line + second_line

            return result

        except Exception:
            await ctx.send("> Input of the wrong format!")
            return

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, throw_command: str = "1d20", *args):
        """Shorthand '!r'.Rolls dice. Defaults to d20. Input '!roll/!r [# dice]d[# sides] + [modifiers]'\n "
        "Allowed operators for modifiers are + - / *. Can also row multiple dice at the same time. Of the format
        !roll/!r [# dice]d[# sides] [+-/*] [modifiers] [# dice]d[# sides] [+-/*] [modifiers] ..."""

        roll_output = await self.get_dice_roll(ctx, throw_command, *args)

        if roll_output is None:
            return

        # Broadcasts the results to the members of the lobby and does not if no lobby exists
        if lobby and (ctx.author.name in lobby_members) and (ctx.author.name != lobby_host):
            for i, o in lobby_members.items():
                user = await ctx.bot.fetch_user(o)
                await user.send(f"{ctx.author.name} rolled {roll_output}")
        else:
            await ctx.send(f"You have rolled {roll_output}")

    @commands.command(name="gmroll", aliases=["gr"], help="Shorthand '!gr'.Rolls a die and sends result directly "
                                                          "to Game Master and also you."
                                                          " Also defaults to 1d20. Great for hidden/discreet checks")
    async def gm_roll(self, ctx, throw_command: str = "1d20", *args):
        if lobby:
            roll_output = await self.get_dice_roll(ctx, throw_command, *args)

            if roll_output is None:
                return

            for i, o in lobby_members.items():
                if (ctx.author.name in lobby_members) and (i == lobby_host):
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"{ctx.author.name} rolled {roll_output}")

            await ctx.send(f"You have rolled {roll_output}")

        else:
            await ctx.send("> This command only works if there is a lobby and you are a member of it!")

    @commands.command(name="scroll", aliases=["sr"], help="Shorthand '!sr'. This is a secret roll that sends "
                                                          "the result to the DM only")
    async def secret_roll(self, ctx, throw_command: str = "1d20", *args):
        if lobby:
            roll_output = await self.get_dice_roll(ctx, throw_command, *args)

            if roll_output is None:
                return

            for i, o in lobby_members.items():
                if (ctx.author.name in lobby_members) and (i == lobby_host):
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"{ctx.author.name} rolled {roll_output}")

            await ctx.send(f"> You have rolled! Your roll has been sent to the DM!")

        else:
            await ctx.send("> This command only works if there is a lobby and you are a member of it!")

    @commands.command(name="rnd", aliases=["rng"], help="This is a random number. Defaults to 0-100. "
                                                        "The format is <start_of_range> - <end_of_range>. ")
    async def rnd(self, ctx, *args):
        rng = ""
        rng_start = 0
        rng_end = 100

        for i in args:
            rng += i

        if "-" in rng:
            try:
                if rng[0] == "-":
                    range_list = rng[1:]
                    range_list = re.split(r"-", range_list)
                    rng_start = -int(range_list[0])
                    rng_end = int(range_list[1])
                else:
                    range_list = re.split(r"-", rng)
                    rng_start = int(range_list[0])
                    rng_end = int(range_list[1])
            except ValueError:
                await ctx.send(">>> Please input an integer format of form '<start_int>-<end_int>'\n"
                               "Format has been defaulted to end at 100")

        # Broadcasts the results to the members of the lobby and does not if no lobby exists
        if lobby and (ctx.author.name in lobby_members) and (ctx.author.name != lobby_host):
            for i, o in lobby_members.items():
                user = await ctx.bot.fetch_user(o)
                if rng_end > rng_start:
                    rnd_number = random.choice(range(rng_start, rng_end + 1))
                    await user.send(f"{ctx.author.name}'s random number between ({rng_start}-{rng_end}) is:\n"
                                    f"```{rnd_number}```")
                else:
                    await ctx.send(f"> The end of the range must be a higher value than the start!")

        else:
            if rng_end > rng_start:
                rnd_number = random.choice(range(rng_start, rng_end + 1))
                await ctx.send(f"Your random number between ({rng_start}-{rng_end}) is:\n"
                               f"```{rnd_number}```")
            else:
                await ctx.send(f"> The end of the range must be a higher value than the start!")


# Music


class Music(commands.Cog):
    """Basic music bot functionality"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 7000, 'eu', "music-node")
        self.bot.add_listener(self.bot.music.voice_update_handler, "on_socket_response")
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name="join")
    async def join(self, ctx):
        print("worked")

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


# Ciphers


class Ciphers(commands.Cog):
    """Some general ciphers to play around with!"""

    @commands.command(pass_context=True)
    async def caesar(self, ctx, *args):
        """This encrypts your messages in the caesar variety, which shits your letters by 3 and returns it."""
        message = ""
        for i in args:
            message += i + " "
        message = message.rstrip()
        message = message.split(" ")

        alphabet_dict = {c: i for i, c in enumerate(string.ascii_lowercase)}
        numbers_first_dict = {i: c for i, c in enumerate(string.ascii_lowercase)}
        new_message = ""

        for i in message:
            word = i.lower()
            new_word = ""
            for j in word:
                if (j == "!") or (j == ",") or (j == ".") or (j == ";") or (j == ":") \
                        or (j == "_") or (j == "-") or (j == "'") or (j == '"'):
                    new_word += j
                elif alphabet_dict[j] > 22:
                    number = alphabet_dict[j] - 23
                    new_word += numbers_first_dict[number]
                else:
                    number = alphabet_dict[j] + 3
                    new_word += numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n{new_message}")

    @commands.command(pass_context=True)
    async def atbash(self, ctx, *args):
        """This converts your message into the Atbash ciper, which takes the reverse of each letter."""
        message = ""
        for i in args:
            message += i + " "
        message = message.rstrip()
        message = message.split(" ")

        alphabet_dict = {c: i for i, c in enumerate(string.ascii_lowercase)}
        numbers_first_dict = {i: c for i, c in enumerate(string.ascii_lowercase)}
        new_message = ""

        for i in message:
            word = i.lower()
            new_word = ""
            for j in word:
                if (j == "!") or (j == ",") or (j == ".") or (j == ";") or (j == ":") \
                        or (j == "_") or (j == "-") or (j == "'") or (j == '"'):
                    new_word += j
                else:
                    number = math.sqrt((alphabet_dict[j] - 25) ** 2)
                    new_word += numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n {new_message}")


# Adds the cog to the register


bot.add_cog(Ciphers())
bot.add_cog(DnDLobby())
bot.add_cog(DnD())

# Runs the bot

bot.run(TOKEN)
