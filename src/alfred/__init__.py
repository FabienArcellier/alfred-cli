#!/usr/bin/python

from alfred.decorator import command, option
from alfred.main import invoke_command, run, sh, env, project_directory, pythonpath, invoke_itself, CMD_RUNNING, execution_directory
from alfred.os import is_posix, is_windows, is_linux, is_macos
from alfred.alfred_prompt import prompt, confirm
import alfred.shell_completion

"""
https://peps.python.org/pep-0440/
"""
__version__ = "2.2.3"
