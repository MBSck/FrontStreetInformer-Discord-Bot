"""Author: Marten Scheuck - FrontStreetInformer"""
# Importing  functionality

from functionality.cogs import add_cogs
from functionality.tools import *

if __name__ == "__main__":
        
    # Startup the bot

    bot, TOKEN, GUILD = startup(0)

    # Calls the logger once to initialize it

    logger = Log()

    # Calls the Updater once to initialize it

    updater = Updater()

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
    '''
    @bot.event
    async def on_message(message):
        """Reacts to a user message to the bot"""
        ...
    '''

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


    # Adds the cogs

    add_cogs(bot)

    # Runs the bot

    bot.run(TOKEN)
