#!/usr/bin/python

from alfred.decorator import command, option
from alfred.main import call, invoke_command, run, sh, env, project_directory, pythonpath
from alfred.os import is_posix, is_windows, is_linux, is_macos

"""
https://peps.python.org/pep-0440/
"""
__version__ = "2.1.0"
