import discord
from conf.bot import *
from CustomTerm import CustomTerminal
import DB
from rich.console import Console
from traceback import print_exc

console = Console()


class BOT(discord.Client):
    def __init__(self, prefixe=None, token=None):
        super().__init__(intents=INTENT_LEVEL)
        self.token = token
        self.prefixe = prefixe
        self.cmd = discord.app_commands.CommandTree(self)
        self._started = False
        self._adm_cmds = {"deco": exit}
        self._app_cmds = {}
        self._objs = {}
        self.term = None

    async def on_ready(self):
        if self._started is False:
            await self.cmd.sync()
            self.term = CustomTerminal("bot", search="n", **self._adm_cmds)

        print(self.user, "Est online")

    def save_comp(self, obj, msg_id: int, attrib: dict):
        DB.update(obj.__name__, {str(msg_id): attrib})

    def rm_comp(self, obj, msg_id: int):
        data = DB.get(obj.__name__, str(msg_id))
        data.pop(str(msg_id))
        DB.update(obj.__name__, data)

    async def on_message(self, msg):
        if msg.author.id in ID_ADMIN:
            if msg.content[:len(PREFIXE)] == PREFIXE:
                if DEL_CMDS_ADMIN:
                    await msg.delete()
                await msg.channel.send(self.term.exe(msg.content[len(PREFIXE):]))

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

        self.run(self.token)


bot = BOT(PREFIXE, TOKEN)