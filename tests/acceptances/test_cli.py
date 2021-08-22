import os
import unittest

from click.testing import CliRunner

from alfred.cli import cli
from tests.fixtures import clone_fixture


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        self.currentCwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.currentCwd)

    def test_cli_should_list_command_with_prefix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, [])

            # Assert
            self.assertIn("cmd:hello_world", result.stdout)

    def test_cli_should_invoke_command_with_prefix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:hello_world_2"])

            # Assert
            self.assertIn("hello world", result.stdout)


if __name__ == '__main__':
    unittest.main()
