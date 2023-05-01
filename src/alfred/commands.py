"""
This module performs column loading operations from the manifest definition.
"""
import glob
import os
import typing as t
from typing import List

import click
from click import Context, Command

from alfred import manifest
from alfred.domain.command import AlfredCommand
from alfred.lib import list_python_modules, import_python


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
        all_commands = list_all(self.path)
        for command in all_commands:
            if cmd_name == command.name:
                return command.command

        return None



def list_all(project_dir: t.Optional[str] = None) -> List[AlfredCommand]:
    """
    Loads all commands available in the project. This function retrieves the .alfred.yml manifest,
    analyzes the plugins present and loads the commands.

    The search for the manifest is done from the current directory. If the manifest is not found, the search continues
    and goes back to the parent folder.

    Once the commands are loaded, they are available in _commands global variable.

    >>> from alfred import commands
    >>> commands.list_all()
    """
    if project_dir is None:
        project_dir = manifest.lookup_project_dir()

    commands = []
    for pattern in manifest.project_commands(project_dir):
        pattern_path = os.path.join(project_dir, pattern)
        prefix = manifest.prefix(project_dir)
        for python_module in list_python_modules(pattern_path):
            module_path = os.path.join(project_dir, python_module)
            module = import_python(module_path)
            for command in module.values():
                if isinstance(command, AlfredCommand):
                    command.module = python_module
                    command.path = os.path.realpath(python_module)
                    command.project_dir = os.path.realpath(project_dir)
                    command.command.name = f"{prefix}{command.name}"
                    commands.append(command)

    subprojects_glob = manifest.subprojects(project_dir)
    for subproject in subprojects_glob:
        directories = glob.glob(subproject)
        for directory in directories:
            if os.path.isdir(directory) and manifest.contains_manifest(directory):
                _subproject_manifest = manifest.lookup(directory)
                command = AlfredCommand()
                command.command = AlfredSubprojectCommand(name=manifest.name(directory),
                                                          help=manifest.description(directory),
                                                          path=os.path.realpath(directory))
                command.path = os.path.realpath(directory)
                command.project_dir = os.path.realpath(directory)
                commands.append(command)

    return commands
