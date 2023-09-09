from typing import Tuple, List

import pytest

from alfred import shparser


@pytest.mark.parametrize('cmd,result', [
    ('echo hello world', ('echo', ['hello', 'world'])),
    ("echo 'hello world'", ('echo', ['hello world'])),
    ("echo --version", ('echo', ['--version'])),
])
def test_parse_text_command_should_parse_text_command(cmd: str, result: Tuple[str, List[str]]):
    """
    tests the extraction of a command from a text string.
    """
    # Acts & Assert
    assert shparser.parse_text_command(cmd) == result


def test_parse_text_command_should_handle_litteral_string():
    # Arrange
    cmd = "python -c \"import os;os.rename('file.txt', 'file2.txt');\""
    expected_result = ('python', ['-c', 'import os;os.rename(\'file.txt\', \'file2.txt\');'])

    # Acts & Assert
    assert shparser.parse_text_command(cmd) == expected_result
