from assets.variables_and_imports import *
from functionality.tools import Updater

# DnD - Lobby


class DnDLobby(commands.Cog):
    """DnD commands that enable online gaming with the discord bot"""
    def __init__(self):
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

    def write_lobby_members(self):
        for i, o in self.lobby_members.items():
            self.updater.update_cfg_file("Lobby-Members", i, o)

    @commands.command(name="lobby.start", aliases=["l.s"], help="Starts a DnD lobby")
    async def lobby_start(self, ctx):

        # Update check
        self.check_for_updates()

        # Sets the command giver as the host if lobby not created, else member
        if not self.lobby:
            self.updater.update_cfg_file(self.section, "Lobby_Host", str(ctx.author.name).lower())
            self.lobby_members[str(ctx.message.author.name).lower()] = ctx.message.author.id
            self.write_lobby_members()
            self.updater.update_cfg_file(self.section, "Lobby", "True")
            self.check_for_updates()

            await ctx.send("> Lobby has been created!")

        else:
            await ctx.send("> There is already another lobby!")

    @commands.command(name="lobby.close", aliases=["l.c"], help="Closes a DnD lobby")
    async def lobby_close(self, ctx):

        # Update check
        self.check_for_updates()

        # Closes the lobby, if lobby host and removes members
        if self.lobby:
            if str(ctx.author.name).lower() == self.lobby_host:
                self.updater.update_cfg_file(self.section, "Lobby", "False")
                self.updater.update_cfg_file(self.section, "Lobby_Host", None)

                for i, o in self.lobby_members.items():
                    self.updater.cfg_parser.remove_option("Lobby-Members", i)

                self.check_for_updates()

                await ctx.send("> Lobby has been closed!")

            else:
                await ctx.send("> You do not have permission to do that!")

        else:
            await ctx.send("> There is no lobby active right now!")

    @commands.command(name="lobby.status", aliases=["l.st"], help="Checks the status of the lobby")
    async def lobby_status(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby:
            await ctx.send(f"> There is a lobby online with {len(self.lobby_members)} members.")
        else:
            await ctx.send("> No lobby exists.")

    @commands.command(name="lobby.members", aliases=["l.m"], help="Displays the members of the lobby")
    async def lobby_members(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby:
            if str(ctx.message.author.name).lower() in self.lobby_members:
                message = ""

                for i in self.lobby_members:
                    if i == self.lobby_host:
                        message += "__Host__: " + str(i).capitalize() + ", "
                    else:
                        message += str(i).capitalize() + ", "

                message = message[:-2]

                await ctx.send(f">>> Members in the lobby:\n{message}")
        else:
            await ctx.send("> There is no lobby or it has been locked!")

    @commands.command("lobby.lock", aliases=["l.lo"], help="Command for the host to lock the lobby")
    async def lobby_locked(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby and ctx.author.name == self.lobby_host:
            self.updater.update_cfg_file(self.section, "Lobby_Locked", "True")
            self.check_for_updates()
            await ctx.send("> Lobby has been **locked**!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.unlock", aliases=["l.u"], help="Command for the host to unlock the lobby")
    async def lobby_unlocked(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby_locked:
            if self.lobby and ctx.author.name == self.lobby_host:
                self.updater.update_cfg_file(self.section, "Lobby_Locked", "False")
                self.check_for_updates()
                await ctx.send("> Lobby has been **unlocked**!")

            else:
                await ctx.send("> You do not have permission to do that!")

        else:
            await ctx.send("> You cannot unlock what is not locked!")

    @commands.command(name="lobby.join", aliases=["l.j"], help="Joins a DnD lobby")
    async def join_lobby(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby and not self.lobby_locked:
            if str(ctx.message.author.name).lower() in self.lobby_members:
                await ctx.send("> You have already joined the lobby.")

            else:
                self.lobby_members[str(ctx.message.author.name).lower()] = ctx.message.author.id
                message = ""

                for i in self.lobby_members:
                    message += str(i).capitalize() + ", "

                message = message[:-2]

                for i, o in self.lobby_members.items():
                    user = await ctx.bot.fetch_user(o)
                    await user.send(f"> {ctx.author.name} has joined the lobby.")

                await ctx.send(f">>> You have joined the lobby!\nWelcome! Members in the lobby:\n{message}")

        else:
            await ctx.send("> There is no lobby to join or it has been locked!")

    @commands.command(name="lobby.leave", aliases=["l.le"], help="Leaves a DnD lobby")
    async def lobby_leave(self, ctx):

        # Update check
        self.check_for_updates()

        if self.lobby:
            del self.lobby_members[str(ctx.author.name).lower()]

            for i, o in self.lobby_members.items():
                user = await ctx.bot.fetch_user(o)

                if str(ctx.author.name).lower() == self.lobby_host:
                    self.lobby_host = random.choice(self.lobby_members)
                    self.updater.update_cfg_file(self.section, "Lobby_Host", self.lobby_host)
                    await self.lobby_host_change(ctx, self.lobby_host)

                await user.send(f"> {ctx.author.name} has **left** the lobby.")

            if len(self.lobby_members) == 0:
                # Lazy bugfix for the problem of closing the lobby if you leave yourself and lose the rights to do that
                await ctx.send("> You were the last member, lobby has been closed!")
                await self.updater.create_cfg_file()

            await ctx.send("> You have left the lobby!")

        else:
            await ctx.send("> You are in no lobby!")

    @commands.command(name="lobby.kick", aliases=["l.k"], help="Command for the host to kick a member from the lobby")
    async def lobby_kick(self, ctx, name):

        # Update check
        self.check_for_updates()

        if self.lobby and (str(ctx.author.name).lower() == self.lobby_host):
            if name in self.lobby_members:
                if name == self.lobby_host:
                    if len(self.lobby_members) == 1:
                        await self.lobby_close(ctx)

                    else:
                        await self.lobby_host_change(ctx, random.choice(self.lobby_members))

            else:
                for i, o in self.lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == name:
                        del self.lobby_members[i]
                        await user.send("> You have been **kicked** from the lobby!")

                    else:
                        await user.send(f"> {name} has been **kicked** from the lobby!")

                else:
                    await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")

    @commands.command(name="lobby.host", aliases=["l.h"],
                      help="Command for the host to change host to another member of the lobby")
    async def lobby_host_change(self, ctx, name):

        # Update check
        self.check_for_updates()

        if self.lobby and ctx.author.name == self.lobby_host:
            if name in self.lobby_members:
                self.updater.update_cfg_file(self.section, "Lobby_Host", name)
                self.check_for_updates()
                for i, o in self.lobby_members.items():

                    user = await ctx.bot.fetch_user(o)

                    if i == self.lobby_host:
                        await user.send("> You are ***already*** the host of the lobby!")

                    elif (i == name) and (name != self.lobby_host):
                        await user.send("> You have been made **host** of the lobby!")

                    else:
                        await user.send(f"> {name} has been made into the **host** of the lobby!")

            else:
                await ctx.send("> User not found!")

        else:
            await ctx.send("> You do not have permission to do that!")
