import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world(name):
    print(f"hello world, {name}")


@alfred.command("invoke_check")
def invoke_check():
    alfred.invoke_itself(["--check"])
