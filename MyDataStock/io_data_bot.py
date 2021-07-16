
from MyDataStock.app import io_s3


class Bot_DS:
    token = str()

    def __init__(
        self,
    ):
        self.io = io_s3.json_io_s3("data_bot")

    def push(self):
        if self.token:
            token = self.token
        for (symbol, value) in locals().items():
            self.io.put({symbol: value})

    def pull(self):
        token = self.token
        ite_temp = list(locals().keys())
        for symbol in ite_temp:
            dict_data = self.io.get()
            locals()[symbol] = dict_data.get(symbol)
        self.token = token
