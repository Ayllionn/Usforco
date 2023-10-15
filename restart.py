import os
from platform import system
from Bot import bot

if system() == "Windows":
    system = "win"
else:
    system = "lin"
    try:
        with open("os_conf", "r+", encoding="utf8") as f:
            terminal = f.read()

    except:
        terminal = input(
            "Vue que vous êtes sous linux veuillez indiquer la commande qui permet de lancer votre terminal (exemple sous mate : mate-terminal) :")
        with open("os_conf", "w+", encoding="utf8") as f:
            f.write(terminal)


if system == "win":
    os.system("start start.py")
else:
    os.system(f"{terminal} -e python3 'start.py' &")