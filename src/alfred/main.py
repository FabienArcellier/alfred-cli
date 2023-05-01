import contextlib
import os
from functools import wraps
from typing import Optional, Union, List, Callable

import click
import plumbum
from click import BaseCommand
from click.exceptions import Exit
from plumbum import CommandNotFound, ProcessExecutionError, FG, local
from plumbum.machines import LocalCommand

from alfred import ctx as alfred_ctx, commands, echo, lib
from alfred.logger import get_logger


def call(command: LocalCommand, args: [str], exit_on_error=True) -> str:  #pylint: disable=inconsistent-return-statements
    """
    Most of the process run by alfred are supposed to stop
    if the excecution process is finishing with an exit code of 0

    There is one or two exception as the execution of migration by alembic through honcho.
    exit_on_error allow to manage them

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> output = alfred.call(echo, ["hello", "world"])
    >>> print(output)
    >>> # show `hello world`


    :param command: shell program to execute
    :param exit_on_error: break the flow if the exit code is different of 0 (active by default)
    """
    try:
        logger = get_logger()
        complete_command = command[args]
        working_directory = os.getcwd()
        logger.debug(f'{complete_command} - wd: {working_directory}')
        output = complete_command()

        """
        the output of the command is already parsed but the parsing is
        not usable on some command. I prefer to have a full stdout and delegate the parsing of stdout
        further
        """
        return "".join(output)
    except ProcessExecutionError as exception:
        if exit_on_error:
            click.echo(exception.stdout)
            raise Exit(code=exception.retcode) from exception


def project_directory() -> str:
    """
    Returns the project directory of alfred relative to the current command.
    This is the first parent where the `.alfred.yml` file is present.

    >>> @alfred.command("project_directory")
    >>> def project_directory_command():
    >>>     project_directory = alfred.project_directory()
    >>>     print(project_directory)
    """
    current_cmd = alfred_ctx.current_command()
    return current_cmd.project_dir


@contextlib.contextmanager
def env(**kwargs) -> None:
    """
    Assign environment variables in a build command

    >>> with alfred.env(ENV="prod"):
    >>>     echo = alfred.sh("echo")
    >>>     echo("hello world")

    This instruction should update the python environment and the environment
     from plumbum.
    """
    previous_environ = os.environ.copy()
    try:
        local.env.update(**kwargs)
        os.environ.update(kwargs)
        yield
    finally:
        local.env.clear()
        local.env.update(previous_environ)
        os.environ.clear()
        os.environ.update(previous_environ)


@click.pass_context
def invoke_command(ctx, command_label: str, **kwargs) -> None:
    click_command = None
    _commands = commands.list_all()
    origin_alfred_command = None
    for alfred_command in _commands:
        if ctx.command.name == alfred_command.name:
            origin_alfred_command = alfred_command

    plugin = origin_alfred_command.module
    plugin_click_command=_lookup_plugin_command(_commands, command_label, plugin)
    global_click_command=_lookup_global_command(_commands, command_label)

    available_plugins_commands = [command.original_name for command in _commands if command.module == plugin]
    available_global_commands = [command.name for command in _commands]
    if plugin_click_command is None and global_click_command is None:
        message = [
            f"command {command_label} does not exists.",
            f"Available plugin commands for plugin `{plugin}`: {available_plugins_commands}",
            f"Available global commands: {available_global_commands}",
        ]

        raise click.ClickException("\n".join(message))

    if plugin_click_command:
        click_command = plugin_click_command
    elif global_click_command:
        click_command = global_click_command

    echo.subcommand(f"$ alfred {click_command.name} : {click_command.help}")
    with alfred_ctx.stack_subcommand(origin_alfred_command):
        ctx.invoke(click_command, **kwargs)

class pythonpath:  #pylint: disable=invalid-name
    """
    Add the project folder, i.e. the root folder which corresponds to the alfred command used,
    to pythonpath to make available the packages present at this level.

    >>> @alfred.command()
    >>> @alfred.pythonpath()
    >>> def my_command():
    >>>     pass

    It is possible to add other directories to the pythonpath with the `directories` parameter.
    The path of the added folders is relative to the root folder of the alfred command used, ie
    the location of the `.alfred.yml` file.

    >>> @alfred.command()
    >>> @alfred.pythonpath(['src'])
    >>> def my_command():
    >>>     pass
    """

    def __init__(self, directories: List[str] = None, append_project=True):
        """
        manage the case where the decorator is used without parenthesis

        """
        if isinstance(directories, Callable):
            raise TypeError("alfred.pythonpath decoratore must be called with parenthesis as @alfred.pythonpath()")

        self.directories = directories
        self.append_project = append_project
        self._generator = None

    def __enter__(self):
        self._generator = _pythonpath(self.directories, self.append_project)
        self._generator.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._generator.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _pythonpath(self.directories, self.append_project):
                return func(*args, **kwargs)

        return wrapper


@contextlib.contextmanager
def _pythonpath(directories: List[str] = None, append_project=True) -> None:
    """
    See the pythonpath class above which implements the pattern
    to support a decorator and a context manager.
    """
    alfred_ctx.assert_in_command("alfred.pythonpath")

    if directories is None:
        directories = []

    _pythonpath = os.environ.get("PYTHONPATH", "").split(':')
    root_directory = project_directory()
    real_directories = [os.path.realpath(directory) for directory in directories]

    if append_project:
        real_directories += [root_directory]

    new_pythonpath = ":".join(real_directories + _pythonpath)
    with lib.override_pythonpath(new_pythonpath):
        yield


def sh(command: Union[str, List[str]], fail_message: str = None) -> LocalCommand:  # pylint: disable=invalid-name
    """
    Load a shell program from the local system. If the command does not exists, it
    will show an error `fail_message` to the console.

    If many commands are provided as command name, it will try the command one by one
    until one of them is present on the system. This behavior is require when you target
    different platform for example (Ubuntu is using `open` to open an url, when MacOs support `xdg-open`
    with the same behavior)

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> alfred.run(echo, ["hello", "world"])


    >>> open = alfred.sh(["open", "xdg-open"], "Either open, either xdg-open is missing on your system. Are you using a compatible platform ?")  # pylint: disable=line-too-long
    >>> alfred.run(open, "http://www.github.com")

    :param command: command or list of command name to lookup
    :param fail_message: failure message show to the user if no command has been found
    :return: a command you can use with alfred.run
    """
    if isinstance(command, str):
        command = [command]

    shell_command = None
    for _command in command:
        try:
            shell_command = plumbum.local[_command]
            break
        except CommandNotFound:
            continue

    if not shell_command:
        complete_fail_message = f" - {fail_message}" if fail_message is not None else ""
        raise click.ClickException(f"unknow command {command}{complete_fail_message}")

    return shell_command


def run(command: LocalCommand, args: [str], exit_on_error=True) -> None:
    """
    Most of the process run by alfred are supposed to stop
    if the excecution process is finishing with an exit code of 0

    There is one or two exception as the execution of migration by alembic through honcho.
    exit_on_error allow to manage them

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> alfred.run(echo, ["hello", "world"])

    The flag exitè
    >>> ls = alfred.sh("ls", "ls is missing on your system")
    >>> mv = alfred.sh("mv", "mv is missing on your system")
    >>> alfred.run(ls, ["/var/yolo"], exit_on_error=False)
    >>> alfred.run(mv, ["/var/yolo", "/var/yolo1"], exit_on_error=False)


    :param command: shell program to execute
    :param exit_on_error: break the flow if the exit code is different of 0 (active by default)
    """
    try:
        logger = get_logger()
        complete_command = command[args]
        working_directory = os.getcwd()
        logger.debug(f'{complete_command} - wd: {working_directory}')
        complete_command & FG  # pylint: disable=pointless-statement
    except ProcessExecutionError as exception:
        if exit_on_error:
            raise Exit(code=exception.retcode) from exception


def _lookup_plugin_command(all_commands, command_label, plugin) -> Optional[BaseCommand]:
    click_command = None
    for alfred_command in all_commands:
        if alfred_command.original_name == command_label and alfred_command.module == plugin:
            click_command = alfred_command.command
    return click_command


def _lookup_global_command(all_commands, command_label) -> Optional[BaseCommand]:
    click_command = None
    for alfred_command in all_commands:
        if alfred_command.name == command_label:
            click_command = alfred_command.command
    return click_command
