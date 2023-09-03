from click.exceptions import Exit

from alfred import logger, echo, commands


def check():
    logger.debug("Checking commands integrity...")
    is_ok = commands.check_integrity()
    if is_ok is True:
        logger.debug("Commands integrity is ok")
        raise Exit(code=0)
    else:
        echo.error("Fail to load some commands")
        raise Exit(code=1)


def version():
    import alfred  # pylint: disable=import-outside-toplevel
    echo.message(f"{alfred.__version__}")
    raise Exit(code=0)
