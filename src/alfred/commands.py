"""
This module performs column loading operations from the manifest definition.
"""
import contextlib
import dataclasses
from typing import List, Dict

from alfred import manifest
from alfred.domain.command import AlfredCommand
from alfred.lib import list_python_modules, import_python


@dataclasses.dataclass
class Commands:
    commands: List[AlfredCommand] = dataclasses.field(default_factory=list)

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
    for pattern in manifest.project_commands_pattern():
        prefix = manifest.prefix()
        for python_module in list_python_modules(pattern):
            module = import_python(python_module)
            for command in module.values():
                if isinstance(command, AlfredCommand):
                    command.plugin = pattern
                    command.path = pattern
                    command.command.name = f"{prefix}{command.name}"
                    _commands.commands.append(command)

    # include the commands from the plugins
    # for plugin in manifest.project_commands_pattern():
    #     folder_path = plugin["path"]
    #     for python_path in list_python_modules(folder_path):
    #         prefix = "" if "prefix" not in plugin else plugin['prefix']
    #         try:
    #             result = import_python(python_path)
    #             list_commands = [elt for elt in result.values() if isinstance(elt, AlfredCommand)]
    #             for command in list_commands:
    #                 command.plugin = folder_path
    #                 command.path = folder_path
    #                 command.command.name = f"{prefix}{command.name}"
    #                 _commands.commands.append(command)
    #         except InvalidPythonModule as exception:
    #             print_error(str(exception))


def list_plugins_folder() -> List[Dict[str, str]]:
    return []


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
