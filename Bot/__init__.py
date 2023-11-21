import os
import traceback
from .master import bot
from importlib import import_module

libs = []
for root, dirs, files in os.walk("./Bot/Bot"):
    for file in files:
        try:
            temp = root + "." + file

            temp = temp[2:-3].replace("/", '.').replace('\\', '.')

            if "__pycache__" in temp.split("."):
                continue

            c = False
            for dir in temp.split(".")[:-1]:
                if dir.startswith("_"):
                    print(f"{root} -> {file} : a bien était ignoré (package {dir})")
                    c = True
                    break

            if c:
                continue

            if file.startswith("_"):
                print(f"{root} -> {file} : a bien était ignoré")
                continue

            with open(root + "/" + file, "r+", encoding="utf8") as f:
                for i, line in enumerate(f.read().split("\n")):
                    if i > 0:
                        break
                    if line in ["#ignore", "#pass", "#no"]:
                        print(f"{root} -> {file} : a bien était ignoré")
                        c = True
            if c:
                continue

            import_module(temp)
        except:
            print(temp, "N'as pas correctement était importé au projet")
            with open("traceback.txt", "a+", encoding="utf8") as file:
                file.write("________________________________________________________________________________________")
                file.write(traceback.format_exc())