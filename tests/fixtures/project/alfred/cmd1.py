import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")


@alfred.command("hello_world_2")
@alfred.option("--name")
def hello_world_2_command(name):
    alfred.invoke_command("hello_world")


@alfred.command("multicommand")
def multicommand():
    echo = alfred.sh(["@@@@", "test"])
    alfred.run(echo, ["1", "-eq", "1"])\


@alfred.command("wrong_multicommand")
def wrong_multicommand():
    echo = alfred.sh(["@@@@", "@@@@@"])
    alfred.run(echo, ["multicommand", "is", "working"])
