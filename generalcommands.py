import discord
from discord.ext import commands

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