import re

from cogs.dndlobby import *

"""Dungeons and Dragons online functionality for the bot"""


class DnD(commands.Cog):
    """Gameplay functions for DnD"""

    def __init__(self):
        """Initializes all the classes attributes"""

        # Initialize updater
        self.updater = Updater()

        # Sets the config file section name
        self.section = "Lobby-Config"

        # Reads out the values out of the cfg
        self.lobby = False
        self.lobby_locked = False
        self.lobby_members = {}
        self.lobby_host = ""

    def check_for_updates(self):
        """Updates the values and checks if anything changed"""

        self.lobby = ast.literal_eval(self.updater.read_cfg_file(self.section, "Lobby"))
        self.lobby_locked = ast.literal_eval(self.updater.read_cfg_file(self.section, "Lobby_Locked"))
        self.lobby_members = self.updater.readout_section_to_dict("Lobby-Members")
        self.lobby_host = self.updater.read_cfg_file(self.section, "Lobby_Host")

    @staticmethod
    async def get_dice_roll(ctx, dice: str = "1d20", *args: str):
        """Gets the dice rolls after user output and calculates its sum"""

        try:
            # Gets all arguments
            arg_list = [dice]
            arg_list.extend(args)

            # Sets the list for the die operators
            dice_operator_list = [re.split('([-+/*])', i) for i in arg_list]
            multiple_dice_list = []

            # Removes any possible white-spaces
            for i in dice_operator_list.copy():
                if i == "":
                    dice_operator_list.remove(i)

            second_line = "```"

            # If the format fits and only one argument is passed split die number and die range
            if len(dice_operator_list) == 1:
                number_of_dice, die_range = map(int, dice.lower().split('d'))
                result_dice = [random.randint(1, die_range) for _ in range(number_of_dice)]
                second_line += ' + '.join(str(i) for i in result_dice)

                # Checks for the die number
                if number_of_dice > 1:
                    sum_total = sum(result_dice)
                    second_line += f" = {sum_total}"

                multiple_dice_list.append(dice_operator_list[0].lower())

            # If more than one die is passed by the end-user parse the message
            else:
                sum_total = 0
                if len(dice_operator_list) > 3:
                    second_line += '{'

                # The message is being checked for any modifiers/operators
                for i, o in enumerate(dice_operator_list):
                    if len(dice_operator_list) > 1:
                        if 'd' in o.lower():

                            # Catches any index errors -> Lazy workaround
                            try:
                                # If operator does not exist, pass '+0'
                                if dice_operator_list[i+1] not in ['+', '-', '/', '*']:
                                    dice_operator_list.insert(i+1, '+')
                                    dice_operator_list.insert(i+2, '0')

                            except IndexError:
                                dice_operator_list.insert(i+1, '+')
                                dice_operator_list.insert(i+2, '0')

                            # Checks if modifier of operator is '0'
                            if dice_operator_list[i+2] == '0':
                                multiple_dice_list.append(dice_operator_list[i].lower())

                            # If everythin was input correctly, append it to the right list
                            else:
                                multiple_dice_list.append(f"{dice_operator_list[i].lower()}"
                                                          f"{dice_operator_list[i+1]}{dice_operator_list[i+2]}")

                        # Gets default value if first element of list is operator
                        if (i == 0) and o in ['+', '-', '/', '*']:
                            dice_operator_list.insert(0, '1d20')

                            multiple_dice_list.append(f"1d20"
                                                      f"{dice_operator_list[1]}{dice_operator_list[2]}")
                            continue

                    # Check for operators
                    if o in ['+', '-', '/', '*']:

                        # Catch any index errors
                        try:

                            # Reformatting of the output string
                            if len(dice_operator_list) > 3:
                                second_line += "["

                            # Gets operator and splits the input into number of dice and range of die
                            operator_func = operator_dict[dice_operator_list[i]]
                            number_of_dice_part, die_range_part = map(int, dice_operator_list[i-1].lower().split('d'))
                            result_dice = [random.randint(1, die_range_part) for _ in range(number_of_dice_part)]
                            second_line_part = "(" + ' + '.join(str(i) for i in result_dice)

                            # Sums up over all of the single dice and then uses the modifying operator
                            sum_total_part = sum(result_dice)
                            sum_total_part = operator_func(sum_total_part, int(dice_operator_list[i+1]))
                            sum_total += sum_total_part

                            # Reformatting of output string
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

            return first_line + second_line

        except Exception:
            await ctx.send("> Input of the wrong format!")
            return

    @commands.command(name="roll", aliases=["r"], help="Shorthand '!r'.Rolls dice. Defaults to d20."
                                                       " Input '!roll/!r [# dice]d[# sides] + [modifiers]'\n"
                                                       "Allowed operators for modifiers are + - / *. "
                                                       "Can also row multiple dice at the same time. Of the format"
                                                       " !roll/!r [# dice]d[# sides] [+-/*] [modifiers]"
                                                       " [# dice]d[# sides] [+-/*] [modifiers] ...")
    async def roll(self, ctx, throw_command: str = "1d20", *args):

        # Update check
        self.check_for_updates()

        if (roll_output := await self.get_dice_roll(ctx, throw_command, *args)) is None:
            return

        # Broadcasts the results to the members of the lobby and does not if no lobby exists
        if self.lobby and (str(ctx.author.name).lower() in self.lobby_members) \
                and (str(ctx.author.name).lower() != self.lobby_host):
            for i, o in self.lobby_members.items():
                user = await ctx.bot.fetch_user(o)
                await user.send(f"{ctx.author.name} rolled {roll_output}")
        else:
            await ctx.send(f"You have rolled {roll_output}")

    @commands.command(name="gmroll", aliases=["gr"], help="Shorthand '!gr'.Rolls a die and sends result directly "
                                                          "to Game Master and also you."
                                                          " Also defaults to 1d20. Great for hidden/discreet checks")
    async def gm_roll(self, ctx, throw_command: str = "1d20", *args):

        # Update check
        self.check_for_updates()

        if self.lobby:

            if (roll_output := await self.get_dice_roll(ctx, throw_command, *args)) is None:
                return

            for i, o in self.lobby_members.items():
                if (str(ctx.author.name).lower() in self.lobby_members) and (i == self.lobby_host):
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"{ctx.author.name} rolled {roll_output}")

            await ctx.send(f"You have rolled {roll_output}")

        else:
            await ctx.send("> This command only works if there is a lobby and you are a member of it!")

    @commands.command(name="scroll", aliases=["sr"], help="Shorthand '!sr'. This is a secret roll that sends "
                                                          "the result to the DM only")
    async def secret_roll(self, ctx, throw_command: str = "1d20", *args):

        # Update check
        self.check_for_updates()

        if self.lobby:

            if (roll_output := await self.get_dice_roll(ctx, throw_command, *args)) is None:
                return

            for i, o in self.lobby_members.items():
                if (str(ctx.author.name).lower() in self.lobby_members) and (i == self.lobby_host):
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"{ctx.author.name} rolled {roll_output}")

            await ctx.send(f"> You have rolled! Your roll has been sent to the DM!")

        else:
            await ctx.send("> This command only works if there is a lobby and you are a member of it!")

    @commands.command(name="rnd", aliases=["rng"], help="This is a random number. Defaults to 0-100. "
                                                        "The format is <start_of_range> - <end_of_range>. ")
    async def rnd(self, ctx, *args):

        # Update check
        self.check_for_updates()

        # Gets the arguments and sets the default variables
        rng = "".join(i for i in args)
        rng_start, rng_end = 0, 100

        if "-" in rng:
            try:
                if rng[0] == "-":
                    -rng_start, rng_end = re.split(r"-", rng[1:])
                else:
                    rng_start, rng_end = re.split(r"-", rng[1:])

            except ValueError:
                await ctx.send(">>> Please input an integer format of form '<start_int>-<end_int>'\n"
                               "Format has been defaulted to end at 100")

        # Broadcasts the results to the members of the lobby and does not if no lobby exists
        if self.lobby and (str(ctx.author.name).lower() in self.lobby_members) and\
                (str(ctx.author.name).lower() != self.lobby_host):

            for i, o in self.lobby_members.items():
                user = await ctx.bot.fetch_user(o)
                if rng_end > rng_start:
                    await user.send(f"{ctx.author.name}'s random number between ({rng_start}-{rng_end}) is:\n"
                                    f"```{random.choice(range(rng_start, rng_end + 1))}```")
                else:
                    await ctx.send(f"> The end of the range must be a higher value than the start!")

        else:
            if rng_end > rng_start:
                await ctx.send(f"Your random number between ({rng_start}-{rng_end}) is:\n"
                               f"```{random.choice(range(rng_start, rng_end + 1))}```")
            else:
                await ctx.send(f"> The end of the range must be a higher value than the start!")