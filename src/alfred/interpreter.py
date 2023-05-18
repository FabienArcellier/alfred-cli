import os
import sys
from typing import Optional, List

import plumbum
from plumbum import local

from alfred.os import is_windows
from alfred.exceptions import AlfredException
from alfred.logger import logger


def current() -> str:
    """
    returns the path to the current python interpreter
    """
    return sys.executable


def get_venv() -> Optional[str]:
    """
    returns the path to the current virtual environment

    returns None if the current python interpreter is not in a virtual environment, but in the system
    """
    return os.getenv('VIRTUAL_ENV', None)


def run_module(module: str, venv: str, args: List[str]):
    """
    run alfred in another virtual environment with same commands.

    """
    if is_windows():
        python_path = os.path.join(venv, 'Scripts', 'python.exe')
    else:
        python_path = os.path.join(venv, 'bin', 'python')
    if not os.path.isfile(python_path):
        raise AlfredException(f"python interpreter not found in venv: {venv}")

    python = plumbum.local[python_path]
    logger.debug(f"alfred interpreter - switch to python: {python_path} : {args=}")
    with local.env(VIRTUAL_ENV=venv):
        python_args = ['-m', module] + args
        stdout = python[python_args]()
        return stdout
