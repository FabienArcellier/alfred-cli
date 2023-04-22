import fixtup

from alfred import commands


def test_load_commands_handle_multi_command_directory_origin():
    with fixtup.up('project_multicommands'):
        command = commands.list_all()
        assert len(command) == 2
