import os

import alfred


@alfred.command("hello_world")
@alfred.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")


@alfred.command("pythonpath")
@alfred.pythonpath()
def pythonpath():
    print(f"{os.getenv('PYTHONPATH')}")


@alfred.command("pythonpath_src")
@alfred.pythonpath(['src'])
def pythonpath_src():
    print(f"{os.getenv('PYTHONPATH')}")


@alfred.command("hello_world_2")
@alfred.option("--name")
def hello_world_2_command(name):
    alfred.invoke_command("hello_world")


@alfred.command("multicommand")
def multicommand_posix():
    echo = alfred.sh(["@@@@", "python"])
    alfred.run(echo, ["--version"])


@alfred.command("wrong_multicommand")
def wrong_multicommand():
    echo = alfred.sh(["@@@@", "@@@@@"])
    alfred.run(echo, ["multicommand", "is", "working"])


@alfred.command("invoke_check")
def invoke_check():
    alfred.invoke_itself(["--check"])
