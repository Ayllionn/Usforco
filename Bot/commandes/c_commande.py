import os
import platform


def start(*args):
    """permet de crée un fichier de commande pour le bot"""
    for name_module in args:
        with open(f"{os.getcwd()}/Bot/commandes/{name_module}.py", "w", encoding="utf8") as f:
            f.write('from Bot import bot\n'
                    'import discord\n'
                    'from Bot.components import *\n')
            f.write(
                "\"\"\"\nLa class bot est tout simplement votre bot\na part les décorateurs :"
                "\n> [@cmd_admin()] : qui sert a ajouté des commandes faisable que par les admins"
                "\n> [@app_cmd()] : qui sert tout simplement a ajouté des commandes a votre application\n\"\"\"\n\n\n"
            )
            f.write(
            f"# commande d'exemple\n@bot.app_cmd(name='{name_module}')\nasync def {name_module}(i):\n    \"\"\"Description d une app de test\"\"\"\n    await i.response.send_message('Hello world, {name_module}')"
            )
        if platform.system() == "Windows":
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}\\Bot\\commandes\\{name_module}.py")
        else:
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}/Bot/commandes/{name_module}.py")