import alfred

import yo


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")
