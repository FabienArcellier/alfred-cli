import logging
import os
import shutil
import sys
from typing import List, Any

import click
from plumbum import local

from alfred import ctx as alfred_ctx, manifest
from alfred import commands
from alfred.decorator import AlfredCommand
from alfred.exceptions import NotInitialized
from alfred.lib import ROOT_DIR
from alfred.logger import logger


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
        try:
            _list_commands = []
            _commands = commands.list_all()
            for command in _commands:
                click_command = command.command
                _list_commands.append(click_command.name)

            _list_commands.sort()
            return _list_commands
        except NotInitialized as exception:
            # When the project is not recognize as alfred, we show a error message
            # to ask the user to initialized its directory
            click.echo(click.style(f"{exception.message}", fg='red'))
            sys.exit(2)

    def get_command(self, ctx, cmd_name):
        if cmd_name == 'init':
            return init

        _commands = commands.list_all()
        for command in _commands:
            click_command = command.command
            if click_command.name == cmd_name:
                alfred_ctx.stack_root_command(command)
                alfred_manifest = manifest.lookup()
                for environment in alfred_manifest.environments():
                    local.env[environment.key] = environment.value

                return click_command

        return None


@click.command(cls=AlfredCli,
               help='alfred is a building tool to make engineering tasks easier to develop and to maintain')
@click.option("-d", "--debug", is_flag=True, help="display debug information like command runned and working directory")
def cli(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
