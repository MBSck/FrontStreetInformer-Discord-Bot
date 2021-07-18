from assets.variables_and_imports import *

"""Implements general math functionality for the bot"""


class Math(commands.Cog):
    """Simple math functionalities"""

    @commands.command(name="add", aliases=["a"], help="Shorthand '!a'. Adds two or more numbers. "
                                                      "Separate with spaces. "
                                                      "Can also add negative numbers with -<number>")
    async def add(self, ctx, *args: str):
        await ctx.send(f"Your sum total is {sum([float(i) for i in args])}")

    @commands.command(name="mul", aliases=["m"], help="Shorthand '!m'. Adds two or more numbers. "
                                                      "Separate with spaces. "
                                                      "Can also divide with fractions e.g. 0.5 etc.")
    async def mul(self, ctx, *args: str):

        total = 1
        for i in [float(i) for i in args]:
            total *= i

        await ctx.send(f"Your multiplication result is {round(total)}")


if __name__ == "__main__":
    print(sum([0.5, 10, 15]))
    print(help(sum))
