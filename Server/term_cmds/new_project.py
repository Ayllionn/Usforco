import json
import os

def start(variables, name:str=None):
    """crée un nouveau project"""
    with open("./Project/config.json", "r") as file:
        config = json.load(file)

    projects = [k for k in config.keys()]

    if name is None or name in projects:
        while True:
            name = input("project's name : ").replace(" ", "_")
            if name not in projects:
                break
            else:
                print(f"project {name} already exist")

    config.update({
        name: {
            "token": input("Token : ").replace(" ", ""),
            "intents": input("Intents function [all, default]: ").replace(" ", ""),
            "dbname": input("Database name : ").replace(" ", "_"),
            "dbpath": input("Database path : "),
            "dir": input("Project's commands folder : "),
            "static": input("Static folder : "),
            "commun": [],
            "start": False
        }
    })

    cfg = config.copy()
    config = config[name]

    if not os.path.exists(config["dir"]):
        os.makedirs(config["dir"])
    if not os.path.exists(config["dbpath"]):
        os.makedirs(config["dbpath"])

    with open("./Project/config.json", "w", encoding="utf8") as f:
        json.dump(cfg, f)

    print("Project created !")