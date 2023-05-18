import contextlib
import os
from functools import wraps
from typing import Union, List, Callable

import click
import plumbum
from click.exceptions import Exit
from plumbum import CommandNotFound, ProcessExecutionError, FG, local
from plumbum.machines import LocalCommand

from alfred import ctx as alfred_ctx, commands, echo, lib, manifest, alfred_command
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
def invoke_command(ctx, command: str or List[str], **kwargs) -> None:
    """
    Invokes a command as a subcommand.

    >>> alfred.invoke_command("test"])

    Command arguments are passed as named parameters.

    >>> alfred.invoke_command("hello_world", name="fabien"])

    To invoke a command from a sub-project, it is possible to pass the fullname of a command as
    an array as an argument.

    >>> alfred.invoke_command(["product1", "hello_world"], name="fabien"])
    """

    _calling_commmand = alfred_ctx.current_command()
    if _calling_commmand is not None:
        project_dir = _calling_commmand.project_dir
    else:
        project_dir = manifest.lookup_project_dir()

    _command = commands.lookup(command, project_dir)
    if _command is None:
        raise click.ClickException(f"command {command} does not exists.")


    click_command = _command.command
    if hasattr(click_command, "help"):
        echo.subcommand(f"$ alfred {click_command.name} : {click_command.help}")
    else:
        echo.subcommand(f"$ alfred {click_command.name}")

    with alfred_ctx.stack_subcommand(_command):
        args = alfred_command.format_cli_arguments(_command, kwargs)
        if alfred_ctx.should_use_external_venv():
            alfred_ctx.invoke_through_external_venv(args)
        else:
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


def run(command: LocalCommand, args: [str] = None, exit_on_error=True) -> None:
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
    if args is None:
        args = []

    try:
        logger = get_logger()
        complete_command = command[args]
        working_directory = os.getcwd()
        logger.debug(f'{complete_command} - wd: {working_directory}')
        complete_command & FG  # pylint: disable=pointless-statement
    except ProcessExecutionError as exception:
        if exit_on_error:
            raise Exit(code=exception.retcode) from exception


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
