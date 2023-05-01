import os
import sys
from typing import Optional, List

import plumbum

from alfred.exceptions import AlfredException


def current() -> str:
    """
    returns the path to the current python interpreter
    """
    return sys.executable


def venv() -> Optional[str]:
    """
    returns the path to the current virtual environment

    returns None if the current python interpreter is not in a virtual environment, but in the system
    """
    return os.getenv('VIRTUAL_ENV', None)


def run_module(module: str, venv_path: str, args: List[str]):
    python_path = os.path.join(venv_path, 'bin', 'python')
    if not os.path.isfile(python_path):
        raise AlfredException(f"python interpreter not found in {venv_path}")

    python = plumbum.local[python_path]
    python_args = ['-m', module] + args
    python[python_args] & plumbum.FG  # pylint: disable=pointless-statement
