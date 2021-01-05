from assets.variables_and_imports import *

# Ciphers


class Ciphers(commands.Cog):
    """Some general ciphers to play around with!"""

    @commands.command(pass_context=True)
    async def caesar(self, ctx, *args):
        """This encrypts your messages in the caesar variety, which shits your letters by 3 and returns it."""
        message = ""
        for i in args:
            message += i + " "
        message = message.rstrip()
        message = message.split(" ")

        alphabet_dict = {c: i for i, c in enumerate(string.ascii_lowercase)}
        numbers_first_dict = {i: c for i, c in enumerate(string.ascii_lowercase)}
        new_message = ""

        for i in message:
            word = i.lower()
            new_word = ""
            for j in word:
                if (j == "!") or (j == ",") or (j == ".") or (j == ";") or (j == ":") \
                        or (j == "_") or (j == "-") or (j == "'") or (j == '"'):
                    new_word += j
                elif alphabet_dict[j] > 22:
                    number = alphabet_dict[j] - 23
                    new_word += numbers_first_dict[number]
                else:
                    number = alphabet_dict[j] + 3
                    new_word += numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n{new_message}")

    @commands.command(pass_context=True)
    async def atbash(self, ctx, *args):
        """This converts your message into the Atbash ciper, which takes the reverse of each letter."""
        message = ""
        for i in args:
            message += i + " "
        message = message.rstrip()
        message = message.split(" ")

        alphabet_dict = {c: i for i, c in enumerate(string.ascii_lowercase)}
        numbers_first_dict = {i: c for i, c in enumerate(string.ascii_lowercase)}
        new_message = ""

        for i in message:
            word = i.lower()
            new_word = ""
            for j in word:
                if (j == "!") or (j == ",") or (j == ".") or (j == ";") or (j == ":") \
                        or (j == "_") or (j == "-") or (j == "'") or (j == '"'):
                    new_word += j
                else:
                    number = math.sqrt((alphabet_dict[j] - 25) ** 2)
                    new_word += numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n {new_message}")