import click


@click.command("hello_world")
def hello_world_command():
    print("hello world")
