import alfred


@alfred.command("hello_world")
def hello_world_command():
    from utils import invoke
    invoke()
