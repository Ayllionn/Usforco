import traceback

import discord
from discord import Client
from discord.app_commands.tree import CommandTree
import json

import DB
from DB import DB as db


class NotConfigured(Exception):
    pass

class NotFound(Exception):
    pass


config = db("config")

if config.get("intents") == "all":
    Intents = discord.Intents.all()
elif config.get("intents") == 'default':
    Intents = discord.Intents.default()
else:
    print(
        "Intents innatendu :"
    )
    print(config.get("intents"))
    Intents = discord.Intents.default()

if config.if_not_exist():
    raise NotConfigured("Veuilliez configurer le bot avant tout démarrage !")


class BOT(Client):
    def __init__(self, token, intents):
        super().__init__(intents=intents)
        self.token = token
        self.cmd = CommandTree(self)
        self.started = False

        self._on_ready_func = []
        self._on_message_func = []

        self._objs = {}

        config.end()

    def on_ready_func(self):
        def deco(func):
            self._on_ready_func.append(func)

        return deco

    def on_message_func(self):
        def deco(func):
            self._on_message_func.append(func)

        return deco

    async def add_save_view(self, msg: discord.Message, obj, attrib: dict, edit: bool = True):
        self.add_view(view=obj(**attrib), message_id=msg.id)
        views = db(f"views-{msg.guild.id}-{obj.__name__}")
        views.update({str(msg.id): {"attrib": attrib, "obj": obj.__name__}})
        if edit:
            await msg.edit(content=msg.content, view=obj(**attrib))
        views.end()

    def remove_view(self,interaction, msg_id:int, obj_name:str):
        views = db(f'views-{interaction.guild.id}-{obj_name}')
        if views.if_not_exist():
            raise NotFound()
        views.remove(str(msg_id))
        views.end()

    async def on_ready(self):
        if self.started:
            pass
        else:
            await self.cmd.sync()
            self.started = True
            all_db = DB.list_all_db_name()
            views = []
            objkey = "views"
            for k in all_db:
                if k[:len(objkey)] == objkey:
                    print(k)
                    views.append(db(k).get())

            for data in views:
                try:
                    for k, v in data.items():
                        try:
                            self.add_view(self._objs[v["obj"]](**v['attrib']), message_id=int(k))
                        except:
                            print(f"\n{data}\nID msg : {k}\nN AS PAS PUE ETRE CHARGE !\n")
                            with open("traceback.txt", "a+", encoding="utf8") as file:
                                file.write(
                                    "_________________________________________________"
                                    "_______________________________________"
                                )
                                file.write(traceback.format_exc())
                except:
                    continue

            print(f"{self.user.name}, ok !")
        print(f"{self.user.name} Est connecté")
        config.end()

        try:
            await self._on_ready_func()
        except:
            pass

        for i in self._on_ready_func:
            await i()

    def load(self):
        self.run(self.token)

    def create_component(self, cls):
        self._objs.update({cls.__name__: cls})

        return cls


bot = BOT(config.get("token"), Intents)