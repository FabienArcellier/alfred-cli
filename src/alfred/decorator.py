from typing import Any, Optional

import click


from alfred.domain.command import AlfredCommand, make_context


def command(name: str, help: str = '', **attrs: Any):  # pylint: disable=redefined-builtin
    """
    Declare a command.

    The command must be created in a module that Alfred references (see Project > Section [alfred.project] > command).
    When executing, Alfred will reference this command by name and execute it if called.

    >>> @alfred.command("hello_world")
    >>> def hello_world():
    >>>     print("hello world")

    ``help`` attribute allow you to configure the inline documentation.

    >>> @alfred.command("hello_world", help="This is a hello world command")
    >>> def hello_world():
    >>>     print("hello world")

    :param name: command name
    :param help: inline documentation
    :param attrs: allow to use any click supported attributes (see https://click.palletsprojects.com/en/latest/api/), support is not garanteed in long term
    """

    def alfred_decorated(func):
        alfred_command = AlfredCommand()
        func = make_context(alfred_command, func)

        click_decorator = click.command(name, help=help, **attrs)
        click_command = click_decorator(func)
        alfred_command.register_click(click_command)

        return alfred_command

    return alfred_decorated


def option(option: str, option_alias: Optional[str] = None, help: str = '', default: Optional[str] = None, **attrs):  # pylint: disable=redefined-builtin,redefined-outer-name
    """
    Declare optional parameter on a command

    This command can be called either with ``alfred hello_world``, or with ``alfred hello_world --name=alfred``,
    or with ``alfred hello_world -n alfred``.

    >>> import alfred
    >>>
    >>> @alfred.command("hello_world")
    >>> @alfred.option("--name", "-n", help="Name of the person to greet", default="world")
    >>> def hello_world(name: str):
    >>>     print("hello {name}")

    :param option: option name (--option)
    :param option_alias: short option (-o)
    :param help: inline documentation
    :param default: default value if option is not provided (None by default)
    :param allow to use any click supported attributes (see https://click.palletsprojects.com/en/latest/api/), support is not garanteed in long term
    """

    def option_decorated(func):
        if option_alias is None:
            decorator = click.option(option, help=help, default=default, **attrs)
        else:
            decorator = click.option(option, option_alias, help=help, default=default, **attrs)
        decorated = decorator(func)
        return decorated

    return option_decorated
