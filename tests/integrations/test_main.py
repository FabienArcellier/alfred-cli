import os

import fixtup

import alfred
from tests.fixtures import alfred_fixture


def test_alfred_project_directory_should_return_the_directory_that_contains_alfred_yml():
    with fixtup.up("project"):
        project_directory = os.getcwd()
        with alfred_fixture.use_command_context("cmd:hello_world"):
            assert alfred.project_directory() == project_directory


def test_pythonpath_should_add_alfred_project_directory_to_pythonpath_env_variable():
    with fixtup.up("project"):
        with alfred_fixture.use_command_context("cmd:hello_world"):
            with alfred.pythonpath():
                assert alfred.project_directory() in os.getenv('PYTHONPATH')
