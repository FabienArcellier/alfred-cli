
import os

import fixtup

from alfred import commands


def test_load_commands_handle_multi_command_directory_origin():
    with fixtup.up('project_multicommands'):
        command = commands.list_all()
        assert len(command) == 2


def test_lookup_should_return_an_alfred_command_from_current_project():
    with fixtup.up('project'):
        path = os.getcwd()

        _command = commands.lookup('cmd:pythonpath')
        assert _command.project_dir == path


def test_lookup_should_return_an_alfred_command_from_sub_project():
    with fixtup.up('multiproject'):
        path = os.getcwd()

        _command = commands.lookup(['product1', 'print_python_exec'])
        assert _command.fullname == "product1 print_python_exec"
        assert _command.project_dir == os.path.join(path, 'products', 'product1')
