import io
import os
from typing import Optional

from alfred.lib import ROOT_DIR

RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')

def directory() -> str:
    return RESOURCE_DIR

def exists(resource: str) -> bool:
    resource_path = os.path.join(RESOURCE_DIR, resource)
    return os.path.isfile(resource_path)


def read(resource: str) -> Optional[str]:
    """
    reads the contents of a file in the resources folder.

    :param resource: file name
    """
    resource_path = os.path.join(RESOURCE_DIR, resource)
    if not os.path.isfile(resource_path):
        raise ValueError(f'{resource_path} is missing')

    with io.open(resource_path, encoding='utf-8') as filep:
        return filep.read()


def template(resource: str, variables: dict):
    """
    reads the contents of a file from the resources folder and replaces variables like {var1} with content

    >>> file = resource.template('file.tpl', variables= {
    >>>     'var1': 'content'
    >>> })
    >>>
    >>> print(file)

    :param resource: file name
    :param variables:
    :return:
    """
    resource_path = os.path.join(RESOURCE_DIR, resource)
    if not os.path.isfile(resource_path):
        raise ValueError(f'{resource_path} is missing')

    with io.open(resource_path, encoding='utf-8') as filep:
        content = filep.read()
        return content.format(**variables)
