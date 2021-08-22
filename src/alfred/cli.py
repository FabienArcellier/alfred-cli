import os
import shutil
from typing import List, Iterator, Any

import click

from alfred.decorator import AlfredCommand, ALFRED_COMMANDS
from alfred.main import lookup_alfred_configuration
from alfred.lib import import_python, list_python_modules, ROOT_DIR


@click.command('init')
def init():
    if os.path.isfile('.alfred.yml'):
        raise click.ClickException(".alfred.yml already exists in this directory")

    os.makedirs('alfred')
    shutil.copy(os.path.join(ROOT_DIR, 'resources', '.alfred.yml'), '.alfred.yml')
    shutil.copy(os.path.join(ROOT_DIR, 'resources', 'cmd.py'), os.path.join('alfred', 'cmd.py'))


class AlfredCli(click.MultiCommand):

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)
        self._commands_loaded = False

    def list_commands(self, ctx):
        self.load_commands()
        _list_commands = []
        for command in self._list_commands_from_plugins():
            click_command = command.command
            _list_commands.append(click_command.name)

        _list_commands.sort()
        return _list_commands

    def get_command(self, ctx, cmd_name):
        if cmd_name == 'init':
            return init

        self.load_commands()

        for command in self._list_commands_from_plugins():
            click_command = command.command
            if click_command.name == cmd_name:
                return click_command

        return None

    def load_commands(self):
        if not self._commands_loaded:
            for command in self._list_commands_from_plugins():
                ALFRED_COMMANDS.append(command)

            self._commands_loaded = True

    def _list_commands_from_plugins(self) -> Iterator[AlfredCommand]:
        for plugin in self._plugins_folder():
            folder_path = plugin["path"]
            for python_path in list_python_modules(folder_path):
                prefix = "" if "prefix" not in plugin else plugin['prefix']
                result = import_python(python_path)
                list_commands = [elt for elt in result.values() if isinstance(elt, AlfredCommand)]
                for command in list_commands:
                    command.plugin = folder_path
                    command.command.name = f"{prefix}{command.name}"
                    yield command

    def _plugins_folder(self) -> List:
        alfred_configuration = lookup_alfred_configuration()
        return alfred_configuration["plugins"]


cli = AlfredCli(help='alfred is a building tool to make engineering tasks easier to develop and to maintain')

if __name__ == '__main__':
    cli()
