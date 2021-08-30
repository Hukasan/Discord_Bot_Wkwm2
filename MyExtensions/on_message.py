from discord import Message
from discord.ext import commands

from bot_define import MyBot
from MyExtensions.app.MyCog import MyCog

class On_Message(commands.Cog):
    """
    会話干渉機能
    """

    def __init__(self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ms: Message):
        if (str(ms.author.id) in list(self.bot.ds_bot.ad_ids.values())) and ms.mentions:
            db = self.bot.servers
            serverdb = db.get(str(ms.guild.id))
            if serverdb:
                delay = serverdb.get("delay")
                if delay and serverdb.get("swich"):
                    await ms.delete(delay=delay)
                    return
            defdb = db.get("DEFAULT")
            if defdb:
                if defdb.get("swith"):
                    await ms.delete(delay=defdb.get("delay"))
        else:
            if ms.author.bot:
                return
            # コマンド文かどうか
            content = ms.content
            flag_command = False
            for prefix in self.bot.command_prefix:
                flag_command = True
                # コマンド分にゴミ箱追加
                if "".join(content[0 : len(prefix)]) == prefix:
                    await ms.add_reaction("🗑")
                return
            if not(flag_command):
                # コマンド文ではなかったとき
                pass


def setup(bot):
    return bot.add_cog(On_Message(bot))
