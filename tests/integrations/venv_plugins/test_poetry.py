import os
import sys

import fixtup
import pytest

from alfred.venv_plugins import poetry


def test_venv_should_detect_poetry_environment():
    with fixtup.up('project_with_poetry'):
        """
        As poetry is already used by alfred, the poetry info that is renamed points to the project folder.
        """
        if sys.version_info < (3, 8):
            pytest.skip('poetry requires python 3.8+')

        venv = poetry.venv_lookup(os.getcwd())

        assert venv is not None, f"venv {venv} should be detected"
