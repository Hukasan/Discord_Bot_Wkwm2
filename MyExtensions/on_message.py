from discord import Message
from discord.ext import commands


class On_Message(commands.Cog):
    """
    会話干渉機能
    """

    qualified_name = "hide"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ms: Message):
        if ms.author.bot:
            # MEE6 Delete
            if int(ms.author.id) == (self.bot.setup.get("MEE6_ID")) and ms.mentions:
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
                return
        else:
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
