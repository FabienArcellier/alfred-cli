import alfred
from alfred import alfred_command


def test_format_cli_arguments_should_convert_command_to_shell_command():
    """
    the alfred.to_shell function converts an alfred command to a shell command
    """
    # Assign
    @alfred.command("hello")
    def cmd():
        pass

    # Acts
    cmdline = alfred_command.format_cli_arguments(cmd)

    # Assert
    assert cmdline == ["hello"]


def test_format_cli_arguments_should_convert_command_to_shell_command_with_options():
    """
    the alfred.to_shell function converts an alfred command to a shell command
    """
    # Assign
    @alfred.command("hello")
    @alfred.option("--name")
    def cmd():
        pass

    # Acts
    cmdline = alfred_command.format_cli_arguments(cmd, {"name": "fabien"})

    # Assert
    assert cmdline == ["hello", "--name", "fabien"]


def test_format_cli_arguments_convert_command_to_shell_command_with_options_and_ignore_unknown_arguments():
    """
    the alfred.to_shell function converts an alfred command to a shell command
    """
    # Assign
    @alfred.command("hello")
    @alfred.option("--name")
    def cmd():
        pass

    # Acts
    cmdline = alfred_command.format_cli_arguments(cmd, {"name": "fabien", "yolo": "nothing"})

    # Assert
    assert cmdline == ["hello", "--name", "fabien"]
