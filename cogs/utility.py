from assets.variables_and_imports import *
from functionality.tools import get_time
"""General Cogs that take care of user-side utility, bug handeling, etc."""


class Utility(commands.Cog):
    """Here we put all general commands"""

    @commands.command(name="sub", help="This makes the bot torment you again. Can be a specifiy command in form of"
                                  "!sub <command_name>")
    async def sub(self):
        ...

    @commands.command(name="unsub", help="This removes you from any commands that the bot targets you with!"
                                    "Can also be a specifiy command with !unsub <command_name>")
    async def unsub(self):
        ...


    @commands.command(name="suggest", help="This makes a suggestion for new bot functionality")
    async def suggest(self, ctx, *args):

        suggestion = ""
        for arg in args:
            if arg in string.punctuation:
                suggestion += arg
            else:
                suggestion += " " + arg
        suggestion = "'" + suggestion[1:] + "'"

        with open(os.path.join("suggestions.txt"), "a") as f:
            f.write(f"\nThis suggestions has been sent in on {get_time()[1]} by {ctx.message.author} and reads:\n"
                    f"{suggestion}\n")
            f.close()

        await ctx.send(f"Suggestion has been recieved at {get_time()[0]}, thank you!")

    @commands.command(name="bug", help="This reports bugs so they can be fixed")
    async def bug(self, ctx, *args):

        bugs = ""
        for arg in args:
            if arg in string.punctuation:
                bugs += arg
            else:
                bugs += " " + arg

        bugs = "'" + bugs[1:] + "'"

        with open(os.path.join("bug_log.txt"), "a") as f:
            f.write(f"\nThis bug report has been sent in on {get_time()[1]} by {ctx.message.author} and reads:\n"
                    f"{bugs}\n")
            f.close()

        await ctx.send(f"The bug report has been recieved at {get_time()[0]}, thank you!")

    @commands.command(name="kungfu", help="Nifty stuff about kung fu.")
    async def kung_fu_write(self, ctx):
        await ctx.send(f"As requested something about Kung fu!\n {random.choice(kung_fu)}")

    '''
    @commands.command(name="j.search", help="Looks up Japanese words and Kanji. Uses Jisho as Basis")
    async def j_search(self, ctx, search_term):
    
        page = urllib.request.urlopen("https://jisho.org/")
        print(page.read())

    @commands.command(name="search.airdates", help="Looks for your series latest airdates")
    async def search_air_dates(self, ctx, series_name):
    
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
    '''


if __name__ == "__main__":
    print(string.punctuation)