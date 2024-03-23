import json
import os
import subprocess
import sys
import platform
import time

from ..term import CustomTerminal
from Server import Server

def delete(variables):
    "delete the project"
    project = variables['project']
    server : Server = variables['serv']
    try:
        server.stop_project(project)
    except:
        pass
    with open("Project/config.json", "r+") as f:
        config = json.load(f)
    with open('Project/config.json', 'w+') as f:
        config.pop(project)
        json.dump(config, f)
    print("Project deleted, please exit this terminal")

def start_ws(variables, y_n):
    """start the project with the server"""
    project = variables['project']
    if y_n == "y":
        with open("Project/config.json", "r+") as f:
            config = json.load(f)
        with open('Project/config.json', 'w+') as f:
            config[project].pop("start")
            json.dump(config, f)
        print("Project will start with server")
    else:
        with open("Project/config.json", "r+") as f:
            config = json.load(f)
        with open('Project/config.json', 'w+') as f:
            config[project].update({"start": False})
            json.dump(config, f)
        print("Project will not start with server")

def s_start(variables):
    """start the project"""
    command = [sys.executable, os.getcwd()+"/"+"main.py", variables["project"]]
    subprocess.Popen(command, shell=True)

def s_stop(variables):
    """stop the project"""
    project = variables['project']
    server: Server = variables['serv']
    server.stop_project(project)
    print("Project will stop")

def reload(variables):
    """reload the project"""
    s_stop(variables)
    time.sleep(5)
    s_start(variables)

def modify(variables):
    """modify the project config"""

    c_cmd = "clear"
    if platform.system() == "Windows":
        c_cmd = "cls"

    f = open("Project/config.json")
    config = json.load(f)[variables["project"]]
    f.close()

    def display(options, txt):
        os.system(c_cmd)
        print(txt)
        print("")
        [print(f"{i+1} => {v}") for i, v in enumerate(options)]
        while True:
            entry = input("\n choose your number :")
            try:
                entry = int(entry)
                if not 1 <= entry <= len(options):
                    raise ValueError()
                else:
                    return options[entry-1]
            except:
                print("something went wrong")
                continue

    while True:
        v = display([i for i in config.keys()]+["exit"], "Select the value :")
        if v == "exit":
            with open("Project/config.json", "r") as f:
                cfg = json.load(f)
            with open("Project/config.json", "w+") as f:
                cfg.update({variables["project"]: config})
                json.dump(cfg, f)
            break
        else:
            t = display(["str", "int", "bool", "exit"], f"Current value = {config[v]}\nSelect type")
            if t == "exit":
                continue
            elif t == "bool":
                value = display(["True, False"], "Select a value :")
                value = True if value == "True" else False
                config[v] = value
            else:
                mapping = {
                    "str":str,
                    "int": int
                }
                while True:
                    try:
                        config[v] = mapping[t](input("Your value :"))
                        break
                    except:
                        continue

def start(variables, project:str=None):
    """Permet de geré les projects"""
    with open("Project/config.json") as json_file:
        config = json.load(json_file)

    if len(config.keys()) == 0:
        print("No Project")
        return

    check = config.get(project)
    if check is None:
        project = None
    if project is None and len(config.keys()) > 1:
        print("Projects :")
        [print("\t", k) for k in config.keys()]
        print("\nSelect a project")
        return
    elif len(config.keys()) == 1:
        project = [k for k in config.keys()][0]


    print(f"Selected project: {project}")
    term = CustomTerminal(search="n", terminal_name=f"manage {project}", panel=False, variable={"project":project, "serv":variables["serv"]},
                          delete=delete,
                          start_ws=start_ws,
                          start=s_start,
                          stop=s_stop,
                          reload=reload,
                          modify=modify)
    term.start()
