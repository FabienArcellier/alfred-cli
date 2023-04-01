from typing import Any

import click

from alfred.domain.command import AlfredCommand


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
