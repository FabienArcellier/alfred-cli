import fixtup

from alfred import manifest


def test_prefix_should_return_specified_prefix():
    with fixtup.up('project'):
        assert manifest.prefix() == "cmd:"


def test_project_commands_pattern_should_return_default_value():
    with fixtup.up('project'):
        assert manifest.project_commands() == ["alfred/*.py"]


def test_project_commands_pattern_should_return_specified_values():
    with fixtup.up('project_with_command'):
        assert manifest.project_commands() == ["customdir/*.py"]
