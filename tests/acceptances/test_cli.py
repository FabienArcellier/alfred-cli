import logging
import os
import unittest

import fixtup
import plumbum
import pytest

import alfred
from alfred import is_windows, alfred_prompt
from alfred.interpreter import venv_python_path
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

    def test_cli_should_show_version_when_version_flag_is_given(self):
        _, stdout, _ = alfred_fixture.invoke(["--version"])
        assert alfred.__version__ in stdout

    def test_cli_should_show_version_when_short_version_flag_is_given(self):
        _, stdout, _ = alfred_fixture.invoke(["-v"])
        assert alfred.__version__ in stdout

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

    def test_init_should_ignore_alfred_directory_when_it_already_exists(self):

        with fixtup.up('empty_directory'):
            # Assign
            cwd = os.path.realpath(os.getcwd())
            os.mkdir(os.path.join(cwd, "alfred"))

            # Acts
            exit_code, _, _ = alfred_fixture.invoke(["init"])

            # Assert
            self.assertEqual(0, exit_code)
            self.assertTrue(os.path.isfile(os.path.join(cwd, ".alfred.toml")))

            """
            As the default commands folder already exists, it is kept as it is and the cmd.py
            module is not created.
            """
            assert os.path.isfile(os.path.join(cwd, "alfred", "cmd.py")) is False

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
        with fixtup.up('pythonpath_project_root'):
            _, stdout, _ = alfred_fixture.invoke(["hello_world"])

            assert "invocation through pythonpath" in stdout

    def test_alfred_invocation_apply_pythonpath_extends(self):
        with fixtup.up('pythonpath_extends'):
            _, stdout, _ = alfred_fixture.invoke(["hello_world"])

            assert "invocation through extended pythonpath" in stdout

    def test_alfred_invocation_should_ignore_command_module_in_error(self):
        with fixtup.up('project_with_invalid_commands'):
            _, stdout, stderr = alfred_fixture.invoke([])

            assert "hello_world" in stdout
            assert 'invalid_cmd.py" is not valid.' in stderr
            assert "SyntaxError" in stderr


    def test_alfred_invocation_should_not_displayed_error_on_invalid_command_when_running_one_command(self):
        with fixtup.up('project_with_invalid_commands'):
            _, stdout, stderr = alfred_fixture.invoke(['hello_world', '--name', 'fabien'])

            assert "hello world, fabien" in stdout
            assert '' in stderr


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
            _, stdout, stderr = alfred_fixture.invoke(["product1", "print_python_exec"])

            if is_windows():
                expected_python_executable = os.path.realpath(os.path.join(os.getcwd(), 'products', 'product1', '.venv', 'Scripts', 'python.exe'))
            else:
                expected_python_executable = os.path.realpath(os.path.join(os.getcwd(), 'products', 'product1', '.venv', 'bin', 'python'))

            assert expected_python_executable in stdout, f"{stdout}, stderr: {stderr}"


    def test_alfred_is_using_virtualenv_and_is_able_to_load_binary_program_from_it(self):
        """
        When alfred uses a virtual environment, he must be able to use the programs
        installed inside like mypy and pytest.

        """
        with fixtup.up('project_with_venv'):
            python_path = venv_python_path(os.path.join(os.getcwd(), '.venv'))
            python = plumbum.local[python_path]

            # Install alfred-cli itself in the virtualenv to be able to invoke command
            root_dir = os.path.realpath(os.path.join(__file__, '..', '..', '..'))
            python['-m', 'pip', 'install', '-e', root_dir]()

            # If hello is not copied in the virtual env, this test will fail
            python['-m', 'pip', 'install', "cowsay"]()

            # Acts
            exit_code, stdout, stderr = alfred_fixture.invoke(["hello"])

            # Assert
            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
            assert stderr.strip() == ''
            assert "hello" in stdout

    def test_alfred_check_should_exit_with_one_when_alfred_command_are_corrupted(self):
        with fixtup.up('project_with_invalid_commands'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["--check"])

            assert exit_code == 1


    def test_alfred_check_should_exit_with_zero_when_alfred_command_are_ok(self):
        with fixtup.up('project'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["--check"])

            assert exit_code == 0


    def test_alfred_is_loading_system_dependencies_at_runtime(self):
        """
        Libraries compiled in the system runtime like sqlite3 can be dynamically loaded inside an alfred command.
        """
        with fixtup.up('loading_compiled_dependencies'):
            # Acts
            exit_code, stdout, stderr = alfred_fixture.invoke(["load_sqlite"])

            # Assert
            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"


    def test_alfred_invokeitself_should_invoke_check_command(self):
        with fixtup.up('project_with_command'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["--debug", "invoke_check"])

            assert exit_code == 0


    def test_alfred_invokeitself_should_invoke_check_command_on_project_with_wrong_command(self):
        with fixtup.up('project_with_invalid_commands'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["--debug", "invoke_check"])

            assert exit_code == 1

    def test_alfred_cmdrunning_ignore_code_section_on_help(self):
        with fixtup.up('project_with_cmd_running'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["--help"])
            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
            assert "command is running" not in stdout
            assert "list command is in progress" in stdout


    def test_alfred_cmdrunning_ignore_code_section_on_listing_call(self):
        with fixtup.up('project_with_cmd_running'):
            exit_code, stdout, stderr = alfred_fixture.invoke([])
            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
            assert "command is running" not in stdout
            assert "list command is in progress" in stdout


    def test_alfred_cmdrunning_run_code_section_on_command_run(self):
        with fixtup.up('project_with_cmd_running'):
            exit_code, stdout, stderr = alfred_fixture.invoke(["hello_world"])
            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
            assert "command is running" in stdout
            assert "list command is in progress" not in stdout


def test_alfred_invoke_command_forward_debug_flag_to_command(caplog):
    with fixtup.up('multiproject'), caplog.at_level(logging.DEBUG):
        alfred_fixture.invoke([ '--debug', "cmd:product1_print_python_exec"])

        execute_child_interpreter = [record.message for record in caplog.records if ' switch to python' in record.message]
        assert '--debug' in execute_child_interpreter[0]


def test_alfred_working_directory_is_the_root_of_the_project():
    with fixtup.up('project'):
        root_directory = os.getcwd()

        os.makedirs('src', exist_ok=True)
        os.chdir('src')
        exit_code, stdout, _ = alfred_fixture.invoke(["cmd:print_cwd"])

        assert exit_code == 0
        assert os.path.realpath(stdout.strip()) == os.path.realpath(root_directory)


def test_alfred_execution_directory_return_the_directory_where_invocation_is_done():
    with fixtup.up('project'):
        root_directory = os.getcwd()

        os.makedirs('src', exist_ok=True)
        os.chdir('src')
        exit_code, stdout, _ = alfred_fixture.invoke(["cmd:execution_directory"])

        assert exit_code == 0
        assert os.path.realpath(stdout.strip()) == os.path.realpath(os.path.join(root_directory, 'src'))


def test_alfred_working_directory_is_the_root_of_the_subproject():
    with fixtup.up('multiproject'), alfred_fixture.use_new_context():
        directory_to_create = os.path.join('products', 'product1', 'src')
        os.makedirs(directory_to_create, exist_ok=True)

        root_directory = os.getcwd()
        exit_code, stdout, stderr = alfred_fixture.invoke(["product1", "print_cwd"])

        assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
        assert os.path.realpath(stdout.strip()) == os.path.realpath(os.path.join(root_directory, 'products', 'product1')), f"stdout={stdout}"


def test_alfred_execution_directory_should_return_directory_where_command_has_been_invocked_on_subproject():
    with fixtup.up('multiproject'):
        directory_to_create = os.path.join('products', 'product1', 'src')
        os.makedirs(directory_to_create, exist_ok=True)

        root_directory = os.getcwd()
        exit_code, stdout, stderr = alfred_fixture.invoke(["product1", "execution_directory"])

        assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
        assert os.path.realpath(stdout.strip()) == os.path.realpath(root_directory), f"stdout={stdout}"

def test_alfred_sh_get_command_from_manifest_path_extension():
    if alfred.os.is_windows():
        pytest.skip('Windows does not support this test')

    with fixtup.up('path_extends'):
        exit_code, stdout, stderr = alfred_fixture.invoke(["hello_world"])

        assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
        assert stdout.strip() == 'hello world', f"stdout={stdout}"

def test_alfred_new_should_create_an_empty_command():
    """
    This test uses the `alfred --new` helper to create a new command. It checks that this command appears in the list of `alfred --help`

    :return:
    """

    with fixtup.up('project'):
        with alfred_prompt.use_test_prompt():
            alfred_prompt.send_test_response('echo')
            alfred_prompt.send_test_response('')
            alfred_prompt.send_test_response('alfred/echo.py')
            alfred_prompt.send_test_response('y')

            exit_code, stdout, stderr = alfred_fixture.invoke(["--new"])

            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"

            exit_code, stdout, stderr = alfred_fixture.invoke(["--help"])
            assert 'cmd:echo' in stdout, f"stdout={stdout}\nstderr={stderr}"


def test_alfred_new_should_create_an_command_run_as_full_text():
    """
    This test uses the `alfred --new` helper to create a new command. It checks that this command appears in the list of `alfred --help`

    :return:
    """
    if alfred.os.is_windows():
        pytest.skip('Windows does not support this test')

    with fixtup.up('project'):
        with alfred_prompt.use_test_prompt():
            alfred_prompt.send_test_response('echo')
            alfred_prompt.send_test_response('')
            alfred_prompt.send_test_response('alfred/echo.py')
            alfred_prompt.send_test_response('y')

            exit_code, stdout, stderr = alfred_fixture.invoke(["--new", "echo", "hello_world"])

            assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"

            exit_code, stdout, stderr = alfred_fixture.invoke(["cmd:echo"])
            assert 'hello_world' in stdout, f"stdout={stdout}\nstderr={stderr}"


def test_alfred_should_hide_output_on_run_command_when_stream_flag_is_set():
    if alfred.os.is_windows():
        pytest.skip('Windows does not support this test')

    with fixtup.up('project'):
        exit_code, stdout, stderr = alfred_fixture.invoke(["cmd:hide_stdout"])

        assert exit_code == 0, f"stdout={stdout}\nstderr={stderr}"
        assert 'not_hello' not in stdout, f"stdout={stdout}\nstderr={stderr}"
        assert 'hello' in stdout, f"stdout={stdout}\nstderr={stderr}"


if __name__ == '__main__':
    unittest.main()
