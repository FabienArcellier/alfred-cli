import contextlib
import logging
import os
import shutil
import sys
from typing import List, Any, Generator

import click
from click.exceptions import Exit

import alfred
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

    shutil.copy(os.path.join(ROOT_DIR, 'resources', '.alfred.toml'), '.alfred.toml')

    if not os.path.isdir('alfred'):
        os.makedirs('alfred', exist_ok=True)
        shutil.copy(os.path.join(ROOT_DIR, 'resources', 'cmd.py'), os.path.join('alfred', 'cmd.py'))


class AlfredCli(click.MultiCommand):

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)
        self._commands_loaded = False
        self._commands: List[AlfredCommand] = []

    def list_commands(self, ctx):
        try:
            _list_commands = []
            project_dir = manifest.lookup_project_dir()
            _commands = commands.list_all(project_dir)
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

    def get_command(self, ctx, cmd_name: str):
        if cmd_name == 'init':
            return init

        project_dir = manifest.lookup_project_dir()
        _command = commands.lookup(cmd_name, project_dir=project_dir)
        if _command is None:
            return  None


        click_command = _command.command
        if click_command.name == cmd_name and isinstance(_command, AlfredCommand):
            alfred_ctx.stack_root_command(_command)
            _command.register_context(_context_middleware)
            return click_command

        if click_command.name == cmd_name and isinstance(_command, commands.AlfredSubprojectCommand):
            alfred_ctx.stack_root_command(_command)
            return click_command

        return None

    def invoke(self, ctx: Context) -> Any:
        """
        The invocation of a command in alfred depends on the location of the targeted alfred command.

        In case it is in a subproject with its own venv, the command must be invoked in the interpreter associated 7
        with the subproject. Otherwise, the command is invoked in the current interpreter.
        """

        """
        Invoking an alfred command may run with a different interpreter than
        the one a developer first invoked alfred with.

        From the command, if it is played with the wrong interpreter, alfred restarts itself with the target interpreter.
        """
        args = [*ctx.protected_args, *ctx.args]
        if ctx.params['version'] is True:
            echo.message(f"{alfred.__version__}")
            raise Exit(code=0)

        if len(args) > 0:
            cmd_output = self.resolve_command(ctx, args)

            if cmd_output is not None and alfred_ctx.should_use_external_venv():
                alfred_ctx.invoke_through_external_venv(args)
                return

        """
        The command is executed by click normally.
        """
        super().invoke(ctx)


@click.command(cls=AlfredCli,
               help='alfred is a building tool to make engineering tasks easier to develop and to maintain')
@click.option("-d", "--debug", is_flag=True, help="display debug information like command runned and working directory")
@click.option("-v", "--version", is_flag=True, help="display the version of alfred")
def cli(debug: bool, version: bool):  # pylint: disable=unused-argument
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
    the context code is executed before executing
    the user's target command.
    """
    pathsep = os.pathsep
    pythonpath = os.environ.get("PYTHONPATH", "")
    if manifest.pythonpath_project_root():
        _pythonpath = pythonpath.split(pathsep)
        root_directory = project_directory()
        _pythonpath.append(root_directory)
        pythonpath = pathsep.join(_pythonpath)

    extensions = manifest.pythonpath_extends()
    if len(extensions) > 0:
        _pythonpath = pythonpath.split(pathsep)
        root_directory = project_directory()
        for extension in extensions:
            if os.path.isabs(extension):
                _pythonpath.append(extension)
            else:
                _pythonpath.append(os.path.join(root_directory, extension))

        pythonpath = pathsep.join(_pythonpath)

    with override_pythonpath(pythonpath):
        yield


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
