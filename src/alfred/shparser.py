import shlex
from typing import Tuple, List

import click


def parse_text_command(command: str) -> Tuple[str, List[str]]:
    """
    Parse a text command and return the executable and the list of arguments

    >>> command, args = _parse_text_command("echo hello world")
    >>> # command == "echo"
    >>> # args == ["hello", "world"]

    This function does not handle shell operations like `|`, `>`, `>>`, etc...
    These operations depend on the user's shell.
    """
    cmd_parser = shlex.shlex(command, punctuation_chars=True)
    cmd_parser.whitespace_split = True
    cmd_parts = list(cmd_parser)
    for index, part in enumerate(cmd_parts):
        cmd_parts[index] = unquote_litteral_string(part)

    contain_shell = any(True for part in cmd_parts if part in ['&', '|', '&&', '||', '>', '>>', '<', '<<'])
    if contain_shell:
        exception = click.ClickException(f"shell operations are not supported: `{command}`")
        exception.exit_code = 1
        raise exception
    executable = cmd_parts[0]
    args = cmd_parts[1:]
    return executable, args


def unquote_litteral_string(quoted_string: str):
    """
    Remove the quotes from a litteral string

    The shlex parser preserves quotes around character strings.

    >>> value = unquote_litteral_string("'hello world'")
    >>> # value == "hello world"
    """
    unquoted_string = quoted_string
    if quoted_string[0] == "'" and quoted_string[-1] == "'":
        unquoted_string = quoted_string[1:-1]
    elif quoted_string[0] == '"' and quoted_string[-1] == '"':
        unquoted_string = quoted_string[1:-1]

    return unquoted_string
