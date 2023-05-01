import sys

import alfred


@alfred.command("print_python_exec")
def print_python_exec():
    print(sys.executable)
