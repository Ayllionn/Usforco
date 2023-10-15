import os
import platform


def start(*args):
    """permet de crée un fichier de routine pour le bot"""
    for name_module in args:
        with open(f"{os.getcwd()}/Bot/routines/{name_module}.py", "w", encoding="utf8") as f:
            var = ['from Bot import bot', 'import discord', 'from discord.ext.tasks import *', '', '"""',
                   'programmation basique des events et taches...',
                   'pour le on_ready et on_message allez modifié le constructeur.py pour evité de casser le script',
                   '"""',
                   '', '#@bot.event', '#async def on_ready():', '#    print("je fonctionne")']

            [f.write(l+"\n") for l in var]
        if platform.system() == "Windows":
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}\\Bot\\routines\\{name_module}.py")
        else:
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}/Bot/routines/{name_module}.py")