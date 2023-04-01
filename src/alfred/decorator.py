from typing import Any, List, Optional

import click
from click import BaseCommand, Command


def command(name: str, **attrs: Any):

    def alfred_decorated(func):
        decorator = click.command(name, **attrs)
        decorated = decorator(func)
        alfred_command = AlfredCommand(decorated)

        return alfred_command

    return alfred_decorated


def option(*args, **attrs):

    def option_decorated(func):
        decorator = click.option(*args, **attrs)
        decorated = decorator(func)
        return decorated

    return option_decorated


class AlfredCommand:

    def __init__(self, _command: BaseCommand):
        self.command: BaseCommand = _command
        self.plugin: Optional[str] = None
        self._original_name = _command.name
        self.path: Optional[str] = None

    def __repr__(self):
        return f"<AlfredCommand {self.name}, {self.path}>"

    @property
    def name(self):
        return self.command.name

    @property
    def original_name(self):
        return self._original_name


ALFRED_COMMANDS: List[AlfredCommand] = []
