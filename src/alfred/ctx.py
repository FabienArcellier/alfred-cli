"""
This module exposes functions that manage the execution context of a command,
such as the current command, its parents, ...
"""
import contextlib
import copy
import dataclasses
import os
import sys
from typing import List, Optional

from click.exceptions import Exit


from alfred import interpreter, logger, echo, manifest
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
    test_runner: bool = False

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


def invoke_through_external_venv(args: List[str], pty: bool = False) -> None:
    """
    Invokes the current alfred command in its own virtual environment.

    """
    alfred_cmd = current_command()
    venv = interpreter.venv_lookup(alfred_cmd.project_dir)
    if pty is True:
        exit_code = interpreter.run_module_as_pty(module='alfred.cli', venv=venv, args=args)
        if exit_code != 0:
            raise Exit(exit_code)

    else:
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


def env_pythonpath(project_dir: Optional[str] = None) -> str:
    """
    Constructs the PYTHONPATH environment variable from project settings and interpreter info.

    """
    if project_dir is None:
        project_dir = project_directory()

    pythonpath_extensions = []
    if manifest.lookup_parameter_project('pythonpath_project_root'):
        pythonpath_extensions.append(project_dir)
    pythonpath_extensions += manifest.lookup_parameter_project('pythonpath_extends')
    pythonpath = os.pathsep.join(sys.path)
    pythonpath = _include_path(pythonpath, pythonpath_extensions, project_dir)
    return pythonpath


def env_path(project_dir: Optional[str] = None):
    """
    Constructs the PATH environment variable from project settings and the os info.

    """
    if project_dir is None:
        project_dir = project_directory()

    path_extensions = manifest.lookup_parameter_project('path_extends', project_dir)
    path = os.environ.get('PATH', '')
    path = _include_path(path, path_extensions, project_dir)
    return path

def project_directory() -> str:
    """
    Returns the project directory of alfred relative to the current command.
    This is the first parent where the `.alfred.toml` file is present.

    >>> @alfred.command("project_directory")
    >>> def project_directory_command():
    >>>     project_directory = alfred.project_directory()
    >>>     print(project_directory)
    """
    return current_command().project_dir


def _include_path(path: str, path_extensions: List[str], root_directory: str) -> str:
    """
    Merges a path variable like the PATH or PYTHONPATH variable with an extension list.

    Extensions can be absolute or relative paths to the project root directory.

    >>> path = include_path('/usr/bin:/usr/local/bin', ['bin', '.venv/bin'])
    """
    if len(path_extensions) > 0:
        _path = path.split(os.pathsep)
        _path = list(reversed(_path))
        for extension in path_extensions:
            if os.path.isabs(extension):
                _path.append(extension)
            else:
                _path.append(os.path.join(root_directory, extension))

        _path = list(reversed(_path))
        path = os.pathsep.join(_path)
    return path


def test_runner_use(enabled: bool):
    """
    Active this flag to indicate that the test runner is being used.
    """
    _invocation_context.test_runner = enabled


def test_runner_used() -> bool:
    """
    Returns whether the test runner is being used.
    """
    return _invocation_context.test_runner


def env_set(env_var: str, value: str) -> None:
    """
    Sets an environment variable to a given value. If the variable is already set to the given value,
    nothing is done.

    """
    original_value = os.getenv(env_var)
    if original_value != value:
        logger.debug(f"alfred interpreter - force environment variable {env_var} to {value}")
        os.environ[env_var] = value
    else:
        logger.debug(f"alfred interpreter - keep environment variable {env_var} at {value}")
