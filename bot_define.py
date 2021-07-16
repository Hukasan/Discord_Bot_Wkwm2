from file_io.file_io_s3 import json_io_s3 as jis
from discord.ext.commands import Bot
from discord import Intents, Guild, Role

from discord.ext.tasks import loop


intents = Intents.all()
intents.typing = False
intents.bans = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
intents.dm_messages = False
intents.dm_reactions = False


class MyBot(Bot):

    funcs = {}
    list_load_first = False
    list_func_loop = []
    list_func_ready = []
    ms_dict = {}
    mod_setup = jis("setup_test").iterate()
    dict_setup = mod_setup.get()
    mod_servers = jis("servers_test").iterate()
    dict_server = mod_servers.get()
    help_dict = {}
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

        super().__init__(
            description=self.dict_setup["DESC"],
            intents=intents,
            case_insensitive=True,
        )
        self.list_func_loop.append(self.loop_start)

    async def on_ready(self):
        if not (self.list_load_first):
            return
        else:
            self.list_load_first = False

        self.update_servers()

        if self.list_func_loop:
            for func in self.list_func_loop:
                await func()
        if self.list_func_ready:
            for func in self.list_func_ready:
                await func()

    def update_db(self):
        self.dict_server = self.mod_servers.get()
        self.dict_setup = self.mod_setup.get()
        for g in self.guilds:
            server = self.dict_server.get(str(g.id))
            if server:
                if g.rules_channel:
                    server.update({"rules_channel": g.rules_channel.id})
            else:
                if g.rules_channel:
                    self.dict_server.update({g.id: {"rules_channel": g.rules_channel.id}})
                else:
                    self.dict_server.update({g.id: {"rules_channel": None}})
            for role in g.roles:
                if role.is_bot_managed and (role.name == self.user.name):
                    self.dict_server[str(g.id)].update({"bot_role": role.id})
        self.mode_servers.put(self.dict_server)

    async def loop_start(self):
        await self.loop_update.start()

    @loop(hours=3.0)
    async def loop_update(self):
        self.update_db()
        pass
