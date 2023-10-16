import os
from platform import system

def start():
    """permet de lancer le bot"""
    if system() == "Windows":
        systeme = "win"
    else:
        systeme = "lin"
        try:
            with open("cache/os_conf", "r+", encoding="utf8") as f:
                terminal = f.read()

        except:
            terminal = input(
                "Vue que vous êtes sous linux veuillez indiquer la commande qui permet de lancer votre terminal (exemple sous mate : mate-terminal) :")
            with open("cache/os_conf", "w+", encoding="utf8") as f:
                f.write(terminal)

    if systeme == "win":
        os.system("start start.py")
    else:
        os.system(f"{terminal} -e python3 'start.py' &")