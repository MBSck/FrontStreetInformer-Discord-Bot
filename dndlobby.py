import discord
from discord.ext import commands

# DnD - Lobby


class DnDLobby(commands.Cog):
    """DnD commands that enable online gaming with the discord bot"""

    @commands.command(name="lobby.start", aliases=["l.s"])
    async def lobby_start(self, ctx):
        """Starts a DnD lobby"""
        global lobby, lobby_host
        if not lobby:
            lobby_host = ctx.author.name
            lobby_members[ctx.message.author.name] = ctx.message.author.id
            lobby = True

            await ctx.send("> Lobby has been created!")

        else:
            await ctx.send("> There is already another lobby!")

    @commands.command(name="lobby.close", aliases=["l.c"])
    async def lobby_close(self, ctx):
        """Closes a DnD lobby"""
        global lobby, lobby_host, lobby_members
        if lobby:
            if ctx.author.name == lobby_host:
                lobby = False
                lobby_host = ""
                lobby_members.clear()

                await ctx.send("> Lobby has been closed!")

            else:
                await ctx.send("> You do not have permission to do that!")

        else:
            await ctx.send("> There is no lobby active right now!")

    @commands.command(name="lobby.status", aliases=["l.st"])
    async def lobby_status(self, ctx):
        """Checks the status of the lobby"""
        if lobby:
            await ctx.send(f"> There is a lobby online with {str(len(lobby_members))} members.")
        else:
            await ctx.send("> No lobby exists.")

    @commands.command("lobby.lock", aliases=["l.lo"])
    async def lobby_locked(self, ctx):
        """Command for the host locks the lobby"""
        global lobby_locked
        if lobby and ctx.author.name == lobby_host:
            lobby_locked = True
            await ctx.send("> Lobby has been **locked**!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.unlock", aliases=["l.u"])
    async def lobby_unlocked(self, ctx):
        """Command for the host to unlock the lobby"""
        global lobby_locked
        if lobby and ctx.author.name == lobby_host:
            lobby_locked = False
            await ctx.send("> Lobby has been **unlocked**!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.join", aliases=["l.j"])
    async def join_lobby(self, ctx):
        """Joins a DnD lobby"""
        global lobby_members

        if lobby and not lobby_locked:
            if ctx.message.author.name in lobby_members:
                await ctx.send("> You have already joined the lobby.")

            else:
                lobby_members[ctx.message.author.name] = ctx.message.author.id
                message = ""

                for i in lobby_members:
                    message += i + ", "

                message = message[:-2]

                for i, o in lobby_members.items():
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"> {ctx.author.name} has joined the lobby.")

                await ctx.send(f">>> You have joined the lobby!\nWelcome! Members in the lobby:\n{message}")

        else:
            await ctx.send("> There is no lobby to join or it has been locked!")

    @commands.command(name="lobby.leave", aliases=["l.le"])
    async def lobby_leave(self, ctx):
        """Leaves a DnD lobby"""
        global lobby, lobby_members, lobby_host

        if lobby:
            del lobby_members[ctx.author.name]

            for i, o in lobby_members.items():
                user = await ctx.bot.fetch_user(o)

                if ctx.author.name == lobby_host:
                    lobby_host = ""
                    lobby_host = random.choice(lobby_members)
                    await self.lobby_host_change(ctx, lobby_host)

                await user.send(f"> {ctx.author.name} has **left** the lobby.")

            if len(lobby_members) == 0:
                lobby = False

            await ctx.send("> You have left the lobby!")

        else:
            await ctx.send("> You are in no lobby!")

    @commands.command(name="lobby.kick", aliases=["l.k"])
    async def lobby_kick(self, ctx, name):
        """Command for the host locks kicks a member of the lobby"""
        global lobby_members

        if lobby and ctx.author.name == lobby_host:
            if name in lobby_members:
                if name == lobby_host:
                    if len(lobby_members) == 1:
                        await self.lobby_close(ctx)

                    else:
                        await self.lobby_host_change(ctx, random.choice(lobby_members))

            else:
                for i, o in lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == name:
                        del lobby_members[i]
                        await user.send("> You have been **kicked** from the lobby!")

                    else:
                        await user.send(f"> {name} has been **kicked** from the lobby!")

                else:
                    await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.host", aliases=["l.h"])
    async def lobby_host_change(self, ctx, name):
        """Command for the host to change host to another member of the lobby"""
        global lobby_host

        if lobby and ctx.author.name == lobby_host:
            if name in lobby_members:
                lobby_host = name
                for i, o in lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == lobby_host:
                        await user.send("> You are ***already*** the host of the lobby!")

                    elif (i == name) and (name != lobby_host):
                        await user.send("> You have been made **host** of the lobby!")

                    else:
                        await user.send(f"> {name} has been made into the **host** of the lobby!")

            else:
                await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.members", aliases=["l.m"])
    async def lobby_members(self, ctx):
        """Displays the members of the lobby"""
        if lobby:
            if ctx.message.author.name in lobby_members:
                message = ""

                for i in lobby_members:
                    if i == lobby_host:
                        message += "__Host__: " + i + ", "
                    else:
                        message += i + ", "

                message = message[:-2]

                await ctx.send(f">>> Members in the lobby:\n{message}")
        else:
            await ctx.send("> There is no lobby or it has been locked!")