from conf import importer
"""
_______________________________________________________________________________________________________________________
                                            <!!!!! ATTENTION !!!!!>

                        Toutes les variables ici sont OBLIGATOIRE au bon fonctionnement du bot

                                            <!!!!! ATTENTION !!!!!>
_______________________________________________________________________________________________________________________

PREFIXE : le prefixe des commandes d'admins (seul les admins du bot peuvent les faire)
TOKEN : C'est le jeton de connexion a votre app
INTENT_LEVEL : se sont tout simplement les intents qu'as votre bit (all() = toutes les perms)
ID_ADMIN : Les ID des gens pouvant faire des commandes admin
DEL_CMDS_ADMIN : Si positionné sur True, alors il suprimera toutes les commandes que les admins enverrons
"""

PREFIXE = "p!"
TOKEN = "MTE2MzA1NzA1MjM2MTQyNTAyMA.GqTxyI.0RGhlswz9h1q89Q_MH9DS6ZXZ49rYxIC8_BJ8k"
ID_ADMIN = [580422615496392715]
DEL_CMDS_ADMIN = True
INTENT_LEVEL = importer.Intents.all()
