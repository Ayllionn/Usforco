import json
import os
import threading
import time
import traceback
from typing import Any

import discord.ext.commands
import asyncio

from glob import glob
from json import load
from discord import Intents
from discord.app_commands.tree import CommandTree
from importlib import import_module
from data import ORM
from .term import CustomTerminal

class BOT(discord.Client):
    def __init__(self, dir, token, dbpath, dbname, static, intent=None, **kwargs):
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

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        with open(f"./errors/{self.project_name}", "a") as log:
            up = "\t\n"
            log.write(f"DICORC API ERROR: {str(event_method)} :\n\n args : {up.join([str(i) for i in args])} kwargs :\n\n {up.join([f'{k} : {v}' for k, v in kwargs.items()])} : \n")
            try:
                log.write("\n\n"+str(traceback.format_exc()))
            except:
                pass
            log.write("\n_______________________________________________________________________________________________")
        print(self.project_name, f"ERROR in {event_method}")

    def static_obj(self, obj, name:str=None):
        if name is None:
            self._static_obj.update(
                {
                    obj.__name__: obj
                }
            )
        else:
            self._static_obj.update(
                {
                    name:obj
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

    def get_static(self, name:str) -> str or dict:
        try:
            with open(f"{self.static_dir}/{name}", "r+") as f:
                if name.endswith(".json"):
                    return load(f)
                else:
                    return f.read()
        except:
            return None

    def all_s_in_dir(self, dir_name:str):
        glober = glob(f'{self.static_dir}/{dir_name}/*')
        glober = [i.replace(f'{self.static_dir}/', '') for i in glober]
        return {k.split(".")[0].replace("\\", "/").split("/")[-1]:self.get_static(k) for k in glober}

    def set_static(self, name:str, content:str or dict=None):
        if content is not None:
            chemin = f"{self.static_dir}/{name}"
            if not os.path.exists(chemin):
                for i in range(len(chemin.replace("\\", "/").split("/"))):
                    try:
                        os.makedirs("/".join(chemin.replace("\\", "/").split("/")[:-(i+1)]))
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

        self.sysorm.create_data('Views', id=int(msg.id), obj_name=obj_name, options=options, channel=msg.channel.id)

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
                channel = self.get_channel(b.channel)
                await channel.fetch_message(int(b))
            except:
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


class Project:
    def __init__(self, name, conf):
        self.bot = BOT(**conf)
        self.error = False
        self._container = []
        self.name = name
        self.commun = conf.get("commun")
        self.dir = conf.get("dir")
        conf.update({"project_name": name})
        self.conf = conf.copy()

    def load(self):
        print(self.name, 'lunched')
        try:
            self._container.clear()
            name = self.name
            conf = self.conf

            self.error = False

            self.name = name

            if self.dir is None:
                raise ValueError("Directory not found in your config file")

            self.bot = BOT(**conf)

            for i in self.commun:
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

# ____________________________________________________________________________________________________________________ #

        if self.error is False:
            try:
                self.bot.run(token=self.bot.token)
            except:
                pass

            if self.bot.get_static("sys/stat.txt") == "off":
                return

            try:
                print(f"{self.bot.user.name} disconnected. Restart in 30 seconds")
            except:
                print(f"Le project {self.name} ne posséde pas un token valide")
                return
            time.sleep(30)
            return self.load()

        else:
            with open(f"./errors/{self.name}", "a+", encoding="utf8") as f:
                f.write(
                    self.error + "\n_____________________________________________________________________________\n")
                print(self.name, f"ERROR, details in ./errors/{self.name}")


class Server:
    def __init__(self):
        self.on = False
        self.threads = []
        if not os.path.exists("errors"):
            os.makedirs("errors")
        try:
            with open("./Project/config.json", "r", encoding="utf8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            try:
                os.mkdir("./Project/")
            except:
                pass

            name = input("1st project's name : ").replace(" ", "_")

            self.config = {
                name : {
                    "start": True,
                    "token": input("Token : ").replace(" ", ""),
                    "intents": input("Intents function [all, default]: ").replace(" ", ""),
                    "dbname": input("Database name : ").replace(" ", "_"),
                    "dbpath": input("Database path : "),
                    "dir": input("Project's commands folder : "),
                    "static" : input("Static folder : "),
                    "commun" : []
                }
            }
            config = self.config[name]

            if not os.path.exists(config["dir"]):
                os.makedirs(config["dir"])
            if not os.path.exists(config["dbpath"]):
                os.makedirs(config["dbpath"])

            with open("./Project/config.json", "w", encoding="utf8") as f:
                json.dump(self.config, f)

        self.projects = [
            Project(k, v) for k, v in self.config.items()
        ]

    def _bg_task(self):
        while self.on:
            time.sleep(2)
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
        print("Server off")

    def stop_project(self, project_name):
        for project in self.projects:
            if project.name == project_name:
                project.bot.off()

    def start_project(self, project_name, standalone=False):
        for project in self.projects:
            if project.name == project_name:
                try:
                    if standalone:
                        project.load()
                    else:
                        thread = threading.Thread(target=project.load)
                        self.threads.append(thread)
                        thread.start()
                except:
                    with open(f"./errors/{project.name}", "a+") as f:
                        f.write(f"ERROR at start :\n {traceback.format_exc()}")
                        f.write(
                            "\n_______________________________________________________________________________________")

    def load(self):
        self.on = True
        threading.Thread(target=self._bg_task).start()
        self.threads = []
        for project in self.projects:
            try:
                if project.conf.get("start") is None or project.conf.get("start") == True:
                    thread = threading.Thread(target=project.load)
                    self.threads.append(thread)
                    thread.start()
            except:
                with open(f"./errors/{project.name}", "a+") as f:
                    f.write(f"ERROR at start :\n {traceback.format_exc()}")
                    f.write("\n_______________________________________________________________________________________")

        terminal = CustomTerminal(panel=False, help_at_start=False, search="n", terminal_name="manage server", variable={"serv":self})
        try:
            terminal.get_raw_cmds_files(f"{os.getcwd()}/Server/term_cmds/")
        except:
            traceback.print_exception()
        terminal.start()

        self.on = False
        for project in self.projects:
            project.bot.off()
