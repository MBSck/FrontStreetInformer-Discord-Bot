from assets.variables_and_imports import *

"""Music cog for the bot"""


class Music(commands.Cog):
    """Basic music bot functionality"""

    def __init__(self, bot) -> None:
        """Initializes the attributes of the class"""

        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 7000, 'eu', "music-node")
        self.bot.add_listener(self.bot.music.voice_update_handler, "on_socket_response")
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name="join", help="Makes the bot join the voice channel.")
    async def join(self, ctx):
        ...

    async def track_hook(self, event):
        """"""

        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """Makes the bot connect to the server"""

        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


if __name__ == "__main__":
    pass
