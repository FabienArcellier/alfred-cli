import contextlib

from alfred import commands, ctx


def setup_context():
    """
    sets up a new independent execution context for a test

    >>> class TestCli(unittest.TestCase):
    >>>
    >>>     def setUp(self) -> None:
    >>>         self.context = alfred_fixture.setup_context()

    >>>     def tearDown(self) -> None:
    >>>         alfred_fixture.teardown_context(self.context)
    """
    context = use_new_context()
    context.__enter__()
    return context


def teardown_context(context):
    context.__exit__(None, None, None)


@contextlib.contextmanager
def use_command_context(command_name: str):
    """
    Use the context of a command.

    :param command_name: The name of the command to use.
    :return: A context manager that will use the context of the command.
    """
    with use_new_context():
        _commands = commands.list_all()
        command_exist = False
        for _command in _commands:
            if _command.name == command_name:
                command_exist = True
                ctx.stack_root_command(_command)
                yield
                break

        if not command_exist:
            raise ValueError(f"Command {command_name} not found in {[_command.name for _command in _commands]}")


@contextlib.contextmanager
def use_new_context():
    """
    sets up a new independent execution context for a test
    """
    with ctx.use_new_context(), commands.use_new_context():
        yield