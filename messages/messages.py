import os
from glob import glob

def get(txt_name):
    files = glob(os.getcwd()+"/messages/*.txt")

    messages = {}

    for f in files:
        with open(f, 'r', encoding="utf8") as file:
            messages.update({f.split("\\")[-1].split("/")[-1][:-4]:file.read()})

    return messages.get(txt_name)
