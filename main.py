import os
import platform

if not os.path.exists('cache'):
    os.mkdir('cache')

try:
    with open('cache/env', "r+") as f:
        env = f.read().split("\n")[0]
        if not os.path.exists("cache/env") or not os.path.exists(env):
            raise ValueError()
except:
    with open('cache/env', "w+") as f:
        env = input("Please enter your environment path\n> :")
        if os.path.exists(env):
            print(env)
            f.write(env)
        else:
            exit("Environment folder not found")

def check():

    for root, dirs, files in os.walk(env):
        for file in files:
            if file.split(".")[0] == "pip":
                pip = os.path.join(root, file)

    try:
        print(pip)
    except:
        exit("pip not found")

    with open("./requirements.txt", "r+") as file:
        requirements = file.read().split("\n")

    cmd = os.popen(f"{pip} freeze")
    cmd = cmd.read().split("\n")[:-1]

    for r in requirements:
        if r == "":
            continue
        if r in cmd:
            print(f"{r} checked !")
            pass
        else:
            print(f"{r} not checked !")
            os.system(f"{pip} install \"{r}\"")

check()
if platform.system() == "Windows":
    os.system("cls")
elif platform.system() == "Linux":
    os.system("clear")
else:
    exit("Unsupported")

from Server import Serveur

if __name__ == '__main__':
    srv = Serveur()
    srv.load()
