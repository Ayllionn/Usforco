import discord
from discord import ui, app_commands
import asyncio
import data_exploit
from random import randint
import os
from glob import glob
import importlib
from rich.console import Console
from rich.prompt import Prompt
from traceback import print_exc

console = Console()

files = glob(f"{os.getcwd()}/bot/components/*.py")

components = {}

for f in files:
    try:
        file_name = f.split("\\")[-1].split('/')[-1][:-3]
        module = importlib.import_module("bot.components." + file_name)
        obj = getattr(module, "obj", None)
        components.update({obj.__doc__: obj})
        console.log(f"[blue]{file_name}[/blue] : [green]loaded")
    except Exception as e:
        console.log(f"{file_name} : ERROR :[red] {e}")
        aws = Prompt.ask(prompt="voulez vous le traceback ?", choices=["o", "n"], default="n")
        if aws == "o":
            print_exc()
            input("Pressez entrer pour continuer")
    finally:
        del files, f, file_name, aws


class BOT(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.token = data_exploit.get("config", "token")[-1]
        self.started = False
        self.tree = discord.app_commands.CommandTree(self)

    def load(self):
        self.run(self.token)

    def rm_view(self, i, type):
        k, v = data_exploit.get(type)
        print(v.pop(str(i.message.id)))
        data_exploit.set(type, **v)

    def add_save_view(self, option: dict, msg_id, obj):
        data_exploit.update(obj.__doc__, **{str(msg_id): option})
        self.add_view(obj, message_id=msg_id)

    async def on_ready(self):
        if self.started is False:
            await self.tree.sync()
            bot_log = self.get_channel(data_exploit.get("config", "log_channel")[-1])
            embed = discord.Embed(title="**Système opérationnel**",
                                  description='Mise en service des systèmes du bot', color=int("00ff07", 16))
            await bot_log.send(embed=embed)

            # reprise des boutons
            for _type, obj in components.items():
                if data_exploit.get(_type)[-1] is not None:
                    for k, v in data_exploit.get(_type)[-1].items():
                        self.add_view(obj(**{"bot": self, **v}), message_id=int(k))

            self.started = True
        print(f"{self.user} : Je suis OK")

bot = BOT()