import os
import platform
import shutil
import zipfile
from venv import create

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("./Server/version", "r", encoding="utf8") as version_file:
    version = version_file.read().split("\n")[0]
    version = version.split(".")

last_version = os.popen("curl https://usforco.netlify.app/documentation/version.txt").read().split(".")
last_version = [int(i.replace("\n", "").replace(" ", "")) for i in last_version]
version = [int(i.replace("\n", "").replace(" ", "")) for i in version]

print("Current version :", version)
print("Last version :", last_version)

update = False

for v, v2 in zip(version, last_version):
    if v < v2:
        update = True

if update:
    resp = input("An update is available. Do you want to install it? (y/n) ")
    if resp == "y":
        os.system("curl -LJ -o temp.zip https://github.com/Ayllionn/Usforco/archive/refs/heads/main.zip")
        with zipfile.ZipFile(os.getcwd() + "/temp.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.remove("temp.zip")

    origin = "./Usforco-main"

    for root, dirs, files in os.walk(origin):
        for file in files:
            # Chemin complet du fichier d'origine
            source_file = os.path.join(root, file)
            # Chemin complet du fichier de destination
            destination_file = os.path.join(os.getcwd(), root[len(origin) + 1:], file)

            # Vérifier si le fichier de source et de destination sont les mêmes
            if os.path.abspath(source_file) != os.path.abspath(destination_file):
                # Vérifier si le dossier de destination existe, sinon le créer
                destination_folder = os.path.dirname(destination_file)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                # Copier le fichier
                shutil.copy(source_file, destination_file)
    shutil.rmtree(origin)

if not os.path.exists('cache'):
    print(f"Python version : {platform.python_version()}\n"
          f"Python recommanded version : 3.11")
    input("Press Enter to continue or CTRL+C to exit...")
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
except:
    os.system(f"{python} main.py")

if __name__ == '__main__':
    try:
        srv = Server()
        srv.load()
    except:
        pass
