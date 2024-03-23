import traceback
import os
import time

from Server.bot import BOT
from importlib import import_module


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