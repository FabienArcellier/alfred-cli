import os

import fixtup
from click import Command, Option, Group

from alfred.shell_completion import BashCompleteAlfred


def test_shell_completion_should_autocomplete_cmd_with_double_point_separator_on_2_parts():
    """
    """
    with fixtup.up(''):
        cli = Group(
            "cli",
            chain=True,
            commands=[
                Command("docs:html:ok", params=[Option(["-y"])]),
                Command("docs:html:ko"),
                Group("doc:ok", commands=[Command("full")]),
            ],
        )
        completion = BashCompleteAlfred(cli, {}, cli.name, "_CLICK_COMPLETE")
        os.environ.setdefault('COMP_WORDS', 'docs:h')

        # Acts
        autocompletes = completion.complete()

        # Assert
        assert 'html:ko' in autocompletes
        assert 'html:ok' in autocompletes

