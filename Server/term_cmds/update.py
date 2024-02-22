import os
import zipfile
import shutil

def start(variables):
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
            with zipfile.ZipFile(os.getcwd()+"/temp.zip", 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            os.remove("temp.zip")
            print("Installed successfully")
            exit("updated successfully, serveur is clossing")

        for root, dirs, files in os.walk("./Usforco-main"):
            for file in files:
                if not os.path.exists(
                        "./" + "/".join(("./" + root.replace(os.getcwd(), "")).replace("\\", "/").split("/")[2:])):
                    os.makedirs(
                        "./" + "/".join(("./" + root.replace(os.getcwd(), "")).replace("\\", "/").split("/")[2:]))
                shutil.copy(root + "/" + file, os.getcwd() + "/" + "/".join(
                    ("./" + root.replace(os.getcwd(), "")).replace("\\", "/").split("/")[2:]))
