import json
import os
import threading
import time
import traceback
from glob import glob
from json import load
import discord.ext.commands
from discord import Intents
from discord.app_commands.tree import CommandTree
from importlib import import_module
from data import ORM


class BOT(discord.Client):
    def __init__(self, dir, token, db_path, db_name, static, intent=None):
        self.dir = dir
        self.static_dir = static
        if intent is not None:
            if type(intent) is list:
                intents = Intents(**{k: True for k in intent})
            elif type(intent) is str:
                intents = getattr(Intents, intent)()
        else:
            intents = Intents.default()

        """
        class créeant le bot et déployant les tools utilisables
        """
        super().__init__(intents=intents)
        self.sysorm: ORM = None
        self.orm: ORM = None

        self.db_path = db_path
        self.db_name = db_name

        self.token = token
        self.tree = CommandTree(self)
        self._objs = {}
        self._fun_or = []

    def on_ready_addon(self):
        def decorator(func):
            self._fun_or.append(func)

        return decorator

    def get_static(self, name):
        try:
            with open(f"{self.static_dir}/{name}", "r+") as f:
                if name.endswith(".json"):
                    return load(f)
                else:
                    return f.read()
        except:
            return None

    def set_static(self, name, content):
        chemin = f"{self.static_dir}/{name}"
        if not os.path.exists(chemin):
            os.makedirs(chemin)
        with open(chemin, "w+", encoding="utf8") as f:
            if name.endswith(".json"):
                json.dump(content, f)
            else:
                f.write(content)

    async def save_view(self, obj: object, msg, edit=False):
        obj_name = obj.__class__.__name__
        options = {k: v for k, v in obj.__dict__.items() if
                   k not in ["_View__timeout", "_children", "_View__weights", "id", "_cache_key",
                             "_View__cancel_callback", "_View__timeout_expiry", "_View__timeout_task", "_View__stopped"] \
                   and type(v) in [int, str, float, bool, tuple, list, dict]}

        if obj_name not in self._objs.keys():
            raise ValueError(f"{obj_name} not in persistant components")

        self.sysorm.create_data('Views', id=int(msg.id), obj_name=obj_name, options=options)

        if edit:
            await msg.edit(content=msg.content, view=obj)

    def delete_view(self, id):
        obj = self.sysorm.get_by_id('Views', id)
        obj.delete()

    async def on_ready(self):

        self.sysorm = ORM(path=self.db_path, name=f"sys_{self.db_name}")
        self.orm = ORM(path=self.db_path, name=self.db_name)

        @self.sysorm.schema
        class Views:
            id = int
            obj_name = str
            options = dict

        await self.tree.sync()
        for b in self.sysorm.get_all_by_table('Views'):
            obj = self._objs.get(b.obj_name)
            if obj is None:
                raise ValueError(f'{b.obj_name} not in [{", ".join(self._objs.keys())}]')

            self.add_view(obj(**b.options), message_id=int(b))

        print(self.user.name, "connected !")
        
        for i in self._fun_or:
            await i()

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


class Project:
    def __init__(self, name, conf):
        self.error = False
        self._container = []

        try:
            self.name = name
            self.dir = conf.pop("dir")
            commun = conf.pop("commun")
            if self.dir is None:
                raise ValueError("Directory not found in your config file")

            self.bot = BOT(dir=self.dir, **conf)

            for i in commun:
                try:
                    module = import_module(i)
                    getattr(module, "addon")(self.bot)
                except Exception as e:
                    with open(f"./errors/{self.name}", "a+", encoding="utf8") as f:
                        f.write(
                            traceback.format_exc() + "\n_____________________________________________________________________________\n")
                        print(self.name, f"ERROR, details in ./errors/{self.name}")

            print(self.dir)
            for root, dirs, files in os.walk(self.dir):
                s = root
                for file in files:
                    root = s
                    if file.endswith(".py"):
                        file = file[:-3]
                        if root.startswith("."):
                            root = root[2:]
                        root.replace(os.getcwd(), "")
                        root = root.replace("\\", "/").replace("/", ".") + "." + file
                        print(root)
                        module = import_module(root)
                        self._container.append(getattr(module, "addon")(self.bot))

            print(name, "initialised ! with no errors")
        except Exception as e:
            print(name, e)
            self.error = traceback.format_exc()

    def load(self):
        if self.error is False:
            while True:
                try:
                    self.bot.run(token=self.bot.token)
                except KeyboardInterrupt:
                    break
                else:
                    time.sleep(10)
                    continue
        else:
            with open(f"./errors/{self.name}", "a+", encoding="utf8") as f:
                f.write(
                    self.error + "\n_____________________________________________________________________________\n")
                print(self.name, f"ERROR, details in ./errors/{self.name}")


class Serveur:
    def __init__(self):
        self.projects = []

        for path in glob(f"{os.getcwd()}/Project/*.json"):

            with open(path, "r+", encoding="utf8") as f:
                conf = load(f)

            try:
                self.projects.append(Project(path.replace("\\", '/').split("/")[-1][:-5], conf))
            except:
                traceback.print_exc()

    def load(self):
        process = []
        for p in self.projects:
            process.append(threading.Thread(target=p.load))
            process[-1].start()

        try:
            for proc in process:
                proc.join()
        except KeyboardInterrupt:
            exit()
