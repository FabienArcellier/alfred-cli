import os
import sys
from typing import Optional, List, Tuple

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


def run_module(module: str, venv: str, args: List[str]) -> Tuple[int, str, str]:
    """
    run alfred in another virtual environment with same commands.

    """
    global_path = os.getenv('PATH', '')
    python_path = venv_python_path(venv)
    bin_path = venv_bin_path(venv)
    global_path = f"{bin_path}:{global_path}"

    if not os.path.isfile(python_path):
        raise AlfredException(f"python interpreter not found in venv: {venv}")

    if not os.path.isdir(bin_path):
        raise AlfredException(f"bin folder not found in venv: {venv}, {bin_path=}")

    python = plumbum.local[python_path]
    logger.debug(f"alfred interpreter - switch to python: {python_path} : {args=}")

    with local.env(VIRTUAL_ENV=venv, PATH=global_path):
        python_args = ['-m', module] + args
        exit_code, stdout, stderr = python[python_args].run(retcode=None)
        return exit_code, stdout, stderr


def venv_bin_path(venv: str) -> str:
    """
    Determines the path to the binary folder based on the OS and virtual environment path.
    """
    if is_windows():
        return os.path.join(venv, 'Scripts')

    return os.path.join(venv, 'bin')


def venv_python_path(venv: str) -> str:
    """
    Determines the path to the python interpreter based on the OS and virtual environment path.
    """
    if is_windows():
        return os.path.join(venv, 'Scripts', 'python.exe')

    return os.path.join(venv, 'bin', 'python')
