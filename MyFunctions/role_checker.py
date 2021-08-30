from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Guild,
    Emoji,
    Role,
    User,
)
from discord.ext.commands import Cog, Bot, Context, check
from discord.abc import GuildChannel, PrivateChannel

from MyDataStock.DataStocks import DS_servers


async def isroleupper(role_id: int, user: Member, guild: Guild, ignore_same=True) -> bool:
    """
    check
    ユーザがそのロールを超えるロールを持っているかどうかを判断します
    """
    member = guild.get_member(user_id=int(user.id))
    comp_role = guild.get_role(int(role_id))
    guild_role_list = guild.roles
    comp_index = guild_role_list.index(comp_role)
    if comp_index < guild_role_list.index(member.top_role):
        return True
    elif (comp_index == guild_role_list.index(member.top_role)) & (bool(ignore_same)):
        return True
    else:
        return False


def check_role_is_upper_member():
    """
    権限ロール以上のロールをユーザが持っているかを判定
    """

    async def predicate(ctx: Context):
        ds = DS_servers().get(ctx.guild.id)
        role_admin = ds.role_admin
        if role_admin:
            return await isroleupper(
                role_id=role_admin,
                user=ctx.author,
                guild=ctx.guild,
            )
        else:
            return False

    return check(predicate)
