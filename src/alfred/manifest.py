import io
import os
from typing import Optional

import yaml
from yaml import SafeLoader

from alfred.domain.manifest import AlfredManifest
from alfred.exceptions import NotInitialized
from alfred.lib import list_hierarchy_directory
from alfred.logger import logger


def lookup() -> AlfredManifest:
    """
    Retrieves the contents of the `.alfred.yml` manifest. The search for the manifest starts from
    the current folder and goes up from parent to parent.

    If no alfred manifest is found, an exception is thrown.

    >>> from alfred import manifest
    >>> _manifest = manifest.lookup()
    >>> for plugin in _manifest.plugins():
    >>>     pass
    """
    alfred_manifest_path = lookup_path()

    with io.open(alfred_manifest_path,  encoding="utf8") as file:
        alfred_configuration = yaml.load(file, Loader=SafeLoader)
        for plugin in alfred_configuration["plugins"]:
            plugin['path'] =  os.path.realpath(os.path.join(alfred_manifest_path, '..', plugin['path']))
            logger.debug(f"alfred plugin : {plugin}")

        return AlfredManifest(alfred_configuration)


def lookup_path(starting_path: Optional[str] = None) -> str:
    """
    Finds the path to the nearest alfred manifest. The search starts at the current folder,
    then goes up from parent to parent. If the manifest is found, the full path is returned.

    >>> from alfred import manifest
    >>> manifest_path = manifest.lookup_path()
    """
    if starting_path is None:
        starting_path = os.getcwd()

    hierarchy_directories = list_hierarchy_directory(starting_path)

    alfred_configuration_path = None
    for directory in hierarchy_directories:
        alfred_configuration_path = is_manifest_directory(directory)
        if alfred_configuration_path is not None:
            break

    if not alfred_configuration_path:
        raise NotInitialized("not an alfred project (or any of the parent directories), you should run alfred init")

    logger.debug(f"alfred configuration file : {alfred_configuration_path}")

    return alfred_configuration_path


def is_manifest_directory(alfred_configuration_path: str) -> Optional[str]:
    alfred_configuration_path = os.path.join(alfred_configuration_path, ".alfred.yml")
    if os.path.isfile(alfred_configuration_path):
        return alfred_configuration_path

    return None
