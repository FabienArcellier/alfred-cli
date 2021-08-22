from typing import Any

import click
from click import BaseCommand


def alfred(click_module: click, name: str, **attrs: Any):

    def alfred_decorated(func):
        decorator = click_module.command(name, **attrs)
        decorated = decorator(func)
        return AlfredCommand(decorated)

    return alfred_decorated


class AlfredCommand:

    def __init__(self, command: BaseCommand):
        self.command = command
