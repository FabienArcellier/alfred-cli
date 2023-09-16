import contextlib
from typing import ContextManager

from alfred import ctx, lib


@contextlib.contextmanager
def command_middleware() -> ContextManager:
    """
    the context code is executed before executing
    the user's target command.
    """
    pythonpath = ctx.env_pythonpath()
    path = ctx.env_path()
    with lib.override_env_pythonpath(pythonpath):
        with lib.override_env_path(path):
            yield
