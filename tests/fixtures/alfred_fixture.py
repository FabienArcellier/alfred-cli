import contextlib
from collections import namedtuple
from typing import List

from click import BaseCommand
from click.testing import CliRunner

import alfred
from alfred.cli import cli
from alfred import commands, ctx

CliResult = namedtuple('CliResult', ['exit_code', 'stdout', 'stderr'])


def invoke(args: List[str]) -> CliResult:
    """
    simulates invoking alfred from the command line.

    >>> exit_code, stdout, stderr = alfred_fixture.invoke(["--help"])

    If the command line invocation raises an exception, this fixture also throws it.
    """
    alfred.commands.cache_clear()

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, args)
    if result.exception is not None and not isinstance(result.exception, SystemExit):
        raise result.exception

    return CliResult(result.exit_code, result.stdout, result.stderr)


def invoke_click(command: BaseCommand, args: List[str] = None) -> CliResult:
    """
    Invokes a click command. This fixture allows to test features of alfred which need to be executed
    through click to work properly like alfred.invoke_command.

    >>> @click.command
    >>> def click_wrapper():
    >>>     print("hello world")
    >>>
    >>> exit_code, stdout, stderr = alfred_fixture.invoke_click(click_wrapper)

    If the command line invocation raises an exception, this fixture also throws it.
    """
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(command, args)

    if result.exception is not None and not isinstance(result.exception, SystemExit):
        raise result.exception

    return CliResult(result.exit_code, result.stdout, result.stderr)


def setup_context():
    """
    sets up a new independent execution context for a test

    >>> class TestCli(unittest.TestCase):
    >>>
    >>>     def setUp(self) -> None:
    >>>         self.context = alfred_fixture.setup_context()

    >>>     def tearDown(self) -> None:
    >>>         alfred_fixture.teardown_context(self.context)
    """
    context = use_new_context()
    context.__enter__()
    return context


def teardown_context(context):
    context.__exit__(None, None, None)


@contextlib.contextmanager
def use_command_context(command_name: str):
    """
    Use the context of a command.

    :param command_name: The name of the command to use.
    :return: A context manager that will use the context of the command.
    """
    alfred.commands.cache_clear()

    with use_new_context():
        _commands = commands.list_all()
        command_exist = False
        for _command in _commands:
            if _command.name == command_name:
                command_exist = True
                ctx.stack_root_command(_command)
                yield
                break

        if not command_exist:
            raise ValueError(f"Command {command_name} not found in {[_command.name for _command in _commands]}")


@contextlib.contextmanager
def use_new_context():
    """
    sets up a new independent execution context for a test
    """
    with ctx.use_new_context():
        ctx.test_runner_use(True)
        yield
