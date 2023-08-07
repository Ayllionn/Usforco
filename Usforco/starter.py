try:
    from traceback import print_exc
    import os
    import time
    from bot.constructeur import bot
    import platform

    def get_os():
        if platform.system() == "Windows":
            return "win"
        elif platform.system() == "Linux":
            return "lin"
        else:
            # Si le système d'exploitation n'est ni Windows ni Linux
            return None

    os_type = get_os()

    while True:
        try:
            bot.load()
        except:
            print_exc()
            time.sleep(30)
            if os_type == "win":
                os.system("cls")
            if os_type == "lin":
                os.system("clear")
except Exception as e:
    try:
        print_exc()
    except:
        print(e)
    print("ERROR")
    input("press enter to end")