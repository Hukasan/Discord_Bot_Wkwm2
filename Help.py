from discord import Emoji
from discord.ext.commands import Cog, Bot, HelpCommand, Group, Command, Context
import sys

from MyDataStock.MyEmbed import MyEmbed
from MyFunctions.inputassist import hyokiyure

EMBED_IDENTIFIER = "HELP_TREE"
EMBED_IDENTIFIER_ERROR = "HELP_ERROR"
BOTTOM_COMMAND_RUN = "ð¬"


class Help(HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category_name = "Help"  # ã«ãã´ãªãè¦ã¤ãããªãã£ãå ´åã®ã«ãã´ãª
        self.command_attrs["description"] = "ãã®ã¡ãã»ã¼ã¸ãè¡¨ç¤º"
        self.command_attrs["help"] = "ãã®BOTã®ãã«ãã³ãã³ãã§ãã"
        self.command_attrs["aliases"] = ["he", "herupu"]
        self.help_dict = dict()
        self.dfembed = MyEmbed()
        self.dfembed.change(
            time=True,
            attr="Help",
            mention_author=True,
        )
        self.emojis = [
            "1ï¸â£",
            "2ï¸â£",
            "3ï¸â£",
            "4ï¸â£",
            "5ï¸â£",
            "6ï¸â£",
            "7ï¸â£",
            "8ï¸â£",
            "9ï¸â£",
            "ð",
        ]

    async def create_category_tree(self, cmd, index=int(0), cmd_list=list()):
        """
        åå¸°é¢æ°ãgroupã®æä¸å±¤ã¾ã§ãæ¢ç´¢ãã
        """
        try:
            await cmd.can_run(self.context)
        except BaseException:
            print(f"ä¾å¤:{cmd.name}")
            return ""
        content = str()
        temp = str()
        underber_p = int()
        name = str()
        params = ""
        if 0 >= index:
            pass
        else:
            underber_p = cmd.name.rfind("_")
            if index != 1:
                indent = (index) * "--"
            else:
                cmd_list.append(f"{cmd.full_parent_name} {cmd.name}")
                indent = f"**{len(cmd_list)}.**"
                # indent = f"**{count}.** "
                # count += 1
                if underber_p:
                    name = f"__{cmd.name[(underber_p + 1) :]}__"
                else:
                    name = f"__{cmd.name}__"
            params = " } { ".join(cmd.clean_params.keys())
            if params:
                params = "{ " + params + " }"
            content = f"{indent}{name}  {params}\r--{cmd.description}\n"
        if isinstance(cmd, Group):
            for subcmd in cmd.walk_commands():
                if not (subcmd.name == temp):
                    content_temp, cmd_list = await self.create_category_tree(
                        cmd=subcmd, index=(index + 1), cmd_list=cmd_list
                    )
                    content += content_temp
                temp = subcmd.name
            return content, cmd_list
        elif isinstance(cmd, Command):
            return content, cmd_list

    async def send_bot_help(self, mapping):
        content = str()
        count = 0
        cog_name_list = list()
        for cog in mapping:
            cog_name = cog.qualified_name if cog else self.no_category_name

            if (cog_name in ["Help", "hide", "main"]):
                continue
            content += f"**{self.emojis[count]}{cog_name}**\r"
            count += 1
            cog_name_list.append(cog.__class__.__name__)
        self.help_dict.update({"bot": cog_name_list})
        embed = self.dfembed.clone(self.context)
        dict_btm_down = dict()
        for count, emoji in enumerate(self.emojis[:(count)]):
            dict_btm_down.update({emoji: cog_name_list[count]})
        embed.change(
            title="Help",
            text_main=str(
                f"âprifex : **{str(self.context.bot.command_prefix[0])}** \n" f"{self.context.bot.description}\n"
            ),
            btm_down=dict_btm_down
        )
        embed.add(
            name="> MainCmd",
            value=f"ã»**{self.context.prefix}help**\n--{self.command_attrs['description']}\n",
        )
        embed.add(name="> Setting", value="ãªã¢ã¯ã·ã§ã³ãæ¼ãã¦è©³ç´°è¡¨ç¤º\r" + content)
        # opt.add(name="> Invite click hereâ", value=f"{ds_bot.links.get('InviteThis')}")
        # opt.add(
        #     name=f"> Suport click hereâ",
        #     value=),
        # )
        embed.args.append("bot")
        await embed.sendEmbed()

    async def send_cog_help(self, cog: Cog):
        # embed = me.MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        temp = str()
        command_name_list = list()
        count = 1
        empty_message = str()

        if cog.walk_commands:
            for cmd in cog.walk_commands():
                if (temp != cmd.name) & (not (cmd.root_parent)):
                    if self.help_dict.get(cog.qualified_name):
                        self.help_dict[cog.qualified_name].append(cmd.name)
                    else:
                        self.help_dict.update({cog.qualified_name: [cmd.name]})

                    temp = cmd.name
                    embed.add(
                        name=f"> [{count}] {self.context.bot.command_prefix[0]}{cmd.name}",
                        value=f"{cmd.description}",
                    )
                    command_name_list.append(temp)
                    count += 1
        else:
            empty_message = "\rã³ãã³ãã¯ããã¾ãã"
        embed.change(
            header="ð Help",
            title=f"{cog.qualified_name}",
            description=f"{cog.description}{empty_message}",
            bottom_down=self.emojis[: len(command_name_list)],
            args_bottom_down=command_name_list,
        )
        embed.footer_arg_add(cog.qualified_name)
        await embed.sendEmbed()

    async def send_group_help(self, group: Group):
        embed = MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        # value = "`" + "`, `".join(group.aliases) + "`"
        tab = "|"
        value = "å¥å"
        count = 0
        for index, a in enumerate(group.aliases):
            if index == (len(group.aliases) - 1):
                value += f"{tab}{a}```"
            elif count % 4 == 0:
                if count == 0:
                    value += f"```{a}"
                    count += 1
                else:
                    value += f"{tab}{a}\r"
            elif count % 4 == 1:
                value += a
            else:
                value += tab + a
            count += 1
        if group.help:
            embed.add(name="è©³ç´°", value="```" + group.help + "```", inline=False)
        content, cmd_name_list = await self.create_category_tree(group)
        embed.add(
            name="> subcommands",
            value=content,
            inline=True,
        )
        if group.aliases:
            embed.add(
                name="> Othercall",
                value=value,
                inline=True,
            )
        prefix = self.context.prefix if self.context.prefix else self.context.bot.command_prefix[0]
        self.help_dict[group.name] = cmd_name_list

        embed.change(
            header="â(è¦ª)Help",
            title=f"{prefix} {group.name} ã³ãã³ã",
            description="__è¦ªcmdã§ãããµãcmdãå¿è¦ã§ã__",
            bottom_down=self.emojis[: len(cmd_name_list)],
            args_bottom_down=cmd_name_list,
            bottom_up=[BOTTOM_COMMAND_RUN],
        )
        embed.footer_arg_add
        await embed.sendEmbed(f"{group.name}")

    async def send_command_help(self, command: Command):
        keys = command.clean_params.keys()
        if not (keys):
            keys = ["none"]
        params = " } { ".join(keys)
        params = "{ " + params + " }"
        embed = MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        prefix = self.context.prefix if self.context.prefix else self.context.bot.command_prefix[0]
        embed.change(
            header="âHelp",
            title=(f"**{prefix}{command.full_parent_name}__{(command.name).split('_')[-1]}__ {params}**"),
            description=f"```{command.help}```",
            bottom_up=[BOTTOM_COMMAND_RUN],
        )

        if command.aliases:
            # "`" + "`, `".join(command.aliases) + "`"
            value = ""
            count = 0
            tab = " , "
            for index, a in enumerate(command.aliases):
                if index == (len(command.aliases) - 1):
                    value += f"{tab}{a}```"
                elif count % 4 == 0:
                    if count == 0:
                        value += f"```{a}"
                        count += 1
                    else:
                        value += f"{tab}{a}\r"
                elif count % 4 == 1:
                    value += a
                else:
                    value += tab + a
                count += 1
            embed.add(
                name="> å¼ã³åºãåè£",
                value=value,
                inline=True,
            )

        embed.footer_arg_add(f"{command.name}")
        await embed.sendEmbed()

    async def send_error_message(self, error):
        embed = MyEmbed(self.context)
        embed.change(header="ð¢Helpã¨ã©ã¼", greeting=f"{self.context.author.mention}", footer_arg=EMBED_IDENTIFIER_ERROR)
        slist = hyokiyure(self.context.kwargs.get("command"), self.context.bot.all_commands.keys())
        for cmd in slist:
            if cmd:
                print(cmd)
                if isinstance(cmd, list):
                    cmd = cmd[0]
                    if isinstance(cmd, list):
                        cmd = cmd[0]
                embed.change(
                    title=f"ã{cmd}ãã§ã¯ããã¾ããã?",
                    description="å®è¡ããã«ã¯ð¬ãæ¼ãã¦ãã ãã",
                    bottom_up=[BOTTOM_COMMAND_RUN],
                )
                embed.footer_arg_add(value=cmd)
                await embed.sendEmbed()
                return

        embed.change(title="ã³ãã³ããè¦ã¤ããã¾ããã§ãã", description="â¹ã§ãããã®ãã«ããè¡¨ç¤º", bottom_up="â¹")
        embed.footer_arg_add("None")
        await embed.sendEmbed()

    def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            # ããããã®ã³ãã³ãã«ãµãã³ãã³ããå­å¨ãã¦ãããªã
            return f"{command.qualified_name} ã« {string} ã¨ãããµãã³ãã³ãã¯ç»é²ããã¦ãã¾ããã"
        return f"{command.qualified_name} ã«ãµãã³ãã³ãã¯ç»é²ããã¦ãã¾ããã"


async def era_help_tree(bot: Bot, usr_id: int, ctx: Context, react: Emoji, footer_arg: list):
    help_dict = bot.help_command.help_dict
    target = str()

    for index, emoji in enumerate(bot.help_command.emojis):
        if emoji == react:
            target = help_dict[footer_arg[0]][index]
            break

    if target == "bot":
        target = None

    await ctx.send_help(target)


# def setup(bot: Bot):
#     bot.funcs.update(
#         {
#             EMBED_IDENTIFIER: era_help_tree,
#         }
#     )
