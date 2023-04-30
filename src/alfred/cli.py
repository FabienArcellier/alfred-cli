import contextlib
import logging
import os
import shutil
import sys
from typing import List, Any, Generator

import click

from alfred import ctx as alfred_ctx, manifest, echo, project_directory
from alfred import commands
from alfred.ctx import Context
from alfred.decorator import AlfredCommand
from alfred.exceptions import NotInitialized
from alfred.lib import ROOT_DIR, override_pythonpath
from alfred.logger import logger


@click.command('init')
def init():
    display_obsolete_manifests()
    if manifest.contains_manifest():
        exit_on_error("manifest .alfred.toml already exists in this directory")

    os.makedirs('alfred')
    shutil.copy(os.path.join(ROOT_DIR, 'resources', '.alfred.toml'), '.alfred.toml')
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
            if click_command.name == cmd_name and isinstance(command, AlfredCommand):
                alfred_ctx.stack_root_command(command)
                command.register_context(_context_middleware)
                return click_command

            if click_command.name == cmd_name and isinstance(command, commands.AlfredSubprojectCommand):
                return click_command

        return None

    def invoke(self, ctx: Context) -> Any:
        """
        The invocation of a command in alfred depends on the location of the targeted alfred command.

        Dans le cas où elle est dans un sous-projet avec son propre venv, la commande doit être invoquée
        dans l'interpréteur associé au projet. Dans le cas contraire, la commande est invoquée dans l'interpréteur
        """
        return super().invoke(ctx)


@click.command(cls=AlfredCli,
               help='alfred is a building tool to make engineering tasks easier to develop and to maintain')
@click.option("-d", "--debug", is_flag=True, help="display debug information like command runned and working directory")
def cli(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)

    display_obsolete_manifests()


def display_obsolete_manifests():
    """
    Show a warning if obsolete manifest files are found.

    >>> cli.display_obsolete_manifests()
    """
    obsolete_manifests = manifest.lookup_obsolete_manifests()
    if len(obsolete_manifests) > 0:
        echo.warning(f"The following obsolete manifest files have been found: {obsolete_manifests}")


def exit_on_error(message: str, exit_code: int = 1):
    """
    Exit the program with a message.

    The exit code can be customized.

    >>> exit_on_error(".alfred.yml already exists in this directory")
    """
    exception = click.ClickException(message)
    exception.exit_code = exit_code
    raise exception


@contextlib.contextmanager
def _context_middleware() -> Generator[None, None, None]:
    """
    le code du contexte est exécuté avant d'exécuter la commande cible
    de l'utilisateur.
    """
    pythonpath = os.environ.get("PYTHONPATH", "")
    if manifest.python_path_project_root():
        _pythonpath = pythonpath.split(':')
        root_directory = project_directory()
        _pythonpath.append(root_directory)
        pythonpath = ":".join(_pythonpath)

    with override_pythonpath(pythonpath):
        yield


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
