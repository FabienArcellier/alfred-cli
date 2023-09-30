import os.path

import alfred.os

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
