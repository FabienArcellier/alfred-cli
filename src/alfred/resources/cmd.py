import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world(name):
    print(f"hello world, {name}")
