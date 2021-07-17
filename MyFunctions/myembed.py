from discord import Embed, Message, PartialMessage

from datetime import datetime
from MyFunctions.methods import dainyu
from copy import copy
from emoji import UNICODE_EMOJI

"""
    embed作成、送信
"""

bottom_action_down = "🔽"
bottom_action_up = "🔼"


class MyEmbed:
    """
    embed作成、送信
    """

    def __init__(self, ctx=None):

        self.ctx = ctx
        self.bot = ctx.bot if ctx else None
        self.target = ctx.channel if ctx else None
        self.obj = None
        self.mention = str()
        self.mention_author = False
        self.help_mode = False
        self.title = str()  # タイトル
        self.color = 0x00FF00  # 色
        self.thumbnail = False  # 大きめのアイコン画像を表示させるかどうか
        self.footer = str()  # フッター文
        self.footer_arg = str()
        self.footer_icon = str()  # フッター画像url
        self.header = None  # ヘッダー文
        self.header_icon = str()  # ヘッダー画像url
        self.fields = list()
        self.description = str()
        self.descriptions = list()
        self.line_number = int(0)
        self.greeting = str()
        self.time = False
        self.dust = True
        self.footer_arg = str()
        self.bottom_up = list()
        self.bottom_down = list()
        self.args_bottom_down = list()
        self.args_bottom_upper = list()
        self.image_url = dict()
        self.video = dict()

    def setTarget(self, target, bot=None):
        self.target = target
        if bot:
            self.bot = bot
        return self

    def change(
        self,
        time=None,
        mention=str(),
        mention_author=None,
        title=None,
        color=None,
        url=str(),
        description=None,
        thumbnail=False,
        header=str(),
        header_icon=None,
        footer=str(),
        footer_icon=str(),
        greeting=str(),
        footer_arg=str(),
        dust=None,
        bottom_up=list(),
        bottom_down=list(),
        args_bottom_down=None,
        args_bottom_upper=None,
        image_url=None,
        video=None,
        help_mode=None,
    ):
        """
        設定書き換え
        """
        self.color = dainyu(color, self.color)
        self.thumbnail = dainyu(thumbnail, self.thumbnail)
        self.header = dainyu(header, self.header)
        self.header_icon = dainyu(header_icon, self.header_icon)
        self.footer = dainyu(footer, self.footer)
        self.title = dainyu(title, self.title)
        self.greeting = dainyu(greeting, self.greeting)
        self.description = dainyu(description, self.description)
        self.footer_arg = dainyu(footer_arg, self.footer_arg)
        self.bottom_down = dainyu(bottom_down, self.bottom_down)
        self.bottom_up = dainyu(bottom_up, self.bottom_up)
        self.args_bottom_down = dainyu(args_bottom_down, self.args_bottom_down)
        self.args_bottom_upper = dainyu(
            args_bottom_upper, self.args_bottom_upper)
        self.time = dainyu(time, self.time)
        self.mention_author = dainyu(mention_author, self.mention_author)
        self.image_url = dainyu(image_url, self.image_url)
        self.video = dainyu(video, self.video)
        self.dust = dainyu(dust, self.dust)
        self.help_mode = dainyu(help_mode, self.help_mode)

    def setCtx(self, ctx=None, bot=None):
        if ctx:
            self.ctx = dainyu(ctx, self.ctx)
        if bot:
            self.bot = bot
        elif self.ctx:
            self.bot = self.ctx.bot
        return self

    def setBot(self, bot):
        self.bot = bot
        return self

    def __cut(self, obj: str):
        point = 50
        if isinstance(obj, str):
            if len(obj) > point:
                ex = f"{obj[:point+1]}\n"
                ex = ex + (self.__cut(obj[point + 1 :]))
            else:
                ex = f"{obj}\n"
        else:
            ex = "TextError"
        return ex

    def __export_complist(self, obj):
        ex = list()
        lines = 0
        if isinstance(obj, str):
            obj = obj.splitlines()
        if isinstance(obj, list):
            temp = list()
            for o in obj:
                temp.extend(o.splitlines())
            obj = temp
            for o in obj:
                content = self.__cut(o)
                line = len(content)
                # print(f"{o},{line}")
                while line > 0:
                    if (line + lines) > 10:
                        if ex:
                            ex[-1] = ex[-1] + content[: 15 - lines + 1]
                        else:
                            ex.append(content[: 15 - lines + 1])
                        content = content[15 - lines + 1 :]
                        lines = 0
                        line = line - 15 + lines - 1
                    else:
                        if ex:
                            ex[-1] = ex[-1] + content
                        else:
                            ex.append(content)
                        line = 0
        return ex

    def default_embed(self) -> classmethod:
        """
        embed初期化
        Returns:
            このクラス
        """
        return self

    def add(self, name: str, value: str, inline=False, greeting=str(), description=str()) -> None:
        if greeting:
            self.greeting = greeting
        self.description = description if description else self.description
        self.fields.append({"name": name, "value": value, "inline": inline})

    def clone(self, ctx=None) -> classmethod:
        temp = self
        temp.setCtx(ctx)
        return temp

    def footer_arg_add(self, value: str):
        if self.footer_arg:
            self.footer_arg = self.footer_arg + " " + value
        else:
            self.footer_arg = value

    def add_page(
        self,
        time=None,
        mention=str(),
        mention_author=None,
        title=None,
        color=None,
        url=str(),
        description=None,
        thumbnail=False,
        header=str(),
        header_icon=None,
        footer=str(),
        footer_icon=str(),
        greeting=str(),
        footer_arg=str(),
        dust=None,
        bottom_up=list(),
        bottom_down=list(),
        args_bottom_down=None,
        args_bottom_upper=None,
        image_url=None,
        video=None,
        help_mode=None,
    ):
        new_embed = copy(self)
        new_embed.change(
            time=time,
            mention=mention,
            mention_author=mention_author,
            title=title,
            color=color,
            url=url,
            description=description,
            thumbnail=thumbnail,
            header=header,
            header_icon=header_icon,
            footer=footer,
            footer_icon=footer_arg,
            greeting=greeting,
            footer_arg=footer_arg,
            dust=dust,
            bottom_up=bottom_up,
            bottom_down=bottom_down,
            args_bottom_down=args_bottom_down,
            args_bottom_upper=args_bottom_upper,
            image_url=image_url,
            video=video,
            help_mode=help_mode,
        )
        if self.bot.pages.get(self.ctx.message.id):
            self.bot.pages[self.ctx.message.id].append(self)
        else:
            self.bot.pages.update({self.ctx.message.id: [self]})

    async def sendEmbed(self, obj=None) -> Message:
        """
        embed送信
        """
        if self.mention:
            self.greeting = self.mention + self.greeting
        elif bool(self.mention_author) & bool(self.ctx):
            self.greeting = self.ctx.author.mention + self.greeting
        elif bool(self.help_mode) & bool(self.ctx):
            if self.ctx.author.id == self.bot.user.id:
                user = self.ctx.message.mentions[0]
                if user:
                    self.greeting = user.mention + self.greeting
            else:
                self.greeting = self.ctx.author.mention + self.greeting
        embed = await self.export_embed()
        obj = obj[0] if isinstance(self.obj, list) else self.obj
        if (not (self.obj)) & bool(self.target):
            obj = self.target
        elif self.ctx:
            obj = self.ctx.channel
        if obj:
            ms = await obj.send(embed=embed, content=self.greeting)
            for b in self.bottom_up:
                await ms.add_reaction(b)
            self.bot.ms_dict.update(
                {ms.id: [self.bottom_down, self.bottom_up, bottom_action_up, bottom_action_down]})
            if self.bottom_down:
                await ms.add_reaction(bottom_action_down)
            if self.dust:
                await ms.add_reaction("🗑")
        return ms

    async def export_embed(self) -> Embed:
        """
        embed生成

        Returns:
            Embed: 生成したembed
        """

        config = dict()
        config["color"] = self.color
        config["title"] = dainyu(self.title)
        config["description"] = dainyu(self.description)
        config["fields"] = self.fields
        config["video"] = self.video

        bot_info = await self.bot.application_info()

        if self.time:
            if isinstance(self.time, bool):
                config["timestamp"] = (
                    ((self.ctx.message.created_at).isoformat()) if self.ctx else (
                        (datetime.utcnow()).isoformat())
                )
            else:
                config["timestamp"] = self.time.isoformat()
        if (bool(self.footer)) or (bool(self.footer_arg)):
            config["footer"] = {
                "text": f"{self.footer}{'@'+self.footer_arg if self.footer_arg else ''}"}
            if isinstance(self.footer_icon, str):
                config["footer"]["icon_url"] = str(self.footer_icon)
            elif bool(bot_info) & (isinstance(self.footer_icon, bool)) & bool(self.footer_icon):
                config["footer"]["icon_url"] = str(bot_info.icon_url)

        if ((bool(self.bot)) & self.thumbnail) & (bool(bot_info)):
            config["thumbnail"] = {"url": str(bot_info.icon_url)}

        if self.header:
            config["author"] = {"name": self.header}
            if isinstance(self.header_icon, str):
                config["author"]["icon_url"] = str(self.header_icon)
            elif bool(bot_info) & (isinstance(self.header_icon, bool)) & bool(self.header_icon):
                config["author"]["icon_url"] = str(bot_info.icon_url)
        if self.image_url:
            config["image"] = {"url": str(self.image_url)}

        return Embed.from_dict(config)

    def import_embed(self, embed: Embed):
        gotten_dict = embed.to_dict()
        (footer, footer_icon) = (
            (gotten_dict["footer"].get("text"),
             gotten_dict["footer"].get("icon_url"))
            if gotten_dict.get("footer")
            else (
                None,
                None,
            )
        )
        self.change(
            title=gotten_dict.get("title"),
            description=gotten_dict.get("description"),
            url=gotten_dict.get("url"),
            time=gotten_dict.get("timestamp"),
            footer=footer,
            footer_icon=footer_icon,
            color=gotten_dict.get("color"),
            thumbnail=gotten_dict.get("thumbnail"),
            image_url=gotten_dict.get("image").get(
                "url") if gotten_dict.get("image") else None,
            video=gotten_dict.get("video"),
        )


def edit_embed(me: MyEmbed, page):
    async def sendEmbed(self, obj=None) -> Message:
        """
        embed送信
        """
        if me.mention:
            me.greeting = me.mention + me.greeting
        elif bool(me.mention_author) & bool(me.ctx):
            me.greeting = me.ctx.author.mention + me.greeting
        elif bool(me.help_mode) & bool(me.ctx):
            if me.ctx.author.id == me.bot.user.id:
                user = me.ctx.message.mentions[0]
                if user:
                    me.greeting = user.mention + me.greeting
            else:
                me.greeting = me.ctx.author.mention + me.greeting
        embed = await me.export_embed()
        obj = obj[0] if isinstance(me.obj, list) else me.obj
        if (not (me.obj)) & bool(me.target):
            obj = me.target
        elif me.ctx:
            obj = me.ctx.channel
        if obj:
            ms = await obj.edit(embed=embed, content=me.greeting)
            for b in me.bottom_up:
                await ms.add_reaction(b)
            me.bot.ms_dict.update(
                {ms.id: [me.bottom_down, me.bottom_up, bottom_action_up, bottom_action_down]})
            if me.bottom_down:
                await ms.add_reaction(bottom_action_down)
            if me.dust:
                await ms.add_reaction("🗑")
        return ms


def scan_footer(embed: Embed, mode_page=False) -> list:
    footer = str()
    arg = list()
    return_list = list
    if embed:
        footer = (embed.to_dict()).get("footer")
        if footer:
            text = footer.get("text")
            if "pp." in text and mode_page:
                return_list = [int(p)
                               for p in (text.split("pp.")[1]).split("/")]
                text = text.split("pp.")[0]

            elif "@" in text:
                arg = text.split("@")[-1]
                return_list = arg.split(" ")

    return return_list
