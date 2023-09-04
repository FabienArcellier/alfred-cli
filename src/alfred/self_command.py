import io
import os
from typing import List

import shellingham
from click.exceptions import Exit

from alfred import logger, echo, commands
from alfred.lib import ROOT_DIR


def check():
    logger.debug("Checking commands integrity...")
    is_ok = commands.check_integrity()
    if is_ok is True:
        logger.debug("Commands integrity is ok")
        raise Exit(code=0)
    else:
        echo.error("Fail to load some commands")
        raise Exit(code=1)


def version():
    import alfred  # pylint: disable=import-outside-toplevel
    echo.message(f"{alfred.__version__}")
    raise Exit(code=0)


def completion():
    try:
        shell = shellingham.detect_shell()
        if shell[0] in completion_supported_shells():
            path = os.path.join(ROOT_DIR, 'resources', shell[0])
            if os.path.isfile(path) is True:
                with io.open(path, "r", encoding='utf-8') as file:
                    file_content = file.read()
                    file_content = file_content.format(shell=shell[1])
                    echo.message(file_content)
                    raise Exit(code=0)
            else:
                echo.error(f"unable to find completion file for {shell[0]}")
        else:
            echo.error(f"unable to propose completion for {shell[0]}")
            raise Exit(code=1)
    except shellingham.ShellDetectionFailure as exception:
        echo.error("unable to detect your shell to propose completion instructions")
        raise Exit(code=1) from exception

def completion_supported_shells() -> List[str]:
    return ["bash", "zsh", "fish"]
