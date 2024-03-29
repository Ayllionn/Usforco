import os
import platform
import time
import traceback
from venv import create
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('opt'):
    print(f"Python version : {platform.python_version()}")
    os.mkdir('opt')

try:
    with open('opt/env', "r+") as f:
        env = f.read().split("\n")[0]
        if not os.path.exists(env):
            print("please wait.")
            create(os.path.join(os.getcwd(), env), with_pip=True, upgrade_deps=True)
            print(env, "done !")
except:
    with open('opt/env', "w+") as f:
        env = input("Please enter your environment path\n> :")
        if os.path.exists(env):
            pass
        else:
            create(os.path.join(os.getcwd(), env), with_pip=True, upgrade_deps=True)

        print(env)
        f.write(env)

python = None


for root, dirs, files in os.walk(env):
    for file in files:
        if file.split(".")[0].lower() == "pip":
            pip = os.path.join(root, file)
        if file.split(".")[0].lower() == "python":
            python = os.path.join(root, file)


try:
    print(pip)
except:
    exit("pip not found")
try:
    print(python)
except:
    exit("python not found")


with open("./requirements.txt", "r+", encoding="utf8") as file:
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

if platform.system() == "Windows":
    os.system("cls")
elif platform.system() == "Linux":
    os.system("clear")
else:
    exit("Unsupported")

try:
    error = False
    from Server import Server
    from Server.update import update as up

    if not os.path.exists('opt/update.txt'):
        with open("opt/update.txt", "w") as update:
            update.write(input("Do you want to auto-update at start ? [y/n] :"))
    up("y")
except ModuleNotFoundError:
    error = True
    os.system(f"{python} main.py {' '.join(sys.argv[1:])}")
except:
    error = True
    traceback.print_exc()
    input("Enter to reload")
    os.system(f"{python} main.py {' '.join(sys.argv[1:])}")
    exit()

if __name__ == '__main__':
    if not error:
        if len(sys.argv) == 1:
            try:
                srv = Server()
                srv.load()
            except:
                pass
        elif len(sys.argv) == 2:
            srv = Server()
            try:
                srv.start_project(sys.argv[1], True)
            except:
                with open(f"errors/{sys.argv[1]}.txt", "a+") as errors:
                    errors.write(f"\t{traceback.format_exc()}\n"
                                 f"________________________________________________________________________________________")
