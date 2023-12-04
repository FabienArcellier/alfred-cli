
import os

import fixtup

import alfred
from alfred import commands


def test_load_commands_handle_multi_command_directory_origin():
    with fixtup.up('project_multicommands'):
        command = commands.list_all()
        assert len(command) == 2


def test_lookup_should_return_an_alfred_command_from_current_project():
    with fixtup.up('project'):
        path = os.path.realpath(os.getcwd())

        _command = commands.lookup('cmd:pythonpath')
        assert _command.project_dir == path


def test_lookup_should_return_an_alfred_command_from_sub_project():
    with fixtup.up('multiproject'):
        alfred.commands.cache_clear()

        path = os.path.realpath(os.getcwd())

        _command = commands.lookup(['product1', 'print_python_exec'])
        assert _command.fullname == "product1 print_python_exec"
        assert _command.project_dir == os.path.join(path, 'products', 'product1')

def test_check_integrity_should_detect_syntax_error():
    # Arrange
    with fixtup.up('project_with_invalid_commands'):
        alfred.commands.cache_clear()

        # Act
        is_ok = commands.check_integrity()

        # Assert
        assert is_ok is False

def test_check_integrity_should_detect_syntax_error_in_subproject():
    # Arrange
    with fixtup.up('project_with_invalid_commands'):
        alfred.commands.cache_clear()

        # Act
        is_ok = commands.check_integrity()

        # Assert
        assert is_ok is False

def test_list_modules_should_return_the_list_of_modules_in_current_alfred_project():
    # Arrange
    with fixtup.up('project'):
        alfred.commands.cache_clear()

        # Act
        modules = commands.list_modules()

        # Assert
        assert [os.path.join('alfred', 'cmd1.py')] == modules

def test_list_command_directories_should_return_the_list_of_root_directory_for_commands():
    # Arrange
    with fixtup.up('project'):
        alfred.commands.cache_clear()

        # Act
        modules = commands.list_command_directories()

        # Assert
        assert ['alfred'] == modules
