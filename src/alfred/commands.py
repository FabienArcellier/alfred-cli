"""
Ce module fournit des fonctions pour charger les commandes d'un projet
alfred et de ses sous projets.
"""
import glob
import os
import typing as t
from functools import lru_cache
from typing import List

import click
from click import Context, Command

from alfred import manifest, echo
from alfred.domain.command import AlfredCommand
from alfred.lib import list_python_modules, import_python, InvalidCommandModule

class AlfredSubprojectCommand(click.MultiCommand):

    def __init__(self, *args, **attrs: t.Any):
        if "path" in attrs:
            self.path = attrs["path"]
            del attrs["path"]

        super().__init__(*args, **attrs)

    def list_commands(self, ctx: Context) -> t.List[str]:
        all_commands = list_all(self.path)
        return [command.name for command in all_commands]

    def get_command(self, ctx: Context, cmd_name: str) -> t.Optional[Command]:
        all_commands = list_all(self.path, show_error=False)
        for _command in all_commands:
            if _command.name == cmd_name:
                return _command.command

        return None


def cache_clear():
    """
    Reset the cache of commands and cause them to be loaded again when the module is called again.

    Resets the cache of the list_all function.
    """
    list_all.cache_clear()


@lru_cache(maxsize=None)
def list_all(project_dir: t.Optional[str] = None, show_error: bool = True) -> List[AlfredCommand]:
    """
    Loads all commands available in the project. This function retrieves the .alfred.yml manifest,
    analyzes the plugins present and loads the commands.

    The search for the manifest is done from the current directory. If the manifest is not found, the search continues
    and goes back to the parent folder.

    If a command module is invalid, for example, the python code has a syntax error, an error message is displayed in the terminal.
    The commands of the other modules remain executable.

    The result of this function is cached to avoid displaying the same error messages several times and
    to avoid loading the content of the commands several times during an execution.

    >>> from alfred import commands
    >>> commands.list_all()
    """
    subproject = None
    main_project_dir = manifest.lookup_project_dir()
    if project_dir is None:
        project_dir = main_project_dir

    if main_project_dir != project_dir:
        subproject = manifest.name(project_dir)

    commands = []
    for pattern in manifest.project_commands(project_dir):
        commands = _load_commands(commands, pattern, project_dir, subproject, show_error)

    subprojects_glob = manifest.subprojects(project_dir)
    for subproject in subprojects_glob:
        directories = glob.glob(subproject)
        for directory in directories:
            if os.path.isdir(directory) and manifest.contains_manifest(directory):
                commands = _load_subproject(commands, directory)

    return commands


def lookup(command: str or List[str], project_dir: t.Optional[str] = None) -> t.Optional[AlfredCommand]:
    """
    Searches for a command by its name.

    >>> _command = commands.lookup('build')
    >>> print(_command.project_dir)

    Searches for an order based on its project and its name.

    >>> _command = commands.lookup(["product1", 'build'])
    """
    if isinstance(command, str):
        command = [command]

    all_commands = list_all(project_dir, show_error=False)
    for _command in all_commands:
        if _command.name == command[0]:
            if isinstance(_command.command, AlfredSubprojectCommand):
                if len(command) == 1:
                    return _command

                subcommands = list_all(_command.project_dir)
                for subcommand in subcommands:
                    if subcommand.name == command[1]:
                        return subcommand

            return _command

    return None


def _load_commands(commands: list, pattern: str, project_dir: str, subproject: str, show_error: bool):
    pattern_path = os.path.join(project_dir, pattern)
    prefix = manifest.prefix(project_dir)
    for python_module in list_python_modules(pattern_path):
        module_path = os.path.join(project_dir, python_module)
        try:
            module = import_python(module_path)
            for command in module.values():
                if isinstance(command, AlfredCommand):
                    command.module = python_module
                    command.path = os.path.realpath(python_module)
                    command.project_dir = os.path.realpath(project_dir)
                    command.command.name = f"{prefix}{command.name}"
                    command.subproject = subproject
                    commands.append(command)
        except InvalidCommandModule as exception:
            if show_error:
                echo.error(str(exception))

    return commands


def _load_subproject(commands: list, directory: str) -> list:
    _subproject_manifest = manifest.lookup(directory)
    name = manifest.name(directory)
    if ' ' in name:
        echo.error(f"Subproject ignored: project name from {directory} cannot contain spaces, {name=}")
    else:
        command = AlfredCommand()
        command.command = AlfredSubprojectCommand(name=name,
                                                  help=manifest.description(directory),
                                                  path=os.path.realpath(directory))
        command.path = os.path.realpath(directory)
        command.project_dir = os.path.realpath(directory)
        commands.append(command)

    return commands
