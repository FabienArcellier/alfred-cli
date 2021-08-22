import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")


@alfred.command("hello_world_2")
@alfred.option("--name")
def hello_world_2_command(name):
    alfred.invoke_command("hello_world")
