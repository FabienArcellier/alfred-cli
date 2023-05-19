"""
This module exposes functions that manage the execution context of a command,
such as the current command, its parents, ...
"""
import contextlib
import dataclasses
from typing import List, Optional

from click.exceptions import Exit

from alfred import manifest, interpreter
from alfred.decorator import AlfredCommand
from alfred.exceptions import NotInCommand
from alfred.logger import get_logger


@dataclasses.dataclass
class Context:
    commands_stack: List[AlfredCommand] = dataclasses.field(default_factory=list)

    @property
    def running(self) -> bool:
        return len(self.commands_stack) > 0


_context = Context()

def assert_in_command(instruction: str) -> None:
    """
    Throws an exception if an alfred command is not running

    >>> ctx.assert_in_command("alfred.pythonpath")
    :return:
    """
    if _context.running is False:
        raise NotInCommand(instruction)


def current_command() -> Optional[AlfredCommand]:
    """
    Retrieves the last running command.

    :return:
    """
    return _context.commands_stack[0] if _context.running else None


def invoke_through_external_venv(args: List[str]) -> None:
    """
    Invokes the current alfred command in its own virtual environment.

    """
    alfred_cmd = current_command()
    venv = manifest.lookup_venv(alfred_cmd.project_dir)
    exit_code, _, _ = interpreter.run_module(module='alfred.cli', venv=venv, args=args)

    if exit_code != 0:
        raise Exit(exit_code)


def root_command() -> Optional[AlfredCommand]:
    """
    Retrieves the root command causing the execution.

    :return:
    """
    return _context.commands_stack[-1] if _context.running else None


def should_use_external_venv() -> bool:
    """
    Checks whether the current command should run in its own virtual environment different from
    the one currently active.

    """
    alfred_cmd = current_command()
    if alfred_cmd is not None:
        venv = manifest.lookup_venv(alfred_cmd.project_dir)

        if venv is not None and interpreter.get_venv() != venv:
            _logger = get_logger()
            _logger.debug(f"alfred interpreter - current venv: {interpreter.get_venv()}")
            _logger.debug(f"alfred interpreter - expected venv: {venv}")
            return True

    return False


def stack_root_command(command: AlfredCommand) -> None:
    """
    Starts execution of a new command invoked from the shell. The command stack is
    expected to be empty at boot time.

    The command stack is cleared by the end of shell execution.

    >>> ctx.stack_root_command(command)
    """
    # assert len(_context.commands_stack) == 0, f"Commands are already running: {_context.commands_stack}"
    _context.commands_stack = [command]


@contextlib.contextmanager
def stack_subcommand(command: AlfredCommand) -> None:
    """
    Ajoute une nouvelle commande sur la pile des commandes en cours.
    Une fois l'exécution

    >>> with ctx.stack_subcommand(command):
    >>>     pass
    """
    _context.commands_stack.insert(0, command)
    yield
    _context.commands_stack.pop(0)


@contextlib.contextmanager
def use_new_context() -> None:
    """
    This context manager is dedicated to unit testing. It allows to reset the
    context to its initial state.

    >>> with ctx.use_new_context():
    >>>     pass
    """
    global _context # pylint: disable=global-statement
    previous_context = _context
    _context = Context()
    yield
    _context = previous_context
