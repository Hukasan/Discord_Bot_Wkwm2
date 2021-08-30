from discord import Embed, Message, PartialMessage

from datetime import datetime
from MyFunctions.methods import dainyu
from copy import copy
from emoji import UNICODE_EMOJI
from MyFunctions.gen_hash import MyHash

"""
    embed作成、送信
"""

bottom_action_down = "🔽"
bottom_action_up = "🔼"
myhash = MyHash()


class MyEmbed():
    """
    embed作成、送信
    """
    __ch_target = None
    __id_guild = str()
    __id_channel = str()
    __id = str()
    __attr = str()
    args = list()
    __ctx = None
    __bot = None
    __mode = False
    __color = int()  # カラーコード(16進)
    __pict = False  # 大きめのアイコン画像を表示させるかどうか
    __greet = str()
    __obj = None
    __mention_author = False
    __mention_str = str()

    __title = str()  # タイトル
    __text_main = str()
    __sum_line = int()
    __fields = list()

    __text_h = str()  # ヘッダー文
    __icon_h = str()  # ヘッダー画像url
    __text_f = str()  # フッター文
    __footer_arg = str()
    __icon_f = str()  # フッター画像url

    __no_page = 1  # ページ数

    __btm_up = dict()
    __btm_down = dict()

    __time = False
    __dustbox = True

    __image_url = dict()
    __video = dict()

    def __init__(self, ctx=None):
        # 内部
        self.__ch_target = None
        self.__bot = None
        self.__ctx = None
        if ctx:
            self.__ctx = ctx
            self.__bot = ctx.bot
            self.__id_guild = str(ctx.guild.id)
            self.__id_channel = str(ctx.channel.id)
        self.__mention_author = False

        # id
        self.__id = myhash.gen()
        self.__id_guild = str()
        self.__id_channel = str()
        self.__attr = str()
        self.args = list()
        self.__color = 0x00FF00  # 色
        # ヘッダー
        self.__text_h = str()  # ヘッダー文
        self.__icon_h = str()  # ヘッダー画像url
        # 本文
        self.__mention_str = str()
        self.__greet = str()
        self.__title = str()  # タイトル
        self.__pict = False  # 大きめのアイコン画像を表示させるかどうか
        self.__text_main = str()
        self.__fields = list()
        self.__video = dict()
        self.__image_url = dict()

        # フッター
        self.__time = False
        self.__text_f = str()  # フッター文
        self.__icon_f = str()  # フッター画像url

        # ボタン
        self.__btm_up = dict()
        self.__btm_down = dict()
        self.__dustbox = True

    def setTarget(self, ctx=None, bot=None, id_guild=str(), id_chanell=str()):
        if ctx:
            self.__ctx = ctx
            if id_guild:
                self.__id_guild = id_guild
            else:
                self.__id_guild = str(ctx.guild.id)
        if bot:
            self.__bot = bot
        return self

    def change(
        self,
        ch_target=None,
        attr=str(),
        args=list(),
        btm_up=None,
        btm_down=None,
        color=None,
        dustbox=None,
        mention_str=str(),
        mention_author=None,
        greet=str(),
        text_main=None,
        text_h=str(),
        text_f=str(),
        time=None,
        title=None,
        url=str(),
        pict=False,
        icon_h=None,
        icon_f=str(),
        image_url=None,
        video=None,
    ):
        keys_local = list(locals().keys())
        for key in keys_local:
            if key:
                if (not (key in ["self"])) and (f"_MyEmbed__{key}" in vars(self)):
                    try:
                        exec(f"self.__{key}=dainyu({key},self.__{key})")
                    except Exception:
                        pass
        self.args = dainyu(args, self.args)

    def setCtx(self, ctx=None, bot=None):
        if ctx:
            self.__ctx = dainyu(ctx, self.__ctx)
        if bot:
            self.__bot = bot
        elif self.__ctx:
            self.__bot = self.__ctx.bot
        return self

    def setBot(self, bot):
        self.__bot = bot
        return self

    def add(self, name: str, value: str, inline=False) -> None:
        self.__fields.append({"name": name, "value": value, "inline": inline})

    def clone(self, ctx=None) -> classmethod:
        temp = self
        temp.setCtx(ctx)
        return temp

    def footer_arg_add(self, value: str):
        if self.__footer_arg:
            self.__footer_arg = self.__footer_arg + " " + value
        else:
            self.__footer_arg = value

    def gen_embed_page(self) -> Embed:
        temp = self.clone()
        temp.desc = str()
        temp.fields = dict()

    def add_page(self, embed_page=None, no=int()):
        if self.__bot.pages.get(self.__ctx.message.id):
            self.__bot.pages[self.__ctx.message.id].append(self)
        else:
            self.__bot.pages.update({self.__ctx.message.id: [self]})

    async def sendEmbed(self, ch_target=None) -> Message:
        """
        embed送信
        """
        mode = str()
        if self.__mention_str:
            self.__greet = self.__mention_str + self.__greet
        elif bool(self.__mention_author) & bool(self.__ctx):
            self.__greet = self.__ctx.author.mention + self.__greet
        if self.__attr:
            mode = self.__attr[0]
        elif bool(mode) & bool(self.__ctx):
            if self.__ctx.author.id == self.__bot.user.id:
                user = self.__ctx.message.mentions[0]
                if user:
                    self.__greet = user.mention + self.__greet
            else:
                self.__greet = self.__ctx.author.mention + self.__greet
        embed = await self.__export_embed()
        if self.__ch_target:
            ch_target = self.__ch_target
        elif self.__ctx:
            ch_target = self.__ctx.channel
        if ch_target:
            ms = await ch_target.send(embed=embed, content=self.__greet)
            for b in self.__btm_up.keys():
                await ms.add_reaction(b)
            self.__bot.ms_dict.update(
                {ms.id: [self.__bottom_down, self.__bottom_up, bottom_action_up, bottom_action_down]})
            if self.__btm_down.keys():
                await ms.add_reaction(bottom_action_down)
            if self.__dustbox:
                await ms.add_reaction("🗑")
            return ms
        else:
            return None

    async def __export_embed(self) -> Embed:
        """
        embed生成

        Returns:
            Embed: 生成したembed
        """

        config = dict()
        config["color"] = self.__color
        config["title"] = dainyu(self.__title)
        config["desc"] = dainyu(self.__text_main)
        config["fields"] = self.__fields
        config["video"] = self.__video

        bot_info = await self.__bot.application_info()

        if self.__time:
            if isinstance(self.__time, bool):
                config["timestamp"] = (
                    ((self.__ctx.message.created_at).isoformat()) if self.__ctx else (
                        (datetime.utcnow()).isoformat())
                )
            else:
                config["timestamp"] = self.__time.isoformat()
        if (bool(self.__text_f)) or (bool(self.__footer_arg)):
            config["footer"] = {
                "text": f"{self.__text_f}{'@'+self.__footer_arg if self.__footer_arg else ''}"}
            if isinstance(self.__icon_f, str):
                config["footer"]["icon_url"] = str(self.__icon_f)
            elif bool(bot_info) & (isinstance(self.__icon_f, bool)) & bool(self.__icon_f):
                config["footer"]["icon_url"] = str(bot_info.icon_url)

        if ((bool(self.__bot)) & self.__pict) & (bool(bot_info)):
            config["pict"] = {"url": str(bot_info.icon_url)}

        if self.__text_h:
            config["author"] = {"name": self.__text_h}
            if isinstance(self.__icon_h, str):
                config["author"]["icon_url"] = str(self.__icon_h)
            elif bool(bot_info) & (isinstance(self.__icon_h, bool)) & bool(self.__icon_h):
                config["author"]["icon_url"] = str(bot_info.icon_url)
        if self.__image_url:
            config["image"] = {"url": str(self.__image_url)}

        return Embed.from_dict(config)

    def import_embed(self, embed: Embed):
        gotten_dict = embed.to_dict()
        (footer, icon_f) = (
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
            desc=gotten_dict.get("desc"),
            url=gotten_dict.get("url"),
            time=gotten_dict.get("timestamp"),
            footer=footer,
            icon_f=icon_f,
            color=gotten_dict.get("color"),
            pict=gotten_dict.get("pict"),
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
            me.greet = me.mention + me.greet
        elif bool(me.mention_author) & bool(me.ctx):
            me.greet = me.ctx.author.mention + me.greet
        elif bool(me.mode) & bool(me.ctx):
            if me.ctx.author.id == me.bot.user.id:
                user = me.ctx.message.mentions[0]
                if user:
                    me.greet = user.mention + me.greet
            else:
                me.greet = me.ctx.author.mention + me.greet
        embed = await me.export_embed()
        obj = obj[0] if isinstance(me.obj, list) else me.obj
        if (not (me.obj)) & bool(me.target):
            obj = me.target
        elif me.ctx:
            obj = me.ctx.channel
        if obj:
            ms = await obj.edit(embed=embed, content=me.greet)
            for b in me.bottom_up:
                await ms.add_reaction(b)
            me.bot.ms_dict.update(
                {ms.id: [me.bottom_down, me.bottom_up, bottom_action_up, bottom_action_down]})
            if me.bottom_down:
                await ms.add_reaction(bottom_action_down)
            if me.dustbox:
                await ms.add_reaction("🗑")
        return ms


def scan_footer(embed: Embed, mode_page=False) -> list:
    return_dict = {"id": None, "args": None}
    if embed:
        flag_arg = False
        footer_dict = (embed.to_dict()).get("footer")
        if footer_dict:
            ftext = footer_dict.get("text")
            args = ftext.split(" ")
            for arg in args:
                if "ID:" in arg:
                    return_dict["uuid"] = ftext.split("ID:")[-1]
                if flag_arg:
                    return_dict["args"].append(arg)
                elif "@" in ftext:
                    return_dict["args"].append(arg.split("@")[-1])

    return return_dict
