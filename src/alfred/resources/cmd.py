import os

import click
from click import Choice

import alfred


@alfred.command("hello_world", help="let alfred introduce it self")
@alfred.option("--name", default="alfred")
def hello_world(name):
    echo = alfred.sh("echo")
    alfred.run(echo, f"Hello world, I am {name}, an extensible automation tool.")
    alfred.run(echo, "")
    alfred.run(echo, "I am here to assist you and your team in your daily tasks.")
    alfred.run(echo, "You can ask me to run simple tasks as running automatic tests.")
    alfred.run(echo, "You can also ask me to run complex workflow as continuous integration & application deployment.")
    alfred.run(echo, "")
    alfred.run(echo, "You writes your commands in python, and I run them for you")
    alfred.run(echo, "")
    alfred.run(echo, "")

    value = click.prompt("Would you want to start ?", type=Choice(['y', 'n']), show_choices=True, default='n')
    if value == 'y':
        command_module = os.path.relpath(__file__, os.getcwd())
        alfred.run(echo, f"Let's code your first command in '{command_module}' !")

        value = click.prompt("Should I open it for you ?", type=Choice(['y', 'n']), show_choices=True, default='n')
        if value == 'y':
            edit = alfred.sh("edit", f"edit alias is not available, you have to open '{command_module}' yourself.")
            alfred.run(edit, command_module)
