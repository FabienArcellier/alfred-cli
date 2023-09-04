import io

import fixtup
import toml

from alfred import interpreter


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
        result = interpreter.venv_lookup()
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
        result = interpreter.venv_lookup()

        # Acts
        assert result is None


def test_venv_lookup_should_not_detect_venv_when_is_absent():
    # Arrange
    with fixtup.up('project'):
        # Acts
        result = interpreter.venv_lookup()
        # Acts
        assert result is None
