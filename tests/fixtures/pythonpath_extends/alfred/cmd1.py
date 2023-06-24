import sys

import alfred


@alfred.command("hello_world")
def hello_world_command():
    print(sys.path)

    import utils2
    utils2.invoke()
