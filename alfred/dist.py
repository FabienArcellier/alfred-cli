import alfred


@alfred.command("dist", help="build distribution packages")
def dist():
    """
    build distribution packages

    >>> $ alfred dist
    """
    python = alfred.sh("poetry", "python should be present")
    alfred.run(python, ['build'])
