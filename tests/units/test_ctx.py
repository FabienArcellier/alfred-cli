from click import BaseCommand

from alfred import ctx
from alfred.decorator import AlfredCommand


def test_current_command_should_return_root_command_when_only_root_command_is_executed():
    with ctx.use_new_context():
        command = BaseCommand("command1")
        alfred_command = AlfredCommand(command)
        ctx.stack_root_command(alfred_command)

        # Acts & Asserts
        assert ctx.current_command() == alfred_command


def test_current_command_should_return_last_command_when_subcommand_is_executed():
    with ctx.use_new_context():
        command1 = BaseCommand("command1")
        command2 = BaseCommand("command2")
        alfred_command1 = AlfredCommand(command1)
        alfred_command2 = AlfredCommand(command2)
        ctx.stack_root_command(alfred_command1)
        with ctx.stack_subcommand(alfred_command2):
            # Acts & Asserts
            assert ctx.current_command() == alfred_command2
            assert ctx.root_command() == alfred_command1


def test_root_command_should_return_root_command():
    with ctx.use_new_context():
        command = BaseCommand("command1")
        alfred_command = AlfredCommand(command)
        ctx.stack_root_command(alfred_command)

        # Acts & Asserts
        assert ctx.root_command() == alfred_command
