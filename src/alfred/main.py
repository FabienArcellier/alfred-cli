import io
import os
from typing import Optional

import yaml
from yaml import SafeLoader

from alfred.lib import list_hierarchy_directory
from alfred.type import path


def lookup_alfred_configuration() -> dict:
    workingdir = path(os.getcwd())
    hierarchy_directories = list_hierarchy_directory(workingdir)

    alfred_configuration_path = None
    for directory in hierarchy_directories:
        alfred_configuration_path = path_contains_alfred_configuration(directory)
        if alfred_configuration_path is not None:
            break

    if alfred_configuration_path is None:
        raise OSError(".alfred.yml configuration is missing")

    with io.open(alfred_configuration_path,  encoding="utf8") as file:
        alfred_configuration = yaml.load(file, Loader=SafeLoader)
        return alfred_configuration


def path_contains_alfred_configuration(alfred_configuration_path: path) -> Optional[path]:
    alfred_configuration_path = path(os.path.join(alfred_configuration_path, ".alfred.yml"))
    if os.path.isfile(alfred_configuration_path):
        return alfred_configuration_path

    return None
