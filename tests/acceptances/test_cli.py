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
            self.assertEqual(0, result.exit_code)
            self.assertIn("cmd:hello_world", result.stdout)

    def test_cli_should_invoke_command_with_prefix(self):

        with clone_fixture('project') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:hello_world_2"])

            # Assert
            self.assertEqual(0, result.exit_code)
            self.assertIn("hello world", result.stdout)

    def test_init_should_create_alfred_directory_and_files(self):

        with clone_fixture('empty_directory') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["init"])

            # Assert
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.isfile(os.path.join(cwddir, ".alfred.yml")))

    def test_sh_should_work_with_multicommand(self):

        with clone_fixture('project') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:multicommand"])

            # Assert
            self.assertEqual(0, result.exit_code)

    def test_sh_should_not_work_with_wrong_multicommand(self):

        with clone_fixture('project') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, ["cmd:wrong_multicommand"])

            # Assert
            self.assertEqual(1, result.exit_code)
            self.assertIn("Error: unknow command [\'@@@@\', \'@@@@@\']", result.stdout, result.stdout)


    def test_wrong_commands_should_show_explicit_messages(self):

        with clone_fixture('wrong_command_module') as cwddir:
            # Assign
            os.chdir(cwddir)
            runner = CliRunner()

            # Acts
            result = runner.invoke(cli, [])

            # Assert
            self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
