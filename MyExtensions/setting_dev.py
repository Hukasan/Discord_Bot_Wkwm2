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
from time import sleep
from MyExtensions.app.MyCog import MyCog


class Developper(MyCog):
    """
    開発者コマンド
    """

    def __init__(self, bot: MyBot):
        self.bot = bot

    @is_owner()
    @group()
    async def dev(self, ctx: Context):
        pass

    @dev.command(aliases=["re", "lode", "l", "れ"], description="プログラムを再読み込み")
    async def load(self, ctx: Context):
        """
        プログラムを再読み込み。内部データは初期化される
        """
        for extension in list(self.bot.extensions):
            self.bot.reload_extension(f"{extension}")
            print(f"{extension}:is_reloted")
        print("再読み込み完了")
        await ctx.message.add_reaction("☑")

    @dev.command(aliases=["あっぷでーと", "あぷで"], description="ループさせている処理を実行")
    async def update(self, ctx: Context):
        await self.bot.loop_update()
        await ctx.message.add_reaction("☑")


def setup(bot: MyBot):
    return bot.add_cog(Developper(bot))
