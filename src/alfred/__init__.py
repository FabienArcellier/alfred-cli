#!/usr/bin/python

from alfred.decorator import command, option
from alfred.main import call, invoke_command, run, sh
from alfred.os import is_posix, is_windows, is_linux, is_macos

"""
version number follow semantic versioning : https://semver.org/

* MAJOR version when you make incompatible API changes, except for 0 that means beta product
* MINOR version when you add functionality in a backwards compatible manner
* PATCH version when you make backwards compatible bug fixes.
"""
__version__ = "1.2.0"
