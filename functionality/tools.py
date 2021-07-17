import os

from assets.variables_and_imports import *

############################################################
# Functions
############################################################


def get_time():
    """Gets the actual time and the datetime"""
    actual = datetime.datetime.now()
    actual_time = f"{actual.hour}:{actual.minute}:{actual.second}"
    actual_date_time = f"{actual.day}.{actual.month}.{actual.year} at {actual_time}"
    return actual_time, actual_date_time


def startup(startup_delay: int):
    """This function takes care of the bot-startup"""
    # To ensure it can be shutdown if it causes any problems to the raspi
    time.sleep(startup_delay)

    # Rewrite the config file
    updater = Updater()
    updater.create_cfg_file()

    # Load Token
    load_dotenv(os.path.join("../../Token.env"))

    # Configure bot tokens
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    return bot, TOKEN, GUILD

############################################################
# Classes
############################################################


class Singleton(type):
    """A singleton metaclass, that creates unique instanced classes"""

    def __init__(cls, *args, **kwargs):
        """Supers and sets private class variables"""
        cls.__instance = None
        super(Singleton, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        """Checks if there is alrady a class instance, and if not creates it"""
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instance


class Updater(metaclass=Singleton):
    """This class writes and updates the config-file"""

    def __init__(self):
        """Sets the class attributes"""

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


if __name__ == "__main__":
    load_dotenv(os.path.join("../../Token.env"))
    print(os.getenv("DISCORD_GUILD"))
