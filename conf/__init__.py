import os
import platform

PATH_DIR = f"{os.getcwd()}"
DB = f"{PATH_DIR}/DB/json_files/db.json"


if platform.system() == "Windows":
    OS = "win"
elif platform.system() == "Linux":
    OS = "lin"
else:
    OS = "jsp ou tu m'as mis la, mais t'abuse"
    print(OS)