import logging
import os
import shutil
from typing import List, Any

import click
from plumbum import local

from alfred.decorator import AlfredCommand, ALFRED_COMMANDS
from alfred.main import lookup_alfred_configuration
from alfred.logger import logger
from alfred.lib import import_python, list_python_modules, ROOT_DIR, InvalidPythonModule, print_error
from alfred.type import Environment

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
        self._commands: List[AlfredCommand] = []

    def list_commands(self, ctx):
        _list_commands = []
        for command in self._list_commands_from_plugins():
            click_command = command.command
            _list_commands.append(click_command.name)

        _list_commands.sort()
        return _list_commands

    def get_command(self, ctx, cmd_name):
        if cmd_name == 'init':
            return init

        for command in self._list_commands_from_plugins():
            click_command = command.command
            if click_command.name == cmd_name:
                alfred_configuration = lookup_alfred_configuration()
                for environment in alfred_configuration.environments():
                    local.env[environment.key] = environment.value

                return click_command

        return None

    def _list_commands_from_plugins(self) -> List[AlfredCommand]:
        if self._commands_loaded:
            return self._commands

        _commands = []
        for plugin in self._plugins_folder():
            folder_path = plugin["path"]
            for python_path in list_python_modules(folder_path):
                prefix = "" if "prefix" not in plugin else plugin['prefix']
                try:
                    result = import_python(python_path)
                    list_commands = [elt for elt in result.values() if isinstance(elt, AlfredCommand)]
                    for command in list_commands:
                        command.plugin = folder_path
                        command.command.name = f"{prefix}{command.name}"
                        _commands.append(command)
                        ALFRED_COMMANDS.append(command)
                except InvalidPythonModule as exception:
                    print_error(str(exception))

        self._commands_loaded = True
        self._commands = _commands
        return self._commands

    def _environments(self) -> List[Environment]:
        alfred_configuration = lookup_alfred_configuration()
        return alfred_configuration.environments()

    def _plugins_folder(self) -> List:
        alfred_configuration = lookup_alfred_configuration()
        return alfred_configuration.plugins()


@click.command(cls=AlfredCli,
               help='alfred is a building tool to make engineering tasks easier to develop and to maintain')
@click.option("-d", "--debug", is_flag=True, help="display debug information as run command and working directory")
def cli(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
