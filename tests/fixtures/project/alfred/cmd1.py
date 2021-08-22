import click

from alfred.decorator import alfred


@alfred(click, "hello_world")
@click.option("--name")
def hello_world_command(name):
    print(f"hello world, {name}")
