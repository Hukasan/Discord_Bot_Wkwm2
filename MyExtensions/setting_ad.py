from discord import Guild
from discord.ext.tasks import loop
from discord.ext.commands import (
    Bot,
    Context,
    command,
    is_owner,
    Group,
    Command,
    group,
)
from MyExtensions.app.MyCog import MyCog
from MyFunctions.role_checker import check_role_is_upper_member as role_check

from MyDataStock.DataStocks import DS_servers


class ADSetting(MyCog):
    """
    自動削除機能(AD)設定
    """
    categoly_parent = "subsetting"
    qualified_name = "ADSetting"

    def __init__(self, bot: Bot):
        self.bot = bot

    @group()
    @role_check()
    async def autodel(self, ctx: Context,):
        pass

    @autodel.command(description="消すまでの秒数を設定")
    async def time(self, ctx: Context, second):
        """
        消すまでの秒数を設定します
        Args:
            second (整数): [設定秒数]
        """
        second = int(second)
        return

    @autodel.command(description="削除機能のON/OFF")
    async def togle(self, ctx: Context):
        ds_sers = DS_servers()
        ds_ser = ds_sers.get(ctx.guild.id)
        ds_ser.enable_ad = not(ds_ser.enable_ad)
        ds_sers.write(ds_ser)
        await ctx.send(f"AutoDelete機能を{ds_ser.enable_ad}にしました")


def setup(bot: Bot):
    return bot.add_cog(ADSetting(bot))
