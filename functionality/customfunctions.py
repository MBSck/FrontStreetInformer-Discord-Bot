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

    # Load Token

    load_dotenv(os.path.join("assets/Token.env"))

    # Configure bot tokens

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("GUILD_TOKEN")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    return bot, TOKEN, GUILD

# Singleton metaclass


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super(Singleton, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instance


# Writes updates and reads the config file

class Updater(metaclass=Singleton):
    def __init__(self):
        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        if not os.path.isfile(os.path.join(install_path, "config.cfg")):
            self.create_cfg_file()

    def create_cfg_file(self):
        """Creates the config.cfg file"""
        # Writes down the install data into file
        with open(os.path.join(install_path, "config.cfg"), "w") as f:
            # Install config
            f.write("[Install-Config]\n")
            f.write(f"Install_Date = {datetime.datetime.now()}\n")
            f.write(f"Install_Path = {install_path}\n")

            f.write('\n')

            # Runtime config
            f.write("[Runtime-Config]\n")
            f.write(f"Date = {datetime.date.today()}\n")
            f.write(f"Time_Since_Last_TimeStep = {round(time.time())}\n")
            f.write(f"Lobby = False\n")
            f.write(f"Lobby_Locked = False\n")
            f.write(f"Lobby_Host = ''\n")
            f.write(f"Lobby_Members = ''\n")

    def update_cfg_file(self, header: str, key: str, value):
        """Updates the config file"""
        update_object = self.cfg_parser[header]
        update_object[key] = str(value)

        with open(os.path.join(install_path, "config.cfg"), "w") as f:
            self.cfg_parser.write(f)

    def read_cfg_file(self, header: str, key: str):
        """Gets the data from the config file"""
        self.cfg_parser.read(os.path.join(install_path, "config.cfg"))

        # reads out the data
        data = self.cfg_parser.get(header, key)

        return data
