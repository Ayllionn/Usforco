import json
from ..term import CustomTerminal
from Server import Server

def deleted(variables):
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
    project = variables['project']
    server: Server = variables['serv']
    server.start_project(project)
    print("Project will start")

def s_stop(variables):
    """stop the project"""
    project = variables['project']
    server: Server = variables['serv']
    server.stop_project(project)
    print("Project will stop")

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
                          deleted=deleted,
                          start_ws=start_ws,
                          s_start=s_start,
                          s_stop=s_stop)
    term.start()