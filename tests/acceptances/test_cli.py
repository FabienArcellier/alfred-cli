import os
import unittest

from click.testing import CliRunner

from alfred.cli import cli
from alfred.os import is_posix, is_windows
from tests.fixtures import clone_fixture


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        """
        AlfredCli is create only once
        :return:
        """
        cli.reset()

    def test_cli_should_show_dedicated_help_to_the_user_when_the_directory_is_not_alfred(self):
        """
        this test check alfred show an help message to the user if a project
        does not contains alfred.ini. It triggered if the user run ``alfred``
        """

        with clone_fixture('empty_directory') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, [])

            # Assert
            self.assertEqual(2, result.exit_code)
            self.assertIn("not an alfred project (or any of the parent directories)", result.stdout)

    def test_cli_should_show_dedicated_help_to_the_user_when_the_directory_is_not_alfred_for_option_help(self):
        """
        this test check alfred show an help message to the user if a project
        does not contains alfred.ini. It triggered if the user run ``alfred --help"
        """

        with clone_fixture('empty_directory') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["--help"])

            # Assert
            self.assertEqual(2, result.exit_code)
            self.assertIn("not an alfred project (or any of the parent directories)", result.stdout)

    def test_cli_should_list_command_with_prefix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, [])

            # Assert
            self.assertEqual(0, result.exit_code)
            self.assertIn("cmd:hello_world", result.stdout)

    def test_cli_should_invoke_command_with_prefix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:hello_world_2"])

            # Assert
            self.assertEqual(0, result.exit_code)
            self.assertIn("hello world", result.stdout)

    def test_init_should_create_alfred_directory_and_files(self):

        with clone_fixture('empty_directory') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["init"])

            # Assert
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.isfile(os.path.join(cwddir, ".alfred.yml")))

    def test_sh_should_work_with_multicommand(self):

        with clone_fixture('project') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:multicommand"])

            # Assert
            self.assertEqual(0, result.exit_code)

    def test_sh_should_not_work_with_wrong_multicommand_for_posix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:wrong_multicommand"])

            # Assert
            self.assertEqual(1, result.exit_code)
            self.assertIn("Error: unknow command [\'@@@@\', \'@@@@@\']", result.stdout, result.stdout)


    def test_wrong_commands_should_show_explicit_messages(self):

        with clone_fixture('wrong_command_module') as cwddir:
            # Assign
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, [])

            # Assert
            self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
