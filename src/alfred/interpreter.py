import os
import sys
from typing import Optional, List, Tuple, Union

import plumbum
from plumbum import local
from plumbum.commands.modifiers import _TEE

import alfred.os
from alfred import manifest
from alfred.os import is_windows
from alfred.exceptions import AlfredException
from alfred.logger import logger


def current() -> str:
    """
    returns the path to the current python interpreter
    """
    return sys.executable


def venv_get() -> Optional[str]:
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
    global_path = format_path_variable(global_path, bin_path)

    if not os.path.isfile(python_path):
        raise AlfredException(f"python interpreter not found in venv: {venv}")

    if not os.path.isdir(bin_path):
        raise AlfredException(f"bin folder not found in venv: {venv}, bin_path={bin_path}")

    python = plumbum.local[python_path]
    logger.debug(f"alfred interpreter - switch to python: {python_path} : args={args}")

    with local.env(VIRTUAL_ENV=venv, PATH=global_path):
        python_args = ['-m', module] + args
        if is_windows():
            # windows does not support streaming through plumbum.
            # the publication is done at the end of the call.
            #
            # I don't know how to do better.
            exit_code, stdout, stderr = python[python_args].run(retcode=None)
            print(stdout)
            print(stderr)
        else:
            exit_code, stdout, stderr = python[python_args] & _TEE(retcode=None)
        return exit_code, stdout, stderr


def venv_bin_path(venv: str) -> str:
    """
    Determines the path to the binary folder based on the OS and virtual environment path.
    """
    if is_windows():
        return os.path.join(venv, 'Scripts')

    return os.path.join(venv, 'bin')


def venv_is_valid(venv: str) -> bool:
    """
    checks if a folder is a valid virtualenv

    * checks for the presence of the `bin` folder for posix systems
    * checks for the presence of the `Scripts` folder for windows
    """
    if alfred.os.is_windows():
        return os.path.isdir(os.path.join(venv, 'Scripts'))
    else:
        return os.path.isdir(os.path.join(venv, 'bin'))


def venv_lookup(project_dir: Optional[str] = None) -> Optional[str]:
    """
    determines which virtual environment to use based on the manifest or if a virtualenv is detected in the project.

    >>> venv_lookup('/home/far/documents/spikes/20230903_1523__try-autocomplete')
    """
    if project_dir is None:
        project_dir = manifest.lookup_project_dir(project_dir)

    venv = manifest.lookup_parameter_project('venv', project_dir)
    if venv is not None and venv_is_valid(venv):
        return venv
    elif venv is not None:
        logger.debug(f"venv {venv} is not valid")

    if manifest.lookup_parameter_project('venv_dotvenv_ignore', project_dir) is False:
        dotvenv_path = os.path.join(project_dir, '.venv')
        if os.path.isdir(dotvenv_path) and venv_is_valid(dotvenv_path):
            return dotvenv_path
        elif os.path.isdir(dotvenv_path):
            logger.debug(f"venv {venv} is not valid")

    return None


def venv_python_path(venv: str) -> str:
    """
    Determines the path to the python interpreter based on the OS and virtual environment path.
    """
    if is_windows():
        return os.path.join(venv, 'Scripts', 'python.exe')

    return os.path.join(venv, 'bin', 'python')


def format_path_variable(initial_path: str, new_paths: Union[str, List[str]]):
    """
    Formats the PATH variable according to the OS rule.

    >>> format_path_variable('/usr/bin', '/usr/local/bin')
    >>> format_path_variable('/usr/bin', ['/usr/local/bin', '/home/far/appdata/sbin'])
    """

    if isinstance(new_paths, str):
        new_paths = [new_paths]

    if is_windows():
        separator = ';'
    else:
        separator = ':'

    return f"{separator.join(new_paths)}{separator}{initial_path}"
