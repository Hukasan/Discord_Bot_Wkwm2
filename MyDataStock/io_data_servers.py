from MyDataStock.app import io_s3


class Server_DS:
    ch_ready = int()
    ch_bot = int()
    delay_mee6delete = int()
    enable_mee6delete = bool()

    def __init__(self, id):
        self.io = io_s3.json_io_s3("data_servers")
        self.id = id

    def push(self):
        dict_data = self.io.get()
        temp_dict = dict()
        if dict_data.get(self.id):
            for key in dict_data.get(self.id).keys():
                exec(f"temp=self.{key}")
                exec("temp_dict.update({key:temp})")
            temp_dict = {self.id: temp_dict}
        dict_data.update(temp_dict)
        self.io.put(dict_data)

    def pull(self):
        dict_data = self.io.get()
        for symbol in list(dict_data.keys()):
            exec(f"self.{symbol}={str(dict_data.get(symbol))}")
