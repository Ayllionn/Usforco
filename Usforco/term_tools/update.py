import os
import shutil
import zipfile
from rich.console import Console
from tkinter import Tk, filedialog
import platform

def get_os():
    if platform.system() == "Windows":
        return "win"
    elif platform.system() == "Linux":
        return "lin"
    else:
        # Si le système d'exploitation n'est ni Windows ni Linux
        return None

os_type = get_os()

console = Console()

whitelist = "term_tools/commandes/components/routine/database/messages".split("/")

def start(with_termtools=False):
    """
    windows commande*
    permet de mettre à jour le build grâce à un zip et sans toucher aux données ajoutées !
    with_termtools=False : si cette valeur est définie alors vous mettrez aussi a jour les tools du terminal.
    ATTENTION cependant ceci suprimera peut être des fichiers que vous auriez ajouté !
    """
    try:
        if os_type == "lin":
            print("Sous linux cette commande ne fonctionne pas encore désole")
            return

        temp_dir = "temp_update"

        root = Tk()
        root.withdraw()

        if with_termtools is not False:
            with_termtools = True
        if with_termtools is False:
            whitelist.append("term_tools")

        file_path = filedialog.askopenfilename(initialdir="/", filetypes=(("fichier compréssé", "*.zip"),("All files", "*.*")))

        if file_path:
            print("Chemin du fichier sélectionné :", file_path)
            zip_path = file_path
            del file_path
        else:
            print("Aucun fichier sélectionné")
            return

        root.destroy()

        # Extraction du contenu du fichier .zip dans un dossier temporaire
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        list_fichier = []

        for root, dirs, files in os.walk(temp_dir):
            root = root.split("\\")[2:]
            root = "\\".join(root)
            for file in files:
                if len(root) == 0:
                    list_fichier.append(os.getcwd() + "\\" + file)
                else:
                    list_fichier.append(os.getcwd()+ "\\" + root + "\\" + file)


        print("Fichiers contenue dans le fichier zip")
        [print(f) for f in list_fichier]

        print("")
        input("Press enter to continue (ctrl + C to end)")
        if os_type == "win":
            os.system("cls")
        else:
            os.system("clear")

        # Parcours de tous les fichiers et dossiers dans le dossier de destination, y compris les sous-dossiers
        for root, dirs, files in os.walk(os.getcwd()):
            whitelisted = False
            for f in root.split("\\"):
                if f in whitelist:
                    whitelisted = True
            if whitelisted:
                continue

            # Supprime les fichiers qui ne sont pas présents dans le dossier .zip
            for file in files:
                chemin_fichier = os.path.join(root, file)
                if root+'\\'+file not in list_fichier:
                    os.remove(chemin_fichier)
                    console.log(f"{file} : [red]supprimé.")

        # Copie les fichiers du dossier temporaire vers le dossier de destination
        for root, dirs, files in os.walk(temp_dir):
            whitelisted = False
            for f in root.split("\\"):
                if f in whitelist:
                    whitelisted = True
            if whitelisted:
                continue

            relative_path = os.path.relpath(root, temp_dir)
            destination_dir = os.path.join(os.getcwd(), relative_path)
            os.makedirs(destination_dir, exist_ok=True)

            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                shutil.copyfile(source_path, destination_path)
                console.log(f"{file} : [green]mis à jour !")

        # Suppression du dossier temporaire
        shutil.rmtree(temp_dir)

        print("")
        console.log("Mise à jour terminée !")

    except KeyboardInterrupt:
        try:
            shutil.rmtree(temp_dir)
        except:
            None