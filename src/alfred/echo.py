import click

def subcommand(text: str):
    """
    Prints a subcommand to the console.

    >>> echo.subcommand("alfred tests:unit")
    """
    click.echo(click.style(text, fg="green", bold=True))

def message(text: str):
    """
    Prints a message to the console.
    """
    click.echo(click.style(text))


def warning(text: str):
    """
    Prints a warning message to the console.
    """
    click.echo(click.style(text, fg="yellow"), err=True)


def error(text: str):
    """
    Prints an error message to the console.
    """
    click.echo(click.style(text, fg="red", bold=True), err=True)
