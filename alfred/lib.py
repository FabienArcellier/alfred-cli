import io
import os
from typing import List, Iterator

from alfred.type import path

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..'))


def import_python(python_path: path) -> dict:

    module = {"__file__": python_path}
    with io.open(python_path, encoding="utf8") as file:
        code = compile(file.read(), python_path, 'exec')
        eval(code, module, module)  # pylint: disable=eval-used

    return module


def list_python_modules(folder_path: path) -> Iterator[path]:
    for filename in os.listdir(folder_path):
        if filename.endswith('.py') and filename != '__init__.py':
            python_path = path(os.path.join(folder_path, filename))
            yield python_path


def list_hierarchy_directory(workingdir: path) -> List[path]:
    workingdir = os.path.realpath(workingdir)
    all_parts = workingdir.split('/')

    result = [workingdir]
    while len(all_parts) != 1:
        all_parts.pop()
        if len(all_parts) == 1:
            result.append('/')
        else:
            result.append("/".join(all_parts))

    return result
