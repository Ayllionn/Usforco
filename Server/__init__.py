import json
import os
import threading
import time
import traceback
from Server.bot import BOT

BOT = BOT

from Server.data import ORM
from .term import CustomTerminal
from .bot.project_manager import Project

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
