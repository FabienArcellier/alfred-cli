import logging
import os
import shutil
import sys
from typing import List, Any

import click

from alfred import ctx as alfred_ctx, manifest, echo, self_command, middlewares
from alfred import commands
from alfred.ctx import Context
from alfred.decorator import AlfredCommand
from alfred.exceptions import NotInitialized
from alfred.lib import ROOT_DIR
from alfred import logger


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
            alfred_ctx.mode_set(alfred_ctx.Mode.ListCommands)
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

        if alfred_ctx.mode_unknown():
            alfred_ctx.mode_set(alfred_ctx.Mode.RunCommand)

        project_dir = manifest.lookup_project_dir()
        _command = commands.lookup(cmd_name, project_dir=project_dir)
        if _command is None:
            return  None


        click_command = _command.command
        if click_command.name == cmd_name and isinstance(_command, AlfredCommand):
            alfred_ctx.stack_root_command(_command)
            _command.register_context(middlewares.command_middleware)
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
        if ctx.params['debug'] is True:
            _logger = logger.get_logger()
            _logger.setLevel(logging.DEBUG)

        display_obsolete_manifests()

        if ctx.params['version'] is True:
            self_command.version()

        if ctx.params['completion'] is True:
            self_command.completion()

        if ctx.params['check'] is True:
            self_command.check()

        if ctx.params['new'] is True:
            fullarg = ' '.join(args)
            if fullarg.strip() == "":
                self_command.new()
            else:
                self_command.new(fullarg)

        if len(args) > 0:
            cmd_output = self.resolve_command(ctx, args)

            if cmd_output is not None and alfred_ctx.should_use_external_venv():
                pty_support = False if alfred_ctx.test_runner_used() else True  # pylint: disable=simplifiable-if-expression
                alfred_ctx.invoke_through_external_venv(args, pty=pty_support)
            else:
                """
                The command is executed by click normally.
                """
                super().invoke(ctx)
        else:
            """
            The command is executed by click normally.
            """
            super().invoke(ctx)

    def parse_args(self, ctx: Context, args: List[str]) -> List[str]:
        if alfred_ctx.cli_args() is None:
            alfred_ctx.cli_args_set(args)
        return super().parse_args(ctx, args)


@click.command(cls=AlfredCli,
               help='alfred is a building tool to make engineering tasks easier to develop and to maintain')
@click.option("-d", "--debug", is_flag=True, help="display debug information like command runned and working directory")
@click.option("-v", "--version", is_flag=True, help="display the version of alfred")
@click.option("--new", is_flag=True, help="open a wizard to generate a new command")
@click.option("-c", "--check", is_flag=True, help="check the command integrity")
@click.option("--completion", is_flag=True, help="display instructions to enable completion for your shell")
@click.pass_context
def cli(ctx, debug: bool, version: bool, check: bool, completion: bool, new: bool):  # pylint: disable=unused-argument, too-many-arguments
    alfred_ctx.flag_set('--debug', debug)
    alfred_ctx.env_set('PYTHONUNBUFFERED', '1')
    alfred_ctx.directory_execution_set(os.getcwd())


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


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
