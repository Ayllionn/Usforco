import os

try:
    import discord
except:
    os.system("pip install discord")

from Server import Serveur

if __name__ == '__main__':
    srv = Serveur()
    srv.load()
