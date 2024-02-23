import os
import shlex
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from traceback import print_exc
from glob import glob
import importlib

console = Console()

class CommandNotFound(Exception):
    pass

class CustomTerminal:
    def __init__(self, terminal_name="Terminal by Ayllionne", search=None, panel=True, help_at_start=True, variable:dict=None, **kwargs):
        if search is None:
            search = Prompt.ask(
                "Voulez-vous que les commandes non trouvées soient demandées au système d'exploitation ?",
                choices=["o", "n"],
                default="n"
            )
        self.name = terminal_name
        self._search = search
        self._message = f"[green]┌── ([blue]{terminal_name}[/blue]) :\n└─[cyan]$ "
        self._commands = {
            "help": self._help_msg,
            "exit": self._exit,
            "para": self._para
        }
        self._default_cmds = self._commands.copy()
        self._true = True
        self.panel = panel
        for cle, value in kwargs.items():
            self.add_command(value, cle)

        self.help_at_start = help_at_start
        self.variable = variable

    def _help_msg(self, command=None):
        """Affiche le message d'aide du terminal ou la documentation d'une commande souhaitée"""
        if self.panel:
            console.print("[black]Terminal by Ayllionne")
        table = Table()
        table.add_column("Commandes")
        table.add_column("Description")
        if command is None:
            for cmd in self._commands:
                table.add_row(cmd, self._commands[cmd].__doc__)
                table.add_section()
        else:
            try:
                table.add_row(command, self._commands[command].__doc__)
            except KeyError:
                raise CommandNotFound(f"Commande '{command}' introuvable")
        console.print(table)
        return 0

    def _exit(self):
        """Permet de quitter ce terminal"""
        self._true = False
        return 0

    def add_command(self, fonction, name=None, default_cmd=False):
        if name is None:
            name = fonction.__name__
        if name in self._commands:
            raise ValueError(f"La commande '{name}' existe déjà")
        if default_cmd:
            self._default_cmds[name] = fonction
        self._commands[name] = fonction

    def command(self, _name=None, default_cmd=False):
        """
        pour passer avec une méthode en décorateur
        """
        def deco(func):
            if _name is None:
                name = func.__name__
            else:
                name = _name
            if name in self._commands:
                raise ValueError(f"La commande '{name}' existe déjà")
            if default_cmd:
                self._default_cmds[name] = func
            self._commands[name] = func
        return deco

    def _para(self, o_n=None):
        """Permet de changer les paramètres entrés au lancement du terminal
        :arg : n/o"""
        if o_n is None:
            self._search = Prompt.ask(
                "Voulez-vous que les commandes non trouvées soient demandées au système d'exploitation ?",
                choices=["o", "n"],
                default="n"
            )
        else:
            self._search = o_n
        return 0

    def start(self):
        if self.panel is True:
            panel = Panel("", title="Terminale Perso", subtitle="[black]by Ayllionne")
            console.print(panel)

        if self.help_at_start:
            self._help_msg()

        while self._true:
            cmd = console.input(self._message)
            cmd_args = shlex.split(cmd)
            try:
                cmd_name = cmd_args[0]
                cmd_args = cmd_args[1:]
            except IndexError:
                continue

            cmd_args_dict = {}
            deleters = []
            for e, v in enumerate(cmd_args):
                if v[:2] == "--":
                    deleters.append(v)
                    deleters.append(cmd_args[e+1])
                    cmd_args_dict.update({v[2:]:cmd_args[e+1]})

            for e in deleters:
                cmd_args.remove(e)
            del deleters

            try:
                if cmd_name in self._commands:
                    try:
                        if self.variable is not None and cmd_name not in self._default_cmds.keys():
                            cmd_args.insert(0, self.variable)
                        self._commands[cmd_name](*cmd_args, **cmd_args_dict)
                    except:
                        print_exc()
                        time.sleep(1)
                        self._help_msg(cmd_name)
                elif self._search == "o":
                    os.system(cmd)
                else:
                    raise CommandNotFound(f"Commande '{cmd_name}' introuvable")
            except Exception as e:
                console.print(f"[red]{e}")

    def exe(self, cmd):
        try:
            cmd_args = shlex.split(cmd)
            cmd_name = cmd_args[0]
            cmd_args = cmd_args[1:]
            if cmd_name in self._commands:
                return self._commands[cmd_name](*cmd_args)
        except Exception as e:
            if self._search == "o":
                os_cmd = os.popen(f"{cmd}")
                return os_cmd.read()
            else:
                return e

    def reset(self):
        self._commands.clear()
        self._commands = self._default_cmds.copy()

    def get_raw_cmds_files(self, directory=os.getcwd(), reset=False):
        """permet aux personne de faire des fichier .py dans un dossier particulier, le nom du fichier serra pris comme nom de commande
        et la UNIQUEMENT fonction start serra prise pour être associé a cette commande"""

        if reset:
            self.reset()

        files = glob(f"{directory}/*.py")

        for file_path in files:
            file_name = file_path.split("\\")[-1].split("/")[-1][:-3]

            compte = 0
            for d, a in zip(file_path, os.getcwd()):
                if d == a:
                    compte += 1
                else:
                    break

            module_acces = ".".join(file_path[compte+1:].split('\\')).replace("/", ".")
            module_acces = module_acces[:-3]

            module = importlib.import_module(module_acces)
            start_func = getattr(module, "start", None)

            if start_func and callable(start_func):
                self.add_command(start_func, file_name)
