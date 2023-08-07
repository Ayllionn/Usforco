import curses
import os
import traceback
import data_exploit
import platform
from rich.prompt import Prompt

def get_os():
    if platform.system() == "Windows":
        return "win"
    elif platform.system() == "Linux":
        return "lin"
    else:
        # Si le système d'exploitation n'est ni Windows ni Linux
        return None

os_type = get_os()
error = False


def raw(os_name):
    with open(f"{os.getcwd()}/libs/{os_name}", "r+", encoding="utf8") as file:
        libs = file.read().split('\n')
        for l in libs:
            os.system(f"pip install {l}")

def module():
    try:
        import rich
        import discord
        import curses
    except ModuleNotFoundError:
        if error:
            traceback.print_exc()
            print("\n\n\n\n\n Nous avons une erreur du au import mais il est impossible pour nous de la règlé veuilliez"
                  " checker les libs pour savoir les libs que normalement le programme a besoin et si besoin"
                  " les reinstaller\n"
                  "Sinon veuilliez regarder les libs qu'on besoin vos programmes que vous avez ajouté !")
            input("Press enter to end")
            quit()

        raw(os_type)

        module()
module()
from Term import CustomTerminal

"""
{
  "log_channel": 123,
  "token": "token"
}
"""

def selecteur(stdscr:curses.window, options: list):
    curses.curs_set(0)
    stdscr.nodelay(1)

    options.append("! Exit !")
    selected_option = 0

    while True:
        stdscr.clear()

        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(f"> {option}\n")
            else:
                stdscr.addstr(f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
            selected_option += 1
        elif key == ord('\n'):
            break

    return options[selected_option]

def start():
    """
    permet de démarrer le bot
    :return: None
    """
    if os_type == 'win':
        os.system('start starter.py')
    else:
        print("Due au fait que notre chère système linux ")

def config():
    """
    permet de config le bot
    :return: None
    """
    if data_exploit.get("config")[1] is None:
        data = {
            "token":input("Mettre le token du bot :")
        }
        while True:
            try:
                log_channel = int(input("Mettre l'id du salon qui annoncera la connexion du bot :"))
                break
            except:
                print("Erreur réessayez avec un nombre valide")
        while True:
            print('D\'autre options ?')
            choice = input("[o/n]")
            if choice.lower() == "o":
                while True:
                    choices = [*data.keys(), "! add list !", "! add str !", "! add int !"]
                    choiced = curses.wrapper(selecteur, choices)

                    if choiced == "! Exit !":
                        break
                    elif choiced == "! add list !":
                        temp = []
                        key = input("Nom de la clé pour accédé a votre list :")
                        while True:
                            ch = Prompt.ask(
                                "Qu ajouté vous a cette list ?",
                                choices=["int", "str", "exit"]
                            )
                            if ch == 'int':
                                try:
                                    entry = input(":>>>")
                                    temp.append(int(entry))
                                except:
                                    try:
                                        temp.append(float(entry))
                                    except:
                                        print("ERREUR : ceci contien des caractère non décimaux")
                            if ch == 'str':
                                temp.append(input(">>>:"))
                            if ch == "exit":
                                break

                        data.update(
                            {
                                key:temp
                            }
                        )
                    elif choiced == "! add str !":
                        key = input("Nom de la clé pour accédé a votre objet str :")
                        strr = input("Votre objet str :")
                        data.update(
                            {
                                key:strr
                            }
                        )
                    elif choiced == "! add int !":
                        key =  input("Nom de la clé pour accédé a votre objet int :")
                        try:
                            intt = input("Votre objet int :")
                            intt = int(intt)
                        except:
                            try:
                                intt = float(intt)
                            except:
                                print("CE N EST PAS UN CHIFFRE !")

                        data.update(
                            {
                                key:intt
                            }
                        )
                    else:
                        while True:
                            choices = [data.get(choiced)]
                            choiced = curses.wrapper(selecteur, choices)
                            if choiced == "! Exit !":
                                break
            else:
                print("Ok on reste sur la config de base")
                break

        data.update({"log_channel": log_channel})
        data_exploit.update("config", **data)
    else:
        data = data_exploit.get("config")[-1]

        print("Voici la config")
        for k, v in data.items():
            print(f"{k} = {v}\ntype de v : {type(v)}")

        print('')
        print("chemin d'accès :")
        print(f"{os.getcwd()}/data_exploit/database/config.json")

console = CustomTerminal(terminal_name="Bot controleur and tools", search="n", panel=False,
                         start=start,
                         config=config)

console.get_raw_cmds_files(f"{os.getcwd()}/term_tools")

if __name__ == '__main__':
    console.start()