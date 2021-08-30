from bot_define import MyBot

if __name__ == "__main__":
    wkwm2 = MyBot()
    print(wkwm2.ds_bot.token)
    print(f"run with {wkwm2.name_project}")
    wkwm2.run(wkwm2.ds_bot.token)
