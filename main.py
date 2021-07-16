from file_io.file_io_s3 import json_io_s3 as jis
from bot_define import MyBot
from pathlib import Path


if __name__ == "__main__":
    bot = MyBot()
    extention_folder = "MyExtension"
    for f in Path(extention_folder).glob("*.py"):
        bot.load_extension(f"{extention_folder}.{f.stem}")
    bot.run(bot.dict_setup["TOKEN"])
