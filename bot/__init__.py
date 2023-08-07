import os
from glob import glob
import importlib
from rich.console import Console
from rich.prompt import Prompt
from traceback import print_exc
from bot.constructeur import bot

console = Console()

console.print("Liste des module de commandes :")

files = glob(f"{os.getcwd()}/bot/commandes/*.py")

for f in files:
    try:
        file_name = f.split("\\")[-1].split("/")[-1][:-3]
        module = importlib.import_module("bot.commandes." + file_name)
        console.log(f"[blue]{file_name}[/blue] : [green]loaded")
    except Exception as e:
        console.log(f"{file_name} : ERROR :[red] {e}")
        aws = Prompt.ask(prompt="voulez vous le traceback ?", choices=["o", "n"], default="n")
        if aws == "o":
            print_exc()
            input("Pressez entrer pour continuer")

console.print("Liste des module de routines :")

files = glob(f"{os.getcwd()}/bot/routine/*.py")

for f in files:
    try:
        file_name = f.split("\\")[-1].split("/")[-1][:-3]
        module = importlib.import_module("bot.routine." + file_name)
        console.log(f"[blue]{file_name}[/blue] : [green]loaded")
    except Exception as e:
        console.log(f"{file_name} : ERROR :[red] {e}")
        aws = Prompt.ask(prompt="voulez vous le traceback ?", choices=["o", "n"], default="n")
        if aws == "o":
            print_exc()
            input("Pressez entrer pour continuer")
