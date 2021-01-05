from assets.variables_and_imports import *

# Math Cog


class Math(commands.Cog):
    """Simple math functionalities"""

    @commands.command(name="add", aliases=["a"], help="Shorthand '!a'. Adds two or more numbers. "
                                                      "Separate with spaces. "
                                                      "Can also add negative numbers with -<number>")
    async def add(self, ctx, *args):
        numbers = []
        for i in args:
            numbers.append(int(i))

        total = 0
        for i in numbers:
            total += i

        await ctx.send(f"Your sum total is {total}")

    @commands.command(name="mul", aliases=["m"], help="Shorthand '!m'. Adds two or more numbers. Separate with spaces")
    async def mul(self, ctx, *args):
        numbers = []

        for i in args:
            numbers.append(int(i))

        total = 1
        for i in numbers:
            total *= i

        await ctx.send(f"Your multiplication result is {total}")
