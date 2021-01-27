from assets.variables_and_imports import *

############################################################
# Functions
############################################################

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

    # Rewrite the config file

    updater = Updater()
    updater.create_cfg_file()

    # Load Token

    load_dotenv(os.path.join("assets/Token.env"))

    # Configure bot tokens

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("GUILD_TOKEN")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    return bot, TOKEN, GUILD

############################################################
# Classes
############################################################

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

        # Defines cfg path
        self.cfg_path = os.path.join(install_path, "config.cfg")

        if not os.path.isfile(self.cfg_path):
            self.create_cfg_file()

    def create_cfg_file(self):
        """Creates the config.cfg file"""

        # Writes the install data into file
        with open(os.path.join(install_path, "config.cfg"), "w") as f:

            # Runtime config
            f.write("[Runtime-Config]\n")
            f.write(f"Startup_Date = {datetime.date.today()}\n")
            f.write(f"Runtime_Path = {install_path}\n")

            f.write('\n')

            # Lobby config
            f.write("[Lobby-Config]\n")
            f.write(f"Lobby = False\n")
            f.write(f"Lobby_Locked = False\n")
            f.write(f"Lobby_Host = \n")

            f.write('\n')

            # Lobby members register
            f.write("[Lobby-Members]\n")

    def update_cfg_file(self, header: str, key: str, value):
        """Updates the config file"""
        update_object = self.cfg_parser[header]
        update_object[key] = str(value)

        with open(self.cfg_path, "w") as f:
            self.cfg_parser.write(f)

    def read_cfg_file(self, header: str, key: str):
        """Gets the data from the config file"""
        self.cfg_parser.read(self.cfg_path)

        # reads out the data
        data = self.cfg_parser.get(header, key)

        return data

    def readout_section_to_dict(self, section):
        """Read out section into dictionary"""
        self.cfg_parser.read(self.cfg_path)

        dictionary = {}

        # Checks if section exists in file
        if self.cfg_parser.has_section(section):
            for sec in self.cfg_parser.sections():
                if sec == section:
                    for k, v in self.cfg_parser.items(sec):
                        dictionary[k] = v

            return dictionary

        else:
            print(f"No section of name {section} found! No information was written into dictionary!")
            return

    def readout_whole_cfg_file(self):
        """Reads out all of the config file"""
        self.cfg_parser.read(self.cfg_path)
        for i in self.cfg_parser.sections():
            print('Section:', i)
            for k, v in self.cfg_parser.items(i):
                print("{} = {}".format(k, v))
                print()
