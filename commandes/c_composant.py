import os
import platform
from string import ascii_lowercase, ascii_uppercase

letters = {k:v for k, v in zip(ascii_lowercase, ascii_uppercase)}

def start(*args):
    """permet de crée un fichier de composants pour le bot"""
    for name_module in args:
        try:
            name_class = letters[name_module[0]]+name_module[1:]
        except:
            print(f"{name_module} n'est pas conventionnellement correcte donc nous l'avons signoré")
            continue

        with open(f"{os.getcwd()}/Bot/components/{name_module}.py", "w", encoding="utf8") as f:
            var = ['from discord.ui import View, button, select',
                   'import discord', 'from Bot import bot', '', '"""',
                   "Tout se programme comme d'habitude, JUSTE que si vous souhaitez que les instances de ces Views soit sauvegardés et redeployé",
                   'faites bot.add_component(<nom_de_la_class>)',
                   '"""', '', f'class {name_class}(View):',
                   '    def __init__(self):',
                   '        super().__init__(timeout=None)','',
                   f'    @button(label="{name_module} bouton", style=discord.ButtonStyle.green, custom_id="{name_module}")',
                   f'    async def {name_module}(self, i, obj):', f'        await i.response.send_message("Je suis vivant !, {name_module}")',
                   '',
                   f'bot.add_component({name_class})']

            [f.write(l+"\n") for l in var]
            with open(f"{os.getcwd()}/Bot/components/__init__.py", "a+", encoding="utf8") as f2:
                f2.write("try:\n")
                f2.write(f"    from .{name_module} import *\n")
                f2.write("except:\n")
                f2.write(f"    raise ImportError('COMPOSANT ALERTE !! {name_module} n\\'existe plus dans les fichier python !')\n"
                         f"#__________________________________________________________________________________________________________\n")
        if platform.system() == "Windows":
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}\\Bot\\components\\{name_module}.py")
        else:
            print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}/Bot/components/{name_module}.py")