import os
import shutil
import sys
import zipfile

def update(auto=None):
    if auto is not None:
        f = open('opt/update.txt', "r")
        if f.read().split("\n")[0] == "n":
            f.close()
            return
        f.close()

    with open("./Server/version", "r", encoding="utf8") as version_file:
        version = version_file.read().split("\n")[0]
        version = version.split(".")

    last_version = os.popen("curl https://raw.githubusercontent.com/Ayllionn/Usforco/main/Server/version").read().split(".")
    last_version = [int(i.split("\n")[0].replace(" ", "")) for i in last_version]
    version = [int(i.split("\n")[0].replace(" ", "")) for i in version]

    print("Current version :", version)
    print("Last version :", last_version)

    update = False

    for v, v2 in zip(version, last_version):
        if v < v2:
            update = True

    if update:
        if auto is None:
            resp = input("An update is available. Do you want to install it? (y/n) ")
        else:
            f = open('opt/update.txt', "r")
            resp = f.read().split("\n")[0]
            f.close()
        if resp == "y":
            os.system("curl -LJ -o temp.zip https://github.com/Ayllionn/Usforco/archive/refs/heads/main.zip")
            with zipfile.ZipFile(os.getcwd() + "/temp.zip", 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            os.remove("temp.zip")

            origin = "./Usforco-main"

            for root, dirs, files in os.walk(origin):
                for file in files:
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join(os.getcwd(), root[len(origin) + 1:], file)

                    if os.path.abspath(source_file) != os.path.abspath(destination_file):
                        destination_folder = os.path.dirname(destination_file)
                        if not os.path.exists(destination_folder):
                            os.makedirs(destination_folder)

                        shutil.copy(source_file, destination_file)

            shutil.rmtree(origin)
            python = sys.executable
            os.execl(python, python, *sys.argv)
