import os
import platform

def start():
    """permet de configuré les variabe de configuration du bot"""
    print("""
_______________________________________________________________________________________________________________________
                                            <!!!!! ATTENTION !!!!!>

                        Toutes les variables ici sont OBLIGATOIRE au bon fonctionnement du bot

                                            <!!!!! ATTENTION !!!!!>
_______________________________________________________________________________________________________________________

PREFIXE : le prefixe des commandes d'admins (seul les admins du bot peuvent les faire)
TOKEN : C'est le jeton de connexion a votre app
INTENT_LEVEL : se sont tout simplement les intents qu'as votre bit (all() = toutes les perms)
""")
    var = ['from conf import importer',
           '"""',
           '_______________________________________________________________________________________________________________________',
           '                                            <!!!!! ATTENTION !!!!!>', '',
           '                        Toutes les variables ici sont OBLIGATOIRE au bon fonctionnement du bot', '',
           '                                            <!!!!! ATTENTION !!!!!>',
           '_______________________________________________________________________________________________________________________',
           '', "PREFIXE : le prefixe des commandes d'admins (seul les admins du bot peuvent les faire)",
           "TOKEN : C'est le jeton de connexion a votre app", "INTENT_LEVEL : se sont tout simplement les intents qu'as votre bit (all() = toutes les perms)",
           'ID_ADMIN : Les ID des gens pouvant faire des commandes admin', 'DEL_CMDS_ADMIN : Si positionné sur True, alors il suprimera toutes les commandes que les admins enverrons',
           '"""', '', f'PREFIXE = "{input("PREFIXE :")}"', f'TOKEN = "{input("TOKEN :")}"',
           f'ID_ADMIN = [{input("ID_ADMIN :")}]', f'DEL_CMDS_ADMIN = {input("DEL_CMDS_ADMIN :")}', 'INTENT_LEVEL = importer.Intents.all()']

    """permet de crée un fichier de conf pour le bot"""
    name_module = "bot"
    with open(f"{os.getcwd()}/conf/{name_module}.py", "w", encoding="utf8") as f:
        def write_p(l):
            f.write(l + "\n")
        [write_p(l) for l in var]

    if platform.system() == "Windows":
        print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}\\conf\\{name_module}.py")
    else:
        print(f"Fichier {name_module} crée, path :", f"{os.getcwd()}/conf/{name_module}.py")