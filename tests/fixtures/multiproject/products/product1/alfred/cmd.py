import os
import sys

import alfred


@alfred.command("print_python_exec")
def print_python_exec():
    print(sys.executable)


@alfred.command("print_cwd")
def print_cwd():
    print(os.getcwd())
