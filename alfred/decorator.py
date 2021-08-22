from typing import Any, List

import click
from click import BaseCommand


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
        self.command = _command
        self._plugin = None
        self._original_name = _command.name

    @property
    def name(self):
        return self.command.name

    @property
    def original_name(self):
        return self._original_name

    @property
    def plugin(self):
        return self._plugin

    @plugin.setter
    def plugin(self, value):
        self._plugin = value


ALFRED_COMMANDS: List[AlfredCommand] = []
