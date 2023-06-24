import alfred
import sys

@alfred.command("hello_world")
def hello_world_command():
    print(sys.path)

    import utils
    utils.invoke()
