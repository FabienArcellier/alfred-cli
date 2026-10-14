import os
from unittest.mock import patch

import fixtup

from alfred.venv_plugins import poetry


def test_venv_should_detect_poetry_environment():
    with fixtup.up('project_with_poetry'):
        """
        As poetry is already used by alfred, the poetry info that is renamed points to the project folder.
        """
        venv = poetry.venv_lookup(os.getcwd())

        assert venv is not None, f"venv {venv} should be detected"


def test_venv_should_ignore_the_active_virtualenv(tmp_path):
    with fixtup.up('project_with_poetry'):
        project_dir = os.getcwd()

        # a decoy virtual environment that poetry would report if VIRTUAL_ENV leaks in the subprocess
        decoy_venv = tmp_path / 'decoy_venv'
        (decoy_venv / 'bin').mkdir(parents=True)
        (decoy_venv / 'Scripts').mkdir(parents=True)

        with patch.dict(os.environ, {'VIRTUAL_ENV': str(decoy_venv)}):
            venv = poetry.venv_lookup(project_dir)

        assert venv is not None, f"venv {venv} should be detected"
        assert os.path.realpath(venv) != os.path.realpath(str(decoy_venv)), \
            "poetry should resolve the project virtual environment, not the active VIRTUAL_ENV"
