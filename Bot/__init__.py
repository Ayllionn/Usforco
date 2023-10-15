import os
from glob import glob
from importlib import import_module
from traceback import print_exc
from .constructeur import bot

DIR = os.getcwd()


PATHS = [
    f"{DIR}/Bot/commandes/*.py",
    f"{DIR}/Bot/components/*.py",
    f"{DIR}/Bot/routines/*.py"
]

libs = [glob(f) for f in PATHS]
for l in libs:
    for i in l:
        i = i[len(DIR)+1:-3].replace("/", ".").replace("\\", ".")
        try:
            import_module(i)
        except:
            print_exc()
            print("\n")
            print("IGNORED")
            print("\n\n")

