"""FrontStreetInformer-Discord-Bot
A Discord-Bot that encompasses several functions to enhance the users' experience"""

__author__ = "Marten Scheuck"

from functionality.cogs import add_cogs
from functionality.tools import *


def main():
    """The bots main functionality"""

    # Startup-function that calls the bots main functionality and reads the cfg-file
    bot, TOKEN, GUILD = startup(0)

    @bot.event
    async def game_presence():
        """Changes the status of the game, which the bot is playing. Passive task"""

        await bot.wait_until_ready()

        while not bot.is_closed():
            status = random.choice(games)

            await bot.change_presence(activity=discord.Game(status, type=3))
            await asyncio.sleep(30)

    bot.loop.create_task(game_presence())

    '''
    @bot.event
    async def on_message(message):
        """Reacts to a user message to the bot"""
        ...
    '''

    @bot.event
    async def on_ready():
        """Sends a message to the Bots Host (in console) in order to verify its activation"""
        print(f"{bot.user.name} has connected to Discord!")

    @bot.event
    async def on_command_error(ctx, error):
        """If a command cannot be accessed by a user, the bot replies with an error"""
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")

    # Adds the cogs
    add_cogs(bot)

    # Runs the bot
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
