import os
import zipfile

def start(variables):
    with open("./Server/version", "r", encoding="utf8") as version_file:
        version = version_file.read().split("\n")[0]
        version = version.split(".")

    last_version = os.popen("curl https://usforco.netlify.app/documentation/version.txt").read().split(".")

    print("Current version :", version)
    print("Last version :", last_version)

    update = False

    for v, v2 in zip(version, last_version):
        if v > v2:
            update = True

    if update:
        resp = input("An update is available. Do you want to install it? (y/n) ")
        if resp == "y":
            os.system("curl -o temp.zip https://github.com/Ayllionn/Usforco/archive/refs/heads/main.zip")
            with zipfile.ZipFile(os.getcwd()+"/temp.zip", 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            print("Installed successfully")
            exit("updated successfully, serveur is clossing")