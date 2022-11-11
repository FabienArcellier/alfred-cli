import os

def is_posix():
    return os.name == 'posix'

def is_windows():
    return os.name == 'nt'
