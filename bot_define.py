from MyDataStock.DataStocks import DS_servers, DS_bot, DS_server
from discord.ext.commands import Bot
from discord import Intents, Guild, Role

from discord.ext.tasks import loop
from Help import Help
from os import environ

from pathlib import Path

intents = Intents.all()
intents.typing = False
intents.bans = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
intents.dm_messages = False
intents.dm_reactions = False


class MyBot(Bot):

    name_project = str()
    funcs = {}
    list_load_first = False
    list_func_loop = []
    list_func_ready = []
    ms_dict = {}
    pages = {}
    emojis_numbers = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟",
    ]

    def __init__(self):
        self.ds_bot = DS_bot().pull()
        super().__init__(
            description=self.ds_bot.desc,
            intents=intents,
            case_insensitive=True,
            command_prefix=self.ds_bot.prefix
        )
        extentions_folder = environ["DISCORD_BOT_EXTENTIONS_FOLDER"]
        self.name_project = environ["DISCORD_BOT_PROJECT_NAME"]
        self.help_command = Help()
        self.list_func_loop.append(self.loop_update)

        for f in Path(extentions_folder).glob("*.py"):
            self.load_extension(f"{extentions_folder}.{f.stem}")

    async def on_ready(self):
        if not (self.list_load_first):
            return
        else:
            self.list_load_first = False

        self.update_ds()

        for func in self.list_func_loop:
            await func.start()
        if self.list_func_ready:
            for func in self.list_func_ready:
                await func()

    def update_ds(self):
        ds = DS_servers().pull()
        for guild in self.guilds:
            guild = Guild
            if not(ds.get(guild.id)):
                ser = DS_server(id=guild.id)
                ser.initialize()
                ds.write(ser)

    @loop(hours=3.0)
    async def loop_update(self):
        print("update")
        self.update_ds()
        pass
