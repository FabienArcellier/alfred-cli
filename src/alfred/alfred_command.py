from typing import List, Optional

from alfred import commands, echo
from alfred.domain.command import AlfredCommand
from alfred.exceptions import UnknownCommand


def format_cli_arguments(command: AlfredCommand or str or List[str], kwargs: Optional[dict] = None) -> List[str]:
    """
    Converts a command and its arguments into an executable command line with alfred

    >>> @alfred.command("hello_world")
    >>> @alfred.option("--name")
    >>> def hello_world_command(name):
    >>>     pass
    >>>
    >>> alfred_command.format_cli_arguments(hello_world_command, {name: "fabien"})
    """
    if isinstance(command, (str, list)):
        command = commands.lookup(command)

        if command is None:
            raise UnknownCommand(command)

    cmdline = command.fullname
    click_command = command.command

    if kwargs is not None:
        for param_name, param_value in kwargs.items():
            match_param = False
            for param in click_command.params:
                if param.name == param_name and param.is_flag is False:
                    cmdline += f" {param.opts[0]} {param_value}"
                    match_param = True
                elif param.name == param_name and param.is_flag is True:
                    cmdline += f" {param.opts[0]}"
                    match_param = True

            if match_param is False:
                echo.warning(f"Unknown parameter {param_name} for command {command.name}")

    return cmdline.split(' ')
