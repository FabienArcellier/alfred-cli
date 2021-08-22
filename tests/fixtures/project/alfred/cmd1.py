import click

from alfred.decorator import command


@command(click, "hello_world")
@click.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")
