import io
import os

import fixtup
import pytest
import toml

from alfred import interpreter


@pytest.fixture(autouse=True)
def clear_venv_lookup_cache():
    """Clear the venv_lookup cache before each test to prevent interference."""
    interpreter.venv_lookup_cache_clear()
    yield
    interpreter.venv_lookup_cache_clear()


def test_venv_lookup_should_detect_venv_automatically():
    # Arrange
    with fixtup.up('project_with_venv'):
        # remove venv parameter from manifest
        with io.open('.alfred.toml', 'r') as filep:
            manifest = toml.load(filep)
            del manifest['alfred']['project']['venv']
        with io.open('.alfred.toml', 'w') as filep:
            toml.dump(manifest, filep)

        # Acts
        result = interpreter.venv_lookup(project_dir=os.getcwd())
        # Acts
        assert result.endswith('.venv')


def test_venv_lookup_should_detect_ignore_dotvenv_when_venv_dotvenv_ignore_is_at_true():
    # Arrange
    with fixtup.up('project_with_venv'):
        # remove venv parameter from manifest and add ignore dotvenv discovery
        with io.open('.alfred.toml', 'r') as filep:
            manifest = toml.load(filep)
            del manifest['alfred']['project']['venv']
            manifest['alfred']['project']['venv_dotvenv_ignore'] = True
        with io.open('.alfred.toml', 'w') as filep:
            toml.dump(manifest, filep)

        # Acts
        result = interpreter.venv_lookup(project_dir=os.getcwd())

        # Acts
        assert result is None


def test_venv_lookup_should_not_detect_venv_when_is_absent():
    # Arrange
    with fixtup.up('project'):
        # Acts
        result = interpreter.venv_lookup(project_dir=os.getcwd())
        # Acts
        assert result is None


def test_venv_lookup_should_prefer_project_dotvenv_over_poetry():
    # Arrange
    with fixtup.up('project_with_poetry_and_dotvenv'):
        project_dir = os.getcwd()

        # Acts
        result = interpreter.venv_lookup(project_dir=project_dir)

        # Assert
        assert result is not None
        assert os.path.realpath(result) == os.path.realpath(os.path.join(project_dir, '.venv'))


def test_venv_lookup_should_fallback_on_poetry_when_dotvenv_is_ignored():
    # Arrange
    with fixtup.up('project_with_poetry_and_dotvenv'):
        project_dir = os.getcwd()
        # ignore the project-local .venv so that poetry is used as a last resort
        with io.open('.alfred.toml', 'r') as filep:
            manifest = toml.load(filep)
            manifest.setdefault('alfred', {}).setdefault('project', {})['venv_dotvenv_ignore'] = True
        with io.open('.alfred.toml', 'w') as filep:
            toml.dump(manifest, filep)

        # Acts
        result = interpreter.venv_lookup(project_dir=project_dir)

        # Assert
        assert result is not None
        assert os.path.realpath(result) != os.path.realpath(os.path.join(project_dir, '.venv'))
