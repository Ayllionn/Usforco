import os
import data_exploit
from glob import glob
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

try:
    import curses
except:
    if os_type == "win":
        os.system("pip install windows-curses")
    if os_type == "lin":
        os.system("pip install curses")
    import curses


def choice(stdscr, options: list):
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
    """Lance l'outil de recherche de la base de données"""

    try:
        while True:
            files = glob("data_exploit/database/*.json")
            choices = [f.split("\\")[-1].split("/")[-1][:-5] for f in files]

            choiced = curses.wrapper(choice, choices)
            if choiced == "! Exit !":
                break
            txt_name = choiced
            road = []

            while True:
                curent = data_exploit.get(txt_name, *road)[-1]
                if type(curent) == dict:
                    choiced = curses.wrapper(choice, [*curent.keys(), "! Back !"])
                    if choiced == "! Back !":
                        road = road[:-1]
                    elif choiced == "! Exit !":
                        break
                    else:
                        road.append(choiced)
                else:
                    choiced = curses.wrapper(choice, [f"La valeur est : {curent}", "! Back !"])
                    if choiced == "! Back !":
                        road = road[:-1]
                    elif choiced == "! Exit !":
                        break


    except ModuleNotFoundError:
        print(
            "Le module curses n est pas correctement installer veuilliez attendre 2 min que nous procédons a ça mise "
            "a jour . . .")
        if os_type == "win":
            os.system("pip install windows-curses")
        if os_type == "lin":
            os.system("sudo pip install curses")
        start()
    except Exception as e:
        print(e)
        return