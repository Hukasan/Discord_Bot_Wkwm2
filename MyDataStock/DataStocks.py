from MyDataStock.app.io_s3 import DS, DS_mass, DS_empty
from os import environ
from MyDataStock.MyEmbed import MyEmbed

name_project = environ["DISCORD_BOT_PROJECT_NAME"]


class DS_server(DS_empty):
    ch_ready = str()
    ch_bot = str()
    role_admin = str()
    delay_ad = int()
    enable_ad = False

    def __init__(self, id):
        super().__init__(id=id)

    def initialize(self):
        self.ch_ready = str()
        self.ch_bot = str()
        self.role_admin = str()
        self.delay_ad = 5
        self.enable_ad = False


class DS_servers(DS_mass):
    def __init__(self):
        super().__init__(name_file="data_servers", name_project=name_project, DS_empty=DS_server)

    def get(self, id) -> DS_server:
        return self.dict_DS.get(str(id))

    def write(self, server: DS_server):
        dict_data = self.io.get()
        df = dict_data.get("DEFAULT")
        if not df:
            temp_dict = dict()
            for key in vars(server).keys():
                print(key)
                if not(key in ["self", "id"]):
                    temp_dict.update({key: None})
            dict_data.update({"DEFAULT": temp_dict})
            self.io.put(dict_data)
            df = dict_data.get("DEFAULT")
        temp_dict = dict()
        for key in df.keys():
            try:
                exec(f"temp=server.{key}")
                exec("temp_dict.update({key:temp})")
            except Exception:
                continue
        if temp_dict:
            temp_dict = {server.id: temp_dict}
            dict_data.update(temp_dict)
            self.io.put(dict_data)


class DS_bot(DS):
    token = str()
    desc = str()
    prefix = list()
    links = dict()
    ad_ids = dict()

    def __init__(self):
        super().__init__(name_file="data_bot", name_project=name_project)


class Page:
    title = str()
    desc = str()
    pict = str()  # thumbnail_url
    fields = list()

    def __init__(self, title=str(), desc=str(), pict=str(), fields=list()):
        self.title = title
        self.desc = desc
        self.pict = pict
        self.fields = fields

    def output(self):
        return {"title": self.title, "desc": self.desc, "pict": self.pict, "fields": self.fields}


class DS_page(DS_empty):
    pages = list()

    def __init__(self, id):
        super().__init__(id=id)

    def initialize(self):
        self.pages = list()

    def make_page(title=str(), desc=str(), pict=str(), fields=list()):
        return Page(title, desc, pict, fields)

    def add_page(self, title=str(), desc=str(), pict=str(), fields=list(), page=Page()):
        if page:
            self.pages.append(page.output())
        else:
            self.pages.append(Page(title, desc, pict, fields).output())


class DS_pages(DS_mass):
    def __init__(self):
        super().__init__(name_file="data_pages", name_project=name_project, DS_empty=DS_server)

    def get(self, id) -> DS_page:
        return self.dict_DS.get(str(id))

    def write(self, page: DS_page):
        dict_data = self.io.get()
        df = dict_data.get("DEFAULT")
        if not df:
            temp_dict = dict()
            for key in vars(page).keys():
                print(key)
                if not(key in ["self", "id"]):
                    temp_dict.update({key: None})
            dict_data.update({"DEFAULT": temp_dict})
            self.io.put(dict_data)
            df = dict_data.get("DEFAULT")
        temp_dict = dict()
        for key in df.keys():
            try:
                exec(f"temp=page.{key}")
                exec("temp_dict.update({key:temp})")
            except Exception:
                continue
        if temp_dict:
            temp_dict = {page.id: temp_dict}
            dict_data.update(temp_dict)
            self.io.put(dict_data)
