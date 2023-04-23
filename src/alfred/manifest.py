import io
import os
from typing import Optional, List

import toml

from alfred import echo
from alfred.domain.manifest import AlfredManifest
from alfred.exceptions import NotInitialized
from alfred.lib import list_hierarchy_directory
from alfred.logger import logger


def lookup() -> AlfredManifest:
    """
    Retrieves the contents of the `.alfred.toml` manifest. The search for the manifest starts from
    the current folder and goes up from parent to parent.

    If no alfred manifest is found, an exception is thrown.

    >>> from alfred import manifest
    >>> _manifest = manifest.lookup()
    """
    alfred_manifest_path = lookup_path()

    with io.open(alfred_manifest_path,  encoding="utf8") as file:
        alfred_configuration = toml.load(file)
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
        alfred_configuration_path = _is_manifest_directory(directory)
        if alfred_configuration_path is not None:
            break

    if not alfred_configuration_path:
        raise NotInitialized("not an alfred project (or any of the parent directories), you should run alfred init")

    logger.debug(f"alfred configuration file : {alfred_configuration_path}")
    return alfred_configuration_path


def lookup_obsolete_manifests(directory: Optional[str] = None) -> List[str]:
    """
    Retrieves the list of obsolete manifest files (for example .alfred.yml).

    >>> from alfred import manifest
    >>> obsolete_manifests = manifest.lookup_obsolete_manifests()
    """
    obsolete_manifests = []
    if directory is None:
        directory = os.getcwd()

    hierarchy_directories = list_hierarchy_directory(directory)
    for hdirectory in hierarchy_directories:
        obsolete_manifest_path = contains_obsolete_manifest(hdirectory)
        if obsolete_manifest_path is not None:
            obsolete_manifests.append(obsolete_manifest_path)

    return obsolete_manifests


def contains_obsolete_manifest(directory: Optional[str] = None) -> Optional[str]:
    """
    Checks if the directory contains an obsolete manifest file (for example .alfred.yml).

    It returns None, if there is no obsolete manifest file. Otherwise, it returns the path to the
    obsolete manifest file.
    """
    alfred_manifest_path = os.path.join(directory, ".alfred.yml")
    if os.path.isfile(alfred_manifest_path):
        return alfred_manifest_path

    return None


def contains_manifest(directory: Optional[str] = None) -> bool:
    """
    Checks if the current directory contains an alfred manifest file.

    >>> if manifest.contains_manifest():
    >>>     print("This is an alfred project")
    """
    if directory is None:
        directory = os.getcwd()

    return _is_manifest_directory(directory) is not None


def project_commands_pattern() -> List[str]:
    """
    Retrieves the list of glob expression to scan alfred commands.

    :return:
    """
    _manifest = lookup()
    configuration = _manifest.configuration()

    _default = ["alfred/*.py"]
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    if 'command' not in configuration['alfred']['project']:
        return _default

    command = configuration['alfred']['project']['command']
    if not isinstance(command, list):
        echo.warning(f"The command in the manifest must be a list of string, use {_default} instead")
        return _default

    return command


def prefix() -> str:
    _manifest = lookup()
    configuration = _manifest.configuration()
    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'prefix' not in configuration['alfred']:
        return _default

    return configuration['alfred']['prefix']


def python_path_project_root() -> Optional[bool]:
    _manifest = lookup()
    configuration = _manifest.configuration()
    _default = True
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    if 'python_path_project_root' not in configuration['alfred']['project']:
        return _default

    return configuration['alfred']['project']['python_path_project_root']


def _is_manifest_directory(directory: str) -> Optional[str]:
    alfred_configuration_path = os.path.join(directory, ".alfred.toml")
    if os.path.isfile(alfred_configuration_path):
        return alfred_configuration_path

    return None
