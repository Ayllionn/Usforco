import os
import zipfile

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

        shutil.rmtree(os.getcwd() + "/Server")
        shutil.rmtree(os.getcwd() + "/Data")
        for files in os.listdir("./Usforco-main"):
            shutil.copytree("./Usforco-main"+files, os.getcwd())
        shutil.rmtree("./Usforco-main")
