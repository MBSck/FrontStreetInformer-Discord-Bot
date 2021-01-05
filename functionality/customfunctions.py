from assets.variables_and_imports import *

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


# Initializes the bot

def startup(startup_delay):
    # To ensure it can be shutdown if it causes any problems to the raspi

    time.sleep(startup_delay)

    # Calls the logger once to initialize it

    logger = Log()

    # Load Token

    load_dotenv(os.path.join("assets/Token.env"))

    # Configure bot tokens

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("GUILD_TOKEN")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    return bot, TOKEN, GUILD

