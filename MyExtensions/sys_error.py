from discord import Emoji, Message
from discord.ext.commands import (
    Bot,
    Context,
    HelpCommand,
    command,
    is_owner,
    Group,
    Command,
)
from discord.ext.commands.errors import (
    CommandNotFound,
    CommandError,
    MissingRequiredArgument,
    NotOwner
)
from MyDataStock.MyEmbed import MyEmbed
from MyFunctions.inputassist import hyokiyure
from bot_define import MyBot
from MyExtensions.app.MyCog import MyCog

EMBED_IDENTIFIER = "ERROR_CMD_HELP"
E_CH_REACTION_ACCEPT = "ð"


async def era_e_ch(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    if str(react) == E_CH_REACTION_ACCEPT:
        target = arg[1]
        await ctx.send_help(target)
        await ctx.message.delete()
    else:
        pass


class OutputError(MyCog):

    def __init__(self, bot: MyBot):
        self.bot = bot
        self.owner = None
        self.__error_title = "ã³ãã³ãå®è¡æã¨ã©ã¼"
        self.__error_fotter = "BotError"
        self._database_error = "ãã¼ã¿å¤æ´ã«ã¨ã©ã¼ãããã¾ãã\rä»å®è¡ããå¦çã¯è¡ãªãã¾ããã§ããã"
        self.__undefine_error_title = "æ³å®å¤ã®ã¨ã©ã¼"
        self.__notice_owner_message_base = "ãããä¸»ã«ééãã¾ã.."
        self.__notice_owner_message = self.__notice_owner_message_base
        self.__missing_arg_message = "ãã®ã³ãã³ãã«å¿è¦ãªè¦ç´ æå®ãè¶³ãã¦ãã¾ãã\r" "ã³ãã³ãã®è©³ç´°ãè¡¨ç¤ºãã¾ããï¼"
        self.__permission_message = "ð¢æ¨©éãè²´æ¹ã«ããã¾ãã\rç®¡çèã¾ã§åãåãããã ãã"

    @MyCog.listener()
    async def on_command_error(self, ctx: Context, error):
        cmd = str()
        embed = MyEmbed(ctx)
        self.owner = self.bot.get_user(self.bot.owner_id)
        if self.owner:
            self.__notice_owner_message = self.owner.mention + self.__notice_owner_message_base
        try:
            embed.change(text_f=self.__error_fotter, title=self.__error_title)
            if isinstance(error, CommandNotFound):
                flag = True
                slist = hyokiyure(ctx.invoked_with, self.bot.all_commands.keys())
                for cmd in slist:
                    if cmd:
                        if isinstance(cmd, list):
                            cmd = cmd[0]
                        temp = ctx.message
                        temp.content = self.bot.command_prefix[0] + cmd
                        await self.bot.process_commands(temp)
                        flag = False
                        break
                if flag:
                    await ctx.message.add_reaction("â")
                return
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                )
                embed.change(greet=self.__notice_owner_message)
        except IndexError:
            embed.change(
                text_f=self.__error_fotter,
                title=self.__error_title,
                greet=f"{ctx.author.mention}",
                time=False,
            )
            if "required argument that is missing." in str(error):
                embed.change(
                    text_main=self.__missing_arg_message,
                    attr=[EMBED_IDENTIFIER, "missing"],
                    btm_up={E_CH_REACTION_ACCEPT: str(ctx.command)},
                )
            elif "You do not own this bot." in str(error):
                embed.change_description(self.__permission_message)
            elif "The check functions for command cmd failed." in str(error):
                embed.change_description(self.__permission_message)
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                )
                embed.change(greet=self.__notice_owner_message)
        await embed.sendEmbed()


def setup(bot: MyBot):
    bot.funcs.update(
        {
            EMBED_IDENTIFIER: era_e_ch,
        }
    )
    return bot.add_cog(OutputError(bot))
