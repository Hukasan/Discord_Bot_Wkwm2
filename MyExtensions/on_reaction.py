from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Emoji,
)
from discord.ext.commands import Cog, Bot, Context
from discord.abc import GuildChannel, PrivateChannel
from MyFunctions.myembed import MyEmbed, scan_footer, edit_embed
from os.path import splitext

# from datetime import datetime
# from pytz import utc
# from Cogs.app.MakeEmbed import MakeEmbed


class ReactionEvent(Cog, name="ReactionEvent"):
    """
    リアクションに対しての処理
    次に行う処理をbot.configにかんすうごと保存し、ここで呼び出す
    識別はembedのフッターを利用している(myembed.scan_footer)
    era:embed_reaction_action
    """

    qualified_name = "hide"

    def __init__(self, bot: Bot):
        self.bot = bot

    async def do_era(self, usr_id: int, ms: Message, react: str, arg: list) -> bool:
        usr = self.bot.get_user(usr_id)
        func = None
        if react == "🗑":
            if usr in ms.mentions:
                await ms.delete()
            return
        ms_list = self.bot.ms_dict.get(ms.id)
        if len(ms_list) >= 4:
            # down
            if react == ms_list[3]:
                await ms.clear_reactions()
                await ms.add_reaction(ms_list[2])
                for b in ms_list[0]:
                    await ms.add_reaction(b)
                await ms.add_reaction("🗑")
                return
            # up
            elif react == ms_list[2]:
                await ms.clear_reactions()
                await ms.add_reaction(ms_list[3])
                for b in ms_list[1]:
                    await ms.add_reaction(b)
                await ms.add_reaction("🗑")
                return
                if len(ms_list) >= 7:
                    page = scan_footer(ms.embeds[0], mode_page=True)
                    if react == ms_list[5]:
                        if not (page[0] <= 0):
                            edit_embed(self.bot.pages.get(ms.id).index(page[0] - 1), page=page[0])
                        pass
                    elif react == ms_list[6]:
                        pass
        if arg:
            func = self.bot.funcs.get(arg[0])
            if func:
                ctx = await self.bot.get_context(ms)
                return await func(self.bot, usr_id, ctx, react, arg[1:])

    @Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        emoji = str(rrae.emoji)

        if bool(channel) & bool(emoji) & bool(usr):
            if usr.bot:
                return
            ms = await channel.fetch_message(id=rrae.message_id)
            if ms.author == self.bot.user:
                if ms.embeds:
                    for embed in ms.embeds:
                        await self.do_era(
                            usr_id=rrae.user_id,
                            ms=ms,
                            react=emoji,
                            arg=scan_footer(embed=embed),
                        )
                else:
                    if emoji == "🗑":
                        for r in ms.reactions:
                            if (r.emoji == emoji) & (r.me):
                                if ms.author == usr:
                                    await ms.delete()
                                    return
                    pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))
