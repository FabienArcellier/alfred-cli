import os
import sys

import click
import fixtup

import alfred
from alfred.os import is_windows
from tests.fixtures import alfred_fixture


def test_alfred_project_directory_should_return_the_directory_that_contains_alfred_yml():
    with fixtup.up("project"):
        project_directory = os.path.realpath(os.getcwd())
        with alfred_fixture.use_command_context("cmd:hello_world"):
            # for windows that use different path
            assert alfred.project_directory() == project_directory


def test_pythonpath_should_add_alfred_project_directory_to_pythonpath_env_variable():
    with fixtup.up("project"):
        with alfred_fixture.use_command_context("cmd:hello_world"):
            with alfred.pythonpath():
                assert alfred.project_directory() in os.getenv('PYTHONPATH')


def test_invoke_command_should_invoke_command_in_the_same_project():
    """
    the alfred.invoke_command function invokes a command within the same project as a subcommand.

    The subcommand is executed in the same virtualenv as the calling command.
    """
    with fixtup.up("project"):
        with alfred_fixture.use_command_context("cmd:hello_world"):
            # Acts
            @click.command
            def click_wrapper():
                alfred.invoke_command("cmd:print_python_exec")

            exit_code, stdout, stderr = alfred_fixture.invoke_click(click_wrapper)

            # Assert
            assert exit_code == 0
            assert sys.executable in stdout


def test_invoke_command_should_invoke_command_in_the_same_project_with_options():
    """
    the alfred.invoke_command function invokes a command with options as a subcommand.
    """
    with fixtup.up("project"):
        with alfred_fixture.use_command_context("cmd:hello_world"):
            # Acts
            @click.command
            def click_wrapper():
                alfred.invoke_command("cmd:hello_world_3", name="alfred")

            exit_code, stdout, stderr = alfred_fixture.invoke_click(click_wrapper)

            # Assert
            assert exit_code == 0
            assert "hello world 3, alfred" in stdout


def test_invoke_command_should_invoke_command_in_subproject():
    """
    the alfred.invoke_command function invokes a command with options as a subcommand.
    """
    with fixtup.up("multiproject"):
        with alfred_fixture.use_command_context("cmd:hello_world"):
            # Acts
            @click.command
            def click_wrapper():
                alfred.invoke_command(["product1", "print_python_exec"])

            exit_code, stdout, _ = alfred_fixture.invoke_click(click_wrapper)

            # Assert
            if is_windows():
                expected_python_exec = os.path.realpath(os.path.join(os.getcwd(), "products", "product1", ".venv", "Scripts", "python.exe"))
            else:
                expected_python_exec = os.path.realpath(os.path.join(os.getcwd(), "products", "product1", ".venv", "bin", "python"))

            assert exit_code == 0
            assert expected_python_exec in stdout
