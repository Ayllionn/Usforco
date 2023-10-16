import os
from CustomTerm import CustomTerminal
from platform import system

try:
    from conf.bot import *
except ModuleNotFoundError:
    print("1er demarrage lancement de la commande de config")
    from commandes.conf import start
    start()
    import restart

if __name__ == '__main__':
    term = CustomTerminal("Bot manager", "o", panel=False, help_at_start=True)
    term.get_raw_cmds_files(f"{os.getcwd()}/commandes")
    term.start()