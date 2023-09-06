import os
import sys


def is_posix() -> bool:
    """
    returns true if the machine executing the code is using linux based os or mac os

    >>> if alfred.is_posix():
    >>>     print("do something for linux and macos"
    """
    return os.name == 'posix'

def is_linux() -> bool:
    """
    returns true if the machine executing the code is using linux based os

    >>> if alfred.is_linux():
    >>>     print("do something for ubuntu, debian, ..."
    """
    return sys.platform.startswith("linux")

def is_macos() -> bool:
    """
    returns true if the machine executing the code is using macos

    >>> if alfred.is_macos():
    >>>     print("do something for macos"
    """
    return sys.platform == "darwin"

def is_windows() -> bool:
    """
    returns true if the machine executing the code is under windows

    >>> if alfred.is_windows():
    >>>     print("do something for windows"
    """
    return os.name == 'nt'
