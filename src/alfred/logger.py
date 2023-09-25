import logging

logging.basicConfig(format="%(asctime)s %(levelname)s - %(message)s [%(filename)s:%(lineno)s]")
logger = logging.getLogger("alfred-cli")

def get_logger() -> logging.Logger:
    return logger

def debug(message: str):
    """
    log a debug message

    >>> from alfred import logger
    >>> logger.debug("hello world")
    """
    logger.debug(message, stacklevel=2)


def warning(message: str):
    """
    log a warning message

    >>> from alfred import logger
    >>> logger.warning("hello world")
    """
    logger.warning(message, stacklevel=2)
