"""
This module performs column loading operations from the manifest definition.
"""
import contextlib
import dataclasses
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
        return []

    def get_command(self, ctx: Context, cmd_name: str) -> t.Optional[Command]:
        pass


@dataclasses.dataclass
class Commands:
    commands: List[AlfredCommand] = dataclasses.field(default_factory=list)
    subprojects: List[str] = dataclasses.field(default_factory=list)

    @property
    def loaded(self) -> bool:
        return len(self.commands) > 0


_commands = Commands()


def list_all() -> List[AlfredCommand]:
    if _commands.loaded:
        return _commands.commands

    load_commands()

    return _commands.commands


def load_commands() -> None:
    """
    Loads all commands available in the project. This function retrieves the .alfred.yml manifest,
    analyzes the plugins present and loads the commands.

    The search for the manifest is done from the current directory. If the manifest is not found, the search continues
    and goes back to the parent folder.

    Once the commands are loaded, they are available in _commands global variable.

    >>> from alfred import commands
    >>> commands.load_commands()
    """
    _commands.commands = []
    _manifest = manifest.lookup()
    for pattern in manifest.project_commands(_manifest):
        prefix = manifest.prefix()
        for python_module in list_python_modules(pattern):
            module = import_python(python_module)
            for command in module.values():
                if isinstance(command, AlfredCommand):
                    command.module = python_module
                    command.path = os.path.realpath(python_module)
                    command.command.name = f"{prefix}{command.name}"
                    _commands.commands.append(command)

    _commands.subprojects = []
    subprojects_glob = manifest.subprojects(_manifest)
    for subproject in subprojects_glob:
        directories = glob.glob(subproject)
        for directory in directories:
            if os.path.isdir(directory) and manifest.contains_manifest(directory):
                _subproject_manifest = manifest.lookup(directory)
                command = AlfredCommand()
                command.command = AlfredSubprojectCommand(name=manifest.name(_subproject_manifest),
                                                          help=manifest.description(_subproject_manifest),
                                                          path=directory)
                command.path = directory
                _commands.commands.append(command)

@contextlib.contextmanager
def use_new_context() -> None:
    """
    This context manager is dedicated to unit testing. It allows to reset the
    context to its initial state.

    >>> with commands.use_new_context():
    >>>     pass
    """
    global _commands # pylint: disable=global-statement
    previous_context = _commands
    _commands = Commands()
    yield
    _commands = previous_context
