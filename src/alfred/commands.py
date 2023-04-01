from typing import List, Dict

from alfred import manifest
from alfred.domain.command import AlfredCommand
from alfred.lib import list_python_modules, import_python, InvalidPythonModule, print_error

ALFRED_COMMANDS: List[AlfredCommand] = []


def list_all() -> List[AlfredCommand]:
    if len(ALFRED_COMMANDS) > 0:
        return ALFRED_COMMANDS

    load_commands()

    return ALFRED_COMMANDS


def load_commands() -> None:
    """
    Loads all commands available in the project. This function retrieves the .alfred.yml manifest,
    analyzes the plugins present and loads the commands.

    The search for the manifest is done from the current directory. If the manifest is not found, the search continues
    and goes back to the parent folder.

    Once the commands are loaded, they are available in the ALFRED_COMMANDS global variable.

    >>> from alfred import commands
    >>> commands.load_commands()
    """
    _commands = []
    for plugin in list_plugins_folder():
        folder_path = plugin["path"]
        for python_path in list_python_modules(folder_path):
            prefix = "" if "prefix" not in plugin else plugin['prefix']
            try:
                result = import_python(python_path)
                list_commands = [elt for elt in result.values() if isinstance(elt, AlfredCommand)]
                for command in list_commands:
                    command.plugin = folder_path
                    command.path = folder_path
                    command.command.name = f"{prefix}{command.name}"
                    _commands.append(command)
                    ALFRED_COMMANDS.append(command)
            except InvalidPythonModule as exception:
                print_error(str(exception))


def list_plugins_folder() -> List[Dict[str, str]]:
    alfred_configuration = manifest.lookup()
    return alfred_configuration.plugins()


def clear():
    """
    Clean the existing commands. This method is dedicated to automatic
    testing. AlfredCli kept between two tests. If a list of commands
    has already been loaded, it will use it.

    >>> commands.clear()
    """
    ALFRED_COMMANDS.clear()
