import os
import sys


def is_posix() -> bool:
    """
    returns true if the machine executing the code is using linux based os or mac os
    """
    return os.name == 'posix'

def is_linux() -> bool:
    """
    returns true if the machine executing the code is using linux based os
    """
    return sys.platform.startswith("linux")

def is_macos() -> bool:
    """
    returns true if the machine executing the code is using macos
    """
    return sys.platform == "darwin"

def is_windows() -> bool:
    """
    returns true if the machine executing the code is under windows
    """
    return os.name == 'nt'
