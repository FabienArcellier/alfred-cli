import pytest
from fixtup import fixtup

import alfred.os
from alfred import process


def test_process_should_encode_unicode_on_windows_equivalent():

    # Arrange
    with fixtup.up('error_encoding'):
        # Acts
        if alfred.os.is_windows():
            result = process.run("CMD.exe /c type encoding_specialchars.txt")
        else:
            result = process.run("cat encoding_specialchars.txt")

        # Acts
        assert "✓" in result.stdout
