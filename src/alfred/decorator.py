from typing import Any

import click


from alfred.domain.command import AlfredCommand, make_context


def command(name: str, **attrs: Any):

    def alfred_decorated(func):
        alfred_command = AlfredCommand()
        func = make_context(alfred_command, func)

        click_decorator = click.command(name, **attrs)
        click_command = click_decorator(func)
        alfred_command.register_click(click_command)

        return alfred_command

    return alfred_decorated


def option(*args, **attrs):

    def option_decorated(func):
        decorator = click.option(*args, **attrs)
        decorated = decorator(func)
        return decorated

    return option_decorated
