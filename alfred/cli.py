from typing import List, Iterator

import click
from click import BaseCommand

from alfred.main import lookup_alfred_configuration
from alfred.lib import import_python, list_python_modules


class AlfredCli(click.MultiCommand):

    def list_commands(self, ctx):
        _list_commands = []
        for command in self._list_commands_from_plugins():
            _list_commands.append(command.name)

        _list_commands.sort()
        return _list_commands

    def get_command(self, ctx, cmd_name):
        for command in self._list_commands_from_plugins():
            if command.name == cmd_name:
                return command

        return None

    def _list_commands_from_plugins(self) -> Iterator[BaseCommand]:
        for plugin in self._plugins_folder():
            folder_path = plugin["path"]
            for python_path in list_python_modules(folder_path):
                result = import_python(python_path)
                list_commands = [elt for elt in result.values() if isinstance(elt, BaseCommand)]
                for command in list_commands:
                    command.name = command.name if "prefix" not in plugin else f"{plugin['prefix']}{command.name}"
                    yield command

    def _plugins_folder(self) -> List:
        alfred_configuration = lookup_alfred_configuration()
        return alfred_configuration["plugins"]




cli = AlfredCli(help='')

if __name__ == '__main__':
    cli()
