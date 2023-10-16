import os
from CustomTerm import CustomTerminal
from platform import system

def reload():
    """restart le programme pour prendre en compte les mise a jour"""
    if system() == "Windows":
        os.system("start py manage.py")
        exit()
    else:
        input("le programme vas s'arreter relancer le pour continuer")
        exit()

try:
    from conf.bot import *
except ModuleNotFoundError:
    print("1er demarrage lancement de la commande de config")
    from commandes.conf import start
    start()
    import restart

if __name__ == '__main__':
    term = CustomTerminal("Bot manager", "o", panel=False, help_at_start=True, save=reload)
    term.get_raw_cmds_files(f"{os.getcwd()}/commandes")
    term.start()