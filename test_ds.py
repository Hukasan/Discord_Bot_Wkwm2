from MyDataStock.io_data_bot import Bot_DS
from MyDataStock.io_data_servers import Server_DS


ts = Server_DS(1)
ts.pull()
print(ts.ch_bot)
ts.ch_bot += 1
ts.push()
print(ts.ch_bot)
# ts.ch_ready = 2
# ts.ch_bot = 1
# ts.delay_mee6delete = 1
# ts.enable_mee6delete = False
# ts.push()
