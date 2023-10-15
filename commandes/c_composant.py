import os
import platform


def start(*args):
    """permet de crée un fichier de composants pour le bot"""
    for name_module in args:
        with open(f"{os.getcwd()}/Bot/components/{name_module}.py", "w", encoding="utf8") as f:
            var = ['from discord.ui import View, button, select',
                   'import discord', 'from Bot import bot', '', '"""',
                   "Tout se programme comme d'habitude JUSTE que si vous souhaitez que les instances de ces Views soit sauvegardés et redeployé",
                   'faites bot.add_component(<nom_de_la_class>)',
                   '"""', '', f'class {name_module}(View):',
                   '    def __init__(self):',
                   '        super().__init__(timeout=None)', '',
                   f'    @button(label="{name_module}", style=discord.ButtonStyle.green, custom_id="{name_module}")',
                   f'    async def {name_module}(self, i, obj):', f'        await i.response.send_message("Je suis vivant !, {name_module}")',
                   '',
                   f'bot.add_component({name_module})']

            [f.write(l+"\n") for l in var]
            with open(f"{os.getcwd()}\\Bot\\components\\__init__.py", "a+", encoding="utf8") as f2:
                f2.write(f"from .{name_module} import *\n")
        if platform.system() == "Windows":
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}\\Bot\\components\\{name_module}.py")
        else:
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}/Bot/components/{name_module}.py")