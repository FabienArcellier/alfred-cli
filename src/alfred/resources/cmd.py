import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world(name):
    echo = alfred.sh("echo")
    alfred.run(echo, f"hello world {name}")
