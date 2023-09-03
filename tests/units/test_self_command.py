import os.path

from alfred import self_command
from alfred.lib import ROOT_DIR


def test_shell_completion_files_should_be_present():
    # Arrange
    # Acts
    shells = self_command.completion_supported_shells()
    for shell_name in shells:
        path = os.path.join(ROOT_DIR, 'resources', shell_name)
        assert os.path.isfile(path), f"completion file for {shell_name} should be present at {path}"
