import glob
import io
import os
import sys
from typing import List, Iterator


ROOT_DIR = os.path.realpath(os.path.join(__file__, '..'))


class InvalidPythonModule(Exception):
    pass


def import_python(python_path: str) -> dict:

    module = {"__file__": python_path}
    with io.open(python_path, encoding="utf8") as file:
        content = file.read()
        try:
            code = compile(content, python_path, 'exec')
            eval(code, module, module)  # pylint: disable=eval-used
        except Exception as exception:
            rows = content.split("\n")
            exc_type, _, exc_tb = sys.exc_info()
            line = "N/D"
            if hasattr(exc_tb, "tb_next"):
                line = exc_tb.tb_next.tb_lineno
            raise InvalidPythonModule(f"""Invalid command module : "{python_path}", Line {line}
  {rows[line - 1]}\n
  {exc_type.__name__} : {exception}\n""") from exception

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
