# Importing the cogs

from cogs import music, ciphers, dnd, dndlobby, utility, maths


def add_cogs(bot):
    """Adds the cogs to the register"""
    bot.add_cog(ciphers.Ciphers())
    bot.add_cog(dndlobby.DnDLobby())
    bot.add_cog(dnd.DnD())
    bot.add_cog(utility.Utility())
    bot.add_cog(maths.Math())
