import contextlib

from alfred import commands, ctx


@contextlib.contextmanager
def use_command_context(command_name: str):
    """
    Use the context of a command.

    :param command_name: The name of the command to use.
    :return: A context manager that will use the context of the command.
    """
    commands.clear()
    _commands = commands.list_all()
    command_exist = False
    for _command in _commands:
        if _command.name == command_name:
            command_exist = True
            with ctx.use_new_context():
                ctx.stack_root_command(_command)
                yield

    if not command_exist:
        raise ValueError(f"Command {command_name} not found in {[_command.name for _command in _commands]}")
