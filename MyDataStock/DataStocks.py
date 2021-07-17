from MyDataStock.app.io_s3 import DS, DS_mass, DS_empty
from os import environ

name_project = environ["DISCORD_BOT_PROJECT_NAME"]


class DS_server(DS_empty):
    ch_ready = int()
    ch_bot = int()
    delay_mee6delete = int()
    enable_mee6delete = bool()

    def __init__(self, id):
        super().__init__(id=id)

    def initialize(self):
        self.delay_mee6delete = 5
        self.enable_mee6delete = False


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
                if not(key in ["self"]):
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
        temp_dict = {server.id: temp_dict}
        dict_data.update(temp_dict)
        self.io.put(dict_data)


class DS_bot(DS):
    token = None
    desc = str()
    prefix = list()

    def __init__(self):
        super().__init__(name_file="data_bot", name_project=name_project)
