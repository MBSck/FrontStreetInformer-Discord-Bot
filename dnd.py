import discord
from discord.ext import commands

# DnD


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