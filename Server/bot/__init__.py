import discord.ext.commands
import asyncio
import os
import traceback
import json

from Server.data import ORM
from typing import Any
from glob import glob
from json import load
from discord import Intents
from discord.app_commands.tree import CommandTree


class BOT(discord.Client):
    def __init__(self, dir, token, dbpath, dbname, static, intents=None, **kwargs):
        self.dir = dir
        self.static_dir = static
        if intents is not None:
            if type(intents) is list:
                intents = Intents(**{k: True for k in intents})
            elif type(intents) is str:
                intents = getattr(Intents, intents)()
        else:
            intents = Intents.default()

        """
        class créeant le bot et déployant les tools utilisables
        """
        super().__init__(intents=intents)
        self.project_name = kwargs.get('project_name')
        self.sysorm: ORM = None
        self.orm: ORM = None

        self.db_path = dbpath
        self.db_name = dbname

        self._schemas = []

        self.token = token
        self.tree = CommandTree(self)
        self._objs = {}
        self._fun_or = []
        self._fun_om = []
        self._fun_omd = []
        self._static_obj = {}

        self.tree.error(self.on_command_error)

    async def on_command_error(self, ctx, erreur):
        await self.on_error("SLASH_COMMAND", error=erreur)

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        with open(f"./errors/{self.project_name}", "a") as log:
            up = "\n"
            log.write(
                f"DICORD API ERROR: {str(event_method)} :\n\n args :\n {up.join([str(i) for i in args])}\n_________________________________________________________\n kwargs :\n {up.join([f'{k} : {v}' for k, v in kwargs.items()])} : \n")
            try:
                log.write("\n\n" + str(traceback.format_exc()))
            except:
                pass
            log.write(
                "\n_______________________________________________________________________________________________\n")
        print(self.project_name, f"ERROR in {event_method}")

    def static_obj(self, obj, name: str = None):
        if name is None:
            self._static_obj.update(
                {
                    obj.__name__: obj
                }
            )
        else:
            self._static_obj.update(
                {
                    name: obj
                }
            )

        return obj

    def schema(self, obj):
        self._schemas.append(obj)

        return None

    def on_message_delete_addon(self):
        def decorator(func):
            self._fun_omd.append(func)

        return decorator

    def on_ready_addon(self):
        def decorator(func):
            self._fun_or.append(func)

        return decorator

    def on_message_addon(self):
        def decorator(func):
            self._fun_om.append(func)

        return decorator

    def get_static_obj(self, obj_name):
        return self._static_obj.get(obj_name)

    def get_static(self, name: str) -> str or dict:
        try:
            with open(f"{self.static_dir}/{name}", "r+") as f:
                if name.endswith(".json"):
                    return load(f)
                else:
                    return f.read()
        except:
            return None

    def all_s_in_dir(self, dir_name: str):
        glober = glob(f'{self.static_dir}/{dir_name}/*')
        glober = [i.replace(f'{self.static_dir}/', '') for i in glober]
        return {k.split(".")[0].replace("\\", "/").split("/")[-1]: self.get_static(k) for k in glober}

    def set_static(self, name: str, content: str or dict = None):
        if content is not None:
            chemin = f"{self.static_dir}/{name}"
            if not os.path.exists(chemin):
                for i in range(len(chemin.replace("\\", "/").split("/"))):
                    try:
                        os.makedirs("/".join(chemin.replace("\\", "/").split("/")[:-(i + 1)]))
                        break
                    except:
                        continue
            with open(chemin, "w+", encoding="utf8") as f:
                if name.endswith(".json"):
                    json.dump(content, f)
                else:
                    f.write(content)
        else:
            os.remove(f"{self.static_dir}/{name}")

    async def save_view(self, obj: object, msg, edit=False):
        obj_name = obj.__class__.__name__
        options = {k: v for k, v in obj.__dict__.items() if
                   k not in ["_View__timeout", "_children", "_View__weights", "id", "_cache_key",
                             "_View__cancel_callback", "_View__timeout_expiry", "_View__timeout_task", "_View__stopped"] \
                   and type(v) in [int, str, float, bool, tuple, list, dict]}

        if obj_name not in self._objs.keys():
            raise ValueError(f"{obj_name} not in persistant components")

        self.sysorm.create_data('Views', id=int(msg.id), obj_name=obj_name, options=options, channel_id=msg.channel.id)

        if edit:
            await msg.edit(content=msg.content, view=obj)

    def delete_view(self, id):
        obj = self.sysorm.get_by_id('Views', id)
        obj.delete()

    async def _back_task(self):
        while not self.is_closed():
            await asyncio.sleep(5)
            if self.get_static("sys/stat.txt") in ["rdm", "off"]:
                await self.close()

    async def on_message_delete(self, message: discord.Message):
        try:
            msg = self.sysorm.get_by_id("Views", message.id)
            msg.delete()
        except:
            pass
        finally:
            [await i(message) for i in self._fun_omd]

    async def on_ready(self):

        self.set_static('sys/stat.txt', "on")
        self.loop.create_task(self._back_task())

        self.sysorm = ORM(path=self.db_path, name=f"sys_{self.db_name}")
        self.orm = ORM(path=self.db_path, name=self.db_name)

        for i in self._schemas:
            self.orm.schema(i)

        @self.sysorm.schema
        class Views:
            id = int
            channel_id = int
            obj_name = str
            options = dict

        await self.tree.sync()
        for b in self.sysorm.get_all_by_table('Views'):

            try:
                channel = self.get_channel(b.channel_id)
                await channel.fetch_message(int(b))
            except discord.NotFound:
                b.delete()
                continue

            obj = self._objs.get(b.obj_name)
            if obj is None:
                raise ValueError(f'{b.obj_name} not in [{", ".join(self._objs.keys())}]')

            self.add_view(obj(**b.options), message_id=int(b))

        print(self.user.name, "connected !")

        for i in self._fun_or:
            await i()

        print(self.user.name, "is op !")

    async def on_message(self, msg):
        for i in self._fun_om:
            await i(msg)

    def cmd(self, name=None, description=None, **kwargs):
        def decorator(func):
            f_name = name
            if name is None:
                f_name = func.__name__
            f_desc = description
            if description is None:
                f_desc = func.__doc__

            self.tree.command(name=f_name, description=f_desc, **kwargs)(func)

        return decorator

    def comp(self, obj):
        self._objs[obj.__name__] = obj

        return obj

    def reload(self):
        self.close()

    def off(self):
        self.set_static("sys/stat.txt", "off")
