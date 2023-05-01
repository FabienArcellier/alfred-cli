import os
import unittest

import fixtup

from tests.fixtures import alfred_fixture


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        """
        AlfredCli is create only once
        :return:
        """
        self.context = alfred_fixture.setup_context()

    def tearDown(self) -> None:
        alfred_fixture.teardown_context(self.context)

    def test_cli_should_show_dedicated_help_to_the_user_when_the_directory_is_not_alfred(self):
        """
        this test check alfred show an help message to the user if a project
        does not contains alfred.ini. It triggered if the user run ``alfred``
        """
        with fixtup.up('empty_directory'):
            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke([])

            # Assert
            self.assertEqual(2, exit_code, stdout)
            self.assertIn("not an alfred project (or any of the parent directories)", stdout)

    def test_cli_should_show_dedicated_help_to_the_user_when_the_directory_is_not_alfred_for_option_help(self):
        """
        this test check alfred show an help message to the user if a project
        does not contains alfred.ini. It triggered if the user run ``alfred --help"
        """

        with fixtup.up('empty_directory'):
            # Assign

            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke(["--help"])

            # Assert
            self.assertEqual(2, exit_code, stdout)
            self.assertIn("not an alfred project (or any of the parent directories)", stdout)

    def test_cli_should_list_commands_with_prefix(self):
        """
        The alfred --help command should list the commands with the prefix defined in the project manifest.
        In this test, the prefix is ``cmd:``.
        """

        with fixtup.up('project'):
            # Assign
            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke(["--help"])

            # Assert
            self.assertEqual(0, exit_code)
            self.assertIn("cmd:hello_world", stdout)

    def test_cli_should_invoke_command_with_prefix(self):

        with fixtup.up('project'):
            # Assign
            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke(["cmd:hello_world_2"])

            # Assert
            self.assertEqual(0, exit_code, stdout)
            self.assertIn("hello world", stdout)

    def test_init_should_create_alfred_directory_and_files(self):

        with fixtup.up('empty_directory'):
            # Assign
            cwd = os.path.realpath(os.getcwd())

            # Acts
            exit_code, _, _ = alfred_fixture.invoke(["init"])

            # Assert
            self.assertEqual(0, exit_code)
            self.assertTrue(os.path.isfile(os.path.join(cwd, ".alfred.toml")))

    def test_pythonpath_decorator_on_command_should_append_alfred_project_directory_to_python_path(self):

        with fixtup.up('project'):
            # Assign
            cwd = os.path.realpath(os.getcwd())

            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke(["cmd:pythonpath"])

            # Assert
            self.assertEqual(0, exit_code)
            assert cwd in stdout

    def test_pythonpath_decorator_on_command_should_append_src_directory_to_python_path(self):

        with fixtup.up('project'):
            # Assign
            cwd = os.path.realpath(os.getcwd())

            # Acts
            exit_code, stdout, _ = alfred_fixture.invoke(["cmd:pythonpath_src"])

            # Assert
            self.assertEqual(0, exit_code)
            assert os.path.join(cwd, 'src')  in stdout

    def test_sh_should_work_with_multicommand(self):

        with fixtup.up('project'):
            # Assign
            # Acts
            exit_code, _, _ = alfred_fixture.invoke(["cmd:multicommand"])

            # Assert
            self.assertEqual(0, exit_code)

    def test_sh_should_not_work_with_wrong_multicommand_for_posix(self):

        with fixtup.up('project'):
            # Assign
            # Acts
            exit_code, _, stderr = alfred_fixture.invoke(["cmd:wrong_multicommand"])

            # Assert
            self.assertEqual(1, exit_code)
            self.assertIn("Error: unknow command [\'@@@@\', \'@@@@@\']", stderr, stderr)


    def test_command_invocation_on_command_that_does_not_exists_should_show_explicit_messages(self):

        with fixtup.up('wrong_command_module'):
            # Assign

            # Acts
            exit_code, _, stderr = alfred_fixture.invoke([""])

            # Assert
            self.assertEqual(2, exit_code)
            assert "Error: No such command" in stderr

    def test_alfred_invocation_use_project_directory_in_pythonpath(self):
        with fixtup.up('project_with_pythonpath_dependency'):
            _, stdout, _ = alfred_fixture.invoke(["hello_world"])

            assert "invocation through pythonpath" in stdout

    def test_alfred_invocation_not_use_project_directory(self):
        """
        If alfred's project manifest declares that the project path is not added to the pythonpath,
        then python cannot resolve the dependency on a project module.

        """
        with fixtup.up('project_without_pythonpath_dependency'):

            try:
                alfred_fixture.invoke(["hello_world"])
            except ModuleNotFoundError as exception:
                assert "No module named 'utils'" in str(exception)


    def test_alfred_subproject_should_invoke_in_its_own_venv(self):
        with fixtup.up('multiproject', keep_mounted_fixture=True):
            _, stdout, _ = alfred_fixture.invoke(["product1", "print_python_exec"])

            assert os.path.join(os.getcwd(), 'products', 'product1', '.venv', 'bin', 'python') in stdout

if __name__ == '__main__':
    unittest.main()
