"""
This module exposes functions that manage the execution context of a command,
such as the current command, its parents, ...
"""
import contextlib
import copy
import dataclasses
from typing import List, Optional

from click.exceptions import Exit


from alfred import interpreter, logger, echo
from alfred.decorator import AlfredCommand
from alfred.exceptions import NotInCommand

class Mode:
    ListCommands = "list_commands"
    RunCommand = "run_command"
    Unknown = "unknown"

@dataclasses.dataclass
class InvocationContext:
    """
    The invocation context represents Alfred's summon information.

    Once written, its attributes, once written, remain constant. If alfred is invoked in a subproject, 7
    the invocation context is loaded from a file written with the parent's pid.

    Attributes must be primitive types to be serializable.
    """
    directory_execution: Optional[str] = None
    args: Optional[List[str]] = None
    mode: str = Mode.Unknown
    flag: List[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Context:
    commands_stack: List[AlfredCommand] = dataclasses.field(default_factory=list)

    @property
    def running(self) -> bool:
        return len(self.commands_stack) > 0

_invocation_context = InvocationContext()
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


def command_run() -> bool:
    return _invocation_context.mode == Mode.RunCommand

def cli_args_set(args: List[str]) -> None:
    _invocation_context.args = copy.copy(args)


def cli_args() -> Optional[List[str]]:
    return _invocation_context.args

def directory_execution_set(directory: str) -> None:
    _invocation_context.directory_execution = directory


def directory_execution() -> Optional[str]:
    return _invocation_context.directory_execution

def flag_set(flag: str, enable: bool) -> None:
    """
    configure flag to forward to interpreter when invoking a command
    """
    if enable and flag not in _invocation_context.flag:
        _invocation_context.flag.append(flag)

def invocation_options() -> List[str]:
    """
    recomposes the list of invocation options (flags + options).

    Options management is missing because Alfred is not using it at the moment.
    """
    return _invocation_context.flag


def mode_unknown() -> str:
    return _invocation_context.mode == Mode.Unknown


def mode_set(mode: str) -> None:
    logger.debug(f"mode set '{mode}'")
    _invocation_context.mode = mode


def invoke_through_external_venv(args: List[str]) -> None:
    """
    Invokes the current alfred command in its own virtual environment.

    """
    alfred_cmd = current_command()
    venv = interpreter.venv_lookup(alfred_cmd.project_dir)
    exit_code, _, stderr = interpreter.run_module(module='alfred.cli', venv=venv, args=args)

    if exit_code != 0:
        echo.error(stderr)
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
        venv = interpreter.venv_lookup(alfred_cmd.project_dir)

        if venv is not None and interpreter.venv_get() != venv:
            logger.debug(f"alfred interpreter - current venv: {interpreter.venv_get()}")
            logger.debug(f"alfred interpreter - expected venv: {venv}")
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
    Adds a new command to the current command stack.

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
    global _context, _invocation_context # pylint: disable=global-statement
    previous_context = _context
    previous_invocation_context = _invocation_context
    try:
        _context = Context()
        _invocation_context = InvocationContext()
        yield
    finally:
        _context = previous_context
        _invocation_context = previous_invocation_context
