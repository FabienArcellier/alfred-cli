import contextlib
import os
from functools import wraps
from typing import Union, List, Callable, Optional, Tuple

import click
from click.exceptions import Exit

from alfred import ctx as alfred_ctx, commands, echo, lib, manifest, alfred_command, process

def CMD_RUNNING():  #pylint: disable=invalid-name
    """
    Isolates heavy dependencies to speed up command discovery on ``alfred`` and ``alfred --help``.

    They are loaded when the user executes a module module command.

    >>> if alfred.CMD_RUNNING():
    >>>     import torch
    >>>
    >>> @alfred.command("use_torch")
    >>> def use_torch():
    >>>     example_list = [1,2,3]
    >>>     x = torch.tensor(example_list)
    >>>     print(x)
    """
    return alfred_ctx.command_run()

def project_directory() -> str:
    """
    Returns the project directory of alfred relative to the current command.
    This is the first parent where the `.alfred.toml` file is present.

    >>> @alfred.command("project_directory")
    >>> def project_directory_command():
    >>>     project_directory = alfred.project_directory()
    >>>     print(project_directory)
    """
    return alfred_ctx.project_directory()


def execution_directory() -> str:
    """
    Returns the directory from which the command is executed.

    The working folder return by ``os.getcwd`` is set to the project directory inside a command.
    This allows to change the path in commands knowing where the working directory is.

    The project directory is the first parent where the `.alfred.toml` file is present.

    >>> @alfred.command("execution_directory")
    >>> def execution_directory_command():
    >>>     execution_directory = alfred.execution_directory()
    >>>     print(execution_directory)
    """
    return alfred_ctx.directory_execution()


@contextlib.contextmanager
def env(**kwargs) -> None:
    """
    Assign environment variables in a command

    >>> with alfred.env(ENV="prod"):
    >>>     echo = alfred.sh("echo")
    >>>     echo("hello world")
    """
    with lib.override_envs(**kwargs):
        yield


@click.pass_context
def invoke_command(ctx, command: str or List[str], **kwargs) -> None:
    """
    Invokes an existing command as a subcommand. This instruction offer the perfect way to build pipelines

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
        os.chdir(project_dir)
        args = alfred_command.format_cli_arguments(_command, kwargs)
        if alfred_ctx.should_use_external_venv():
            alfred_ctx.invoke_through_external_venv(args)
        else:
            previous_directory = os.getcwd()
            try:
                ctx.invoke(click_command, **kwargs)
            finally:
                os.chdir(previous_directory)

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


def sh(command: Union[str, List[str]], fail_message: str = None) -> process.Command:  # pylint: disable=invalid-name
    """
    Load an executable program from the local system. If the command does not exists, it
    will show an error `fail_message` to the console.

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> alfred.run(echo, ["hello", "world"])

    If many commands are provided as command name, it will try the command one by one
    until one of them is present on the system. This behavior is require when you target
    different platform for example (Ubuntu is using `open` to open an url, when MacOs support `xdg-open`
    with the same behavior)

    >>> open = alfred.sh(["open", "xdg-open"], "Either open, either xdg-open is missing on your system. Are you using a compatible platform ?")  # pylint: disable=line-too-long
    >>> alfred.run(open, "http://www.github.com")

    :param command: command or list of command name to lookup
    :param fail_message: failure message show to the user if no command has been found
    :return: a command you can use with alfred.run
    """
    return process.sh(command, fail_message)


def run(command: Union[str, process.Command], args: Optional[Union[str, List[str]]] = None, exit_on_error=True) -> Tuple[int, str, str]:
    """
    Most of the process run by alfred are supposed to stop
    if the excecution process is finishing with an exit code of 0

    There is one or two exception as the execution of migration by alembic through honcho.
    exit_on_error allow to manage them

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> alfred.run(echo, ["hello", "world"])

    The flag ``exit_on_error`` is set to True by default. If you want to ignore the exit code
    and continue the execution even if the execution has failed, you can set it to False.

    >>> ls = alfred.sh("ls", "ls is missing on your system")
    >>> mv = alfred.sh("mv", "mv is missing on your system")
    >>> alfred.run(ls, ["/var/yolo"], exit_on_error=False)
    >>> alfred.run(mv, ["/var/yolo", "/var/yolo1"], exit_on_error=False)

    A text command can be used directly with alfred.run. The text command is parsed and the execute is extracted from first
    element in text. The arguments are extracted from the other elements.

    >>> alfred.run("echo hello world")
    >>> alfred.run('cp "/home/fabien/hello world" /tmp', exit_on_error=False)

    Shell operations are not supported &, |, &&, ||, etc... You can not use for example `echo hello world | grep hello` or
    `echo hello world > file.txt`. If you use it an error will be raised.

    The return code, the stdout and the stderr are returned as a tuple.

    >>> return_code, stdout, stderr = alfred.run("echo hello world")

    :param command: command or text program to execute
    :param exit_on_error: break the flow if the exit code is different of 0 (active by default)
    """
    if isinstance(args, str):
        args = [args]

    result = process.run(command, args)
    if result.return_code != 0 and exit_on_error:
        raise Exit(result.return_code)

    return (result.return_code, result.stdout, result.stderr)


def invoke_itself(args) -> None:
    """
    invoke one of alfred's own commands from alfred himself

    >>> alfred.invoke_itself(['--c'])
    >>> alfred.invoke_itself(['--check'])
    >>> alfred.invoke_itself(['--version'])
    :return:
    """
    try:
        from alfred import self_command  # pylint: disable=import-outside-toplevel
        if '--version' in args or '-v' in args:
            self_command.version()
        if '--check' in args or '-c' in args:
            self_command.check()
        if '--completion' in args:
            self_command.completion()
    except Exit as exception:
        if exception.exit_code == 0:
            return

        raise
    except BaseException as exception:
        raise Exit(code=1) from exception


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
    with lib.override_env_pythonpath(new_pythonpath):
        yield
