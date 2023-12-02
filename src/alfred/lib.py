import contextlib
import glob
import io
import os
import sys
from typing import List, Iterator, ContextManager

from alfred.exceptions import InvalidCommandModule
from alfred import logger

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..'))


def import_python(python_path: str) -> dict:

    module = {"__file__": python_path}
    with io.open(python_path, encoding="utf8") as file:
        content = file.read()
        try:
            code = compile(content, python_path, 'exec')
            eval(code, module, module)  # pylint: disable=eval-used
        except Exception as exception: # pylint: disable=broad-except
            rows = content.split("\n")
            exc_type, _, exc_tb = sys.exc_info()
            line = None
            if hasattr(exc_tb, "tb_next") and hasattr(exc_tb.tb_next, "tb_lineno"):
                line = exc_tb.tb_next.tb_lineno

            if line is not None:
                content = rows[line - 1]
                raise InvalidCommandModule(f"""command module "{python_path}" is not valid at line {line} : {content}.\n {exc_type.__name__} : {exception}\n""") from exception

            raise InvalidCommandModule(f"""command module "{python_path}" is not valid.\n {exc_type.__name__} : {exception}\n""") from exception


    return module


def list_python_modules(glob_expression: str) -> Iterator[str]:
    for filename in glob.glob(glob_expression):
        if filename.endswith('.py') and filename != '__init__.py':
            yield filename


def list_hierarchy_directory(workingdir: str) -> List[str]:
    workingdir = os.path.realpath(workingdir)
    all_parts = workingdir.split(os.sep)

    result = [workingdir]
    while len(all_parts) != 1:
        all_parts.pop()
        if len(all_parts) == 1:
            result.append(os.sep)
        else:
            result.append(os.sep.join(all_parts))

    return result

def slugify(text: str, separator: str = "_"):
    """
    >>> txt = "This is a test ---"
    >>> r = slugify(txt)
    >>> assert r == "this_is_a_test"
    """
    to_replace_with_separator = [' ', '\t', '.', '-', '_']
    text = text.lower()
    for char in to_replace_with_separator:
        text = text.replace(char, separator)
    return text.strip(separator)


@contextlib.contextmanager
def override_env_pythonpath(pythonpath: str) -> ContextManager[None]:
    """
    Override the pythonpath variable in a generalized way

    * override the environment variable in python
    * override pythonpath environment variable in plumbum
    * override sys.path
    """
    previous_syspath = sys.path
    with override_envs(PYTHONPATH=pythonpath):
        sys.path = pythonpath.split(os.pathsep)
        try:
            yield
        finally:
            sys.path = previous_syspath


@contextlib.contextmanager
def override_env_path(path: str) -> ContextManager[None]:
    with override_envs(PATH=path):
        yield

@contextlib.contextmanager
def override_envs(**kwargs) -> ContextManager[None]:
    """
    Overriding environment variables

    >>> with override_envs(PATH="/bin:/usr/bin"):
    >>>     print(os.environ['PATH']) # /bin:/usr/bin
    >>>
    >>> print(os.environ['PATH']) # previous value
    """
    logger.debug(f"override envs: {kwargs}")
    saved = {}
    for key, value in kwargs.items():
        saved[key] = os.environ.get(key)
        os.environ[key] = value

    try:
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value
