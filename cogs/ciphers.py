from assets.variables_and_imports import *

"""All Cipher classes that en-/decrypt"""


class Ciphers(commands.Cog):
    """Some general ciphers to play around with!"""

    def __init__(self) -> None:
        """Initializes the dicts used for encyphering"""

        self.alphabet_dict = {c: i for i, c in enumerate(string.ascii_lowercase)}
        self.numbers_first_dict = {i: c for i, c in enumerate(string.ascii_lowercase)}

    @commands.command(pass_context=True)
    async def caesar(self, ctx, *args: str):
        """This encrypts your messages in the caesar variety, which shits your letters by 3 and returns it."""

        message = ((" ".join(i for i in args)).rstrip()).strip(" ")
        new_message = ""

        for i in message:
            new_word = ""
            for j in i.lower():
                if j in string.punctuation:
                    new_word += j
                elif self.alphabet_dict[j] > 22:
                    number = self.alphabet_dict[j] - 23
                    new_word += self.numbers_first_dict[number]
                else:
                    number = self.alphabet_dict[j] + 3
                    new_word += self.numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n{new_message}")

    @commands.command(pass_context=True)
    async def atbash(self, ctx, *args: str):
        """This converts your message into the Atbash ciper, which takes the reverse of each letter."""

        message = ((" ".join(i for i in args)).rstrip()).strip(" ")
        new_message = ""

        for i in message:
            new_word = ""
            for j in i.lower():
                if j in string.punctuation:
                    new_word += j
                else:
                    number = math.sqrt((self.alphabet_dict[j] - 25) ** 2)
                    new_word += self.numbers_first_dict[number]

            new_message += new_word + " "
        new_message = new_message

        await ctx.send(f"Your secret message reads:\n {new_message}")


if __name__ == "__main__":
    print(string.punctuation)
