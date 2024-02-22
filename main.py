import os
import platform
from venv import create

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('cache'):
    print(f"Python version : {platform.python_version()}\n"
          f"Python recommanded version : 3.11")
    input("Press Enter to continue or CTRL+C to exit...")
    os.mkdir('cache')

try:
    with open('cache/env', "r+") as f:
        env = f.read().split("\n")[0]
        if not os.path.exists("cache/env"):
            raise ValueError()
        elif not os.path.exists(env):
            create(os.path.join(os.getcwd(), env), with_pip=True, upgrade_deps=True)
            print(env)
except:
    with open('cache/env', "w+") as f:
        env = input("Please enter your environment path\n> :")
        if os.path.exists(env):
            pass
        else:
            create(os.path.join(os.getcwd(), env), with_pip=True, upgrade_deps=True)

        print(env)
        f.write(env)

python = None

def check():
    global python

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

check()
if platform.system() == "Windows":
    os.system("cls")
elif platform.system() == "Linux":
    os.system("clear")
else:
    exit("Unsupported")

try:
    from Server import Server
    from Server.update import update as up

    if not os.path.exists('cache/update.txt'):
        with open("cache/update.txt", "w") as update:
            update.write(input("Do you want to auto-update at start ? [y/n] :"))
    up("y")
except:
    os.system(f"{python} main.py")

if __name__ == '__main__':
    try:
        srv = Server()
        srv.load()
    except:
        pass
