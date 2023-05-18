import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("dist", help="build distribution packages")
def dist():
    """
    build distribution packages

    >>> $ alfred dist
    """
    python = alfred.sh("poetry", "python should be present")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['build'])
