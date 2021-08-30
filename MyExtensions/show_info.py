from discord import Guild
from discord.ext.commands import (
    Bot,
    Context,
    command,
    is_owner,
    Group,
    Command,
    group,
)
from bot_define import MyBot
from MyExtensions.app.MyCog import MyCog
from MyDataStock.MyEmbed import MyEmbed


class BotInfo(MyCog):

    qualified_name = "BotInfo"

    def __init__(self, bot: MyBot):
        self.bot = bot

    @command()
    async def info_bot(self, ctx: Context):
        opt = MyEmbed(ctx=ctx)
        opt.change(mention_author=True, title="BotInfo", thumbnail=True, description=self.bot.ds_bot.desc)
        opt.add(name="もろもろ", value=None, inline=True)

        opt.add(name="リンク", value=str(f"Github : {ctx.ds_bot.links.get('GitHub')}\r" f"Support : {ctx.ds_bot.links.get('SupportServer')}"))


def setup(bot: MyBot):
    return bot.add_cog(BotInfo(bot))
