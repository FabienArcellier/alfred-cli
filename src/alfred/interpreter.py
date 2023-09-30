import os
import subprocess
import sys
from typing import Optional, List, Tuple, Union

import alfred.os
from alfred import manifest, ctx, process, venv_plugins
from alfred.exceptions import AlfredException
from alfred.lib import override_envs
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

    >>> interpreter.run_module(module='alfred.cli', venv=venv, args=['hello_world'])
    """
    global_path = os.getenv('PATH', '')
    global_python_path = os.getenv('PYTHONPATH', '')
    python_executable_path = venv_python_path(venv)
    bin_path = venv_bin_path(venv)
    global_path = format_path_variable(global_path, bin_path)
    python_path = format_path_variable(global_python_path, bin_path)

    if not os.path.isfile(python_executable_path):
        raise AlfredException(f"python interpreter not found in venv: {venv}")

    if not os.path.isdir(bin_path):
        raise AlfredException(f"bin folder not found in venv: {venv}, bin_path={bin_path}")

    python = process.sh(python_executable_path)
    args = ctx.invocation_options() + args
    logger.debug(f"alfred interpreter - switch to python: {python_executable_path} : args={args}")

    with override_envs(VIRTUAL_ENV=venv, PATH=global_path, PYTHONPATH=python_path):
        python_args = ['-m', module] + args
        process_result = process.run(python, python_args)
        return process_result.return_code, process_result.stdout, process_result.stderr


def run_module_as_pty(module: str, venv: str, args: List[str]) -> int:
    """
    run alfred in another virtual environment with same commands without capturing the output

    >>> interpreter.run_module_as_pty(module='alfred.cli', venv=venv, args=['hello_world'])
    """
    global_path = os.getenv('PATH', '')
    global_python_path = os.getenv('PYTHONPATH', '')
    python_executable_path = venv_python_path(venv)
    bin_path = venv_bin_path(venv)
    global_path = format_path_variable(global_path, bin_path)
    python_path = format_path_variable(global_python_path, bin_path)

    if not os.path.isfile(python_executable_path):
        raise AlfredException(f"python interpreter not found in venv: {venv}")

    if not os.path.isdir(bin_path):
        raise AlfredException(f"bin folder not found in venv: {venv}, bin_path={bin_path}")

    python = process.sh(python_executable_path)
    args = ctx.invocation_options() + args
    logger.debug(f"alfred interpreter - switch to python: {python_executable_path} : args={args}")

    exit_code = 0
    with override_envs(VIRTUAL_ENV=venv, PATH=global_path, PYTHONPATH=python_path):
        try:
            python_args = ['-m', module] + args
            subprocess.run([python.executable] + python_args, stdout=None, stderr=None, check=True)
        except subprocess.CalledProcessError as exception:
            exit_code = exception.returncode

    return exit_code

def venv_bin_path(venv: str) -> str:
    """
    Determines the path to the binary folder based on the OS and virtual environment path.
    """
    if alfred.os.is_windows():
        return os.path.join(venv, 'Scripts')

    return os.path.join(venv, 'bin')


def venv_lookup(project_dir: Optional[str] = None) -> Optional[str]:
    """
    determines which virtual environment to use based on the manifest or if a virtualenv is detected in the project.

    >>> venv_lookup('/home/far/documents/spikes/20230903_1523__try-autocomplete')
    """
    if project_dir is None:
        project_dir = manifest.lookup_project_dir(project_dir)

    _venv_plugins = [venv_plugins.venv, venv_plugins.poetry, venv_plugins.dotvenv]
    for venv_plugin in _venv_plugins:
        venv = venv_plugin.venv_lookup(project_dir)
        if venv is not None:
            return venv

    return None


def venv_python_path(venv: str) -> str:
    """
    Determines the path to the python interpreter based on the OS and virtual environment path.
    """
    if alfred.os.is_windows():
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

    if alfred.os.is_windows():
        separator = ';'
    else:
        separator = ':'

    return f"{separator.join(new_paths)}{separator}{initial_path}"
