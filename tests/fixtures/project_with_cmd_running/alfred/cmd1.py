import alfred

if alfred.CMD_RUNNING():
    print("command is running")
else:
    print("list command is in progress")

@alfred.command("hello_world")
@alfred.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")
