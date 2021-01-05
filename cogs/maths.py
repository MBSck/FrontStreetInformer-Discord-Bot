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

    @commands.command(name="mul", aliases=["m"], help="Shorthand '!m'. Adds two or more numbers. Separate with spaces."
                                                      "Can also divide with fractions e.g. 0.5 etc.")
    async def mul(self, ctx, *args):
        numbers = []

        for i in args:
            numbers.append(float(i))

        total = 1.0
        for i in numbers:
            total *= i

        if total % 2 == 0:
            total = int(total)

        await ctx.send(f"Your multiplication result is {total}")
