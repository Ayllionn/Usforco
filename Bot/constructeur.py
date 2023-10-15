import discord
from conf.bot import *
from CustomTerm import CustomTerminal
import DB
from rich.console import Console
from traceback import print_exc
import os
from platform import system

console = Console()

def restart():
    if system() == "Windows":
        systeme = "win"
    else:
        systeme = "lin"
        try:
            with open("os_conf", "r+", encoding="utf8") as f:
                terminal = f.read()

        except:
            terminal = input(
                "Vue que vous êtes sous linux veuillez indiquer la commande qui permet de lancer votre terminal (exemple sous mate : mate-terminal) :")
            with open("os_conf", "w+", encoding="utf8") as f:
                f.write(terminal)

    if systeme == "win":
        os.system("start start.py")
    else:
        os.system(f"{terminal} -e python3 'start.py' &")
    exit()

class BOT(discord.Client):
    def __init__(self, prefixe=None, token=None):
        super().__init__(intents=INTENT_LEVEL)
        self.token = token
        self.prefixe = prefixe
        self.cmd = discord.app_commands.CommandTree(self)
        self._started = False
        self._adm_cmds = {"deco": exit, "restart":restart}
        self._app_cmds = {}
        self._objs = {}
        self.term = None
        self._on_msg_cmd = None

    async def on_ready(self):
        if self._started is False:
            await self.cmd.sync()
            self.term = CustomTerminal("bot", search="n", **self._adm_cmds)

            with console.status(f"Initiation des {len(self._objs)} composants et de leurs instances..."):
                print(f"Initiation des {len(self._objs)} composants et de leurs instances...")
                compte = 0
                all = 0
                for k, comp in self._objs.items():
                    data_obj: dict = DB.get(k)[0]
                    if data_obj is None:
                        continue
                    for msg_id, args in data_obj.items():
                        try:
                            self.add_view(comp(**DB.get(k, msg_id)[0]), message_id=int(msg_id))
                            compte += 1
                        except:
                            print_exc()
                            print("_______\n")
                            print("IGNORED\n")
                            print("\n\n")
                        finally:
                            all += 1

            print(f'Composants instanciés {compte}/{all}')

        print(self.user, "Est online")

    def save_comp(self, obj, msg_id: int, attrib: dict):
        DB.update(obj.__name__, {str(msg_id): attrib})

    def rm_comp(self, obj, msg_id: int):
        data = DB.get(obj.__name__)[0]
        data.pop(str(msg_id))
        DB.save(obj.__name__, data)

    async def on_message(self, msg):
        its_cmd = False
        if msg.author.id in ID_ADMIN:
            if msg.content[:len(PREFIXE)] == PREFIXE:
                if DEL_CMDS_ADMIN:
                    await msg.delete()
                await msg.channel.send(self.term.exe(msg.content[len(PREFIXE):]))
                its_cmd = True

        if self._on_msg_cmd is not None:
            if its_cmd is False:
                await self._on_msg_cmd(msg)

    def create_on_messgae(self):
        def deco(func):
            self._on_msg_cmd = func

        return deco

    def cmd_admin(self, name=None):
        def deco(func):
            if name is None:
                self._adm_cmds.update({func.__name__: func})
            else:
                self._adm_cmds.update({name: func})

        return deco

    def app_cmd(self, name=None, **kwargs):
        def deco(func):
            if name is None:
                self._app_cmds.update({func.__name__: {"func":func, "args":kwargs}})
            else:
                self._app_cmds.update({name: {"func":func, "args":kwargs}})

        return deco

    def add_component(self, obj):
        self._objs.update({obj.__name__: obj})

    def load(self):
        jump = '              '
        print("CONFIG DU BOT :")
        print("")
        print("TOKEN:", self.token)
        print("Nombre de commandes :", len(self._app_cmds)+len(self._adm_cmds))
        print("     ADM_CMD :", len(self._adm_cmds))
        print("     APP_CMD :", len(self._app_cmds))
        print("")
        print("     ADM_CMD :")
        [print(jump, l) for l in self._adm_cmds.keys()]
        print("")
        print("     APP_CMD :")
        [print(jump, l) for l in self._app_cmds.keys()]
        print("")
        print("\nComposants :", len(self._objs))
        [print(jump, l) for l in self._objs.keys()]
        print("_________________________________________")

        console.log("Lancement du bot !")
        with console.status(f"Chargement des {len(self._app_cmds)} commandes... "):
            print(f"Chargement des {len(self._app_cmds)} commandes... ")
            compte = 0
            for k, ap_c in self._app_cmds.items():
                try:
                    self.cmd.command(name=k, description=ap_c["func"].__doc__, **ap_c["args"])(ap_c["func"])
                    console.log(f"{k} : [green]LOADED !")
                    compte += 1
                except:
                    print_exc()
                    print("_______\n")
                    print("IGNORED\n")
                    print("\n\n")

        print(f"Commandes initialisées ! {compte}/{len(self._app_cmds)}")
        print('')

        self.run(self.token)


bot = BOT(PREFIXE, TOKEN)
