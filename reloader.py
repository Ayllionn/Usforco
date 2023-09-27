import os
from platform import system

if system() == "Windows":
    os.system("start py manage.py")