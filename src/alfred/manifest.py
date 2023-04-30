import io
import os
from typing import Optional, List

import toml

from alfred import echo
from alfred.domain.manifest import AlfredManifest
from alfred.exceptions import NotInitialized, AlfredException
from alfred.lib import list_hierarchy_directory
from alfred.logger import logger


def lookup(path: Optional[str] = None, search: bool = True) -> AlfredManifest:
    """
    Retrieves the contents of the `.alfred.toml` manifest. The search for the manifest starts from
    the current folder and goes up from parent to parent.

    If no alfred manifest is found, an exception is thrown.

    >>> from alfred import manifest
    >>> _manifest = manifest.lookup()
    """
    alfred_manifest_path = lookup_path(path=path, search=search)

    with io.open(alfred_manifest_path,  encoding="utf8") as file:
        alfred_configuration = toml.load(file)
        return AlfredManifest(alfred_configuration)


def lookup_path(path: Optional[str] = None, search: bool = True) -> str:
    """
    Finds the path to the nearest alfred manifest. The search starts at the current folder,
    then goes up from parent to parent. If the manifest is found, the full path is returned.


    >>> from alfred import manifest
    >>> manifest_path = manifest.lookup_path()
    """
    if path is None:
        path = os.getcwd()

    alfred_configuration_path = None
    if search is True:
        hierarchy_directories = list_hierarchy_directory(path)
        for directory in hierarchy_directories:
            alfred_configuration_path = _is_manifest_directory(directory)
            if alfred_configuration_path is not None:
                break

        if not alfred_configuration_path:
            raise NotInitialized("not an alfred project (or any of the parent directories), you should run alfred init")
    else:
        if _is_manifest_directory(path):
            alfred_configuration_path = os.path.join(path, ".alfred.yml")

        if not alfred_configuration_path:
            raise AlfredException(f"{path} is not an alfred project")

    logger.debug(f"alfred configuration file : {alfred_configuration_path}")
    return alfred_configuration_path


def lookup_obsolete_manifests(path: Optional[str] = None) -> List[str]:
    """
    Retrieves the list of obsolete manifest files (for example .alfred.yml).

    >>> from alfred import manifest
    >>> obsolete_manifests = manifest.lookup_obsolete_manifests()
    """
    obsolete_manifests = []
    if path is None:
        path = os.getcwd()

    hierarchy_directories = list_hierarchy_directory(path)
    for hdirectory in hierarchy_directories:
        obsolete_manifest_path = contains_obsolete_manifest(hdirectory)
        if obsolete_manifest_path is not None:
            obsolete_manifests.append(obsolete_manifest_path)

    return obsolete_manifests


def lookup_venv(project_dir: Optional[str] = None) -> Optional[str]:
    """
    Get the venv from the alfred project manifest or the project manifest in the directory folder

    If directory is empty, we get the current manifest.

    :return: the path to the venv
    """
    alfred_manifest = lookup(project_dir)
    _default = None

    configuration = alfred_manifest.configuration()
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    if 'venv' not in configuration['alfred']['project']:
        return _default

    return os.path.realpath(os.path.join(project_dir, configuration['alfred']['project']['venv']))


def contains_obsolete_manifest(project_dir: Optional[str] = None) -> Optional[str]:
    """
    Checks if the directory contains an obsolete manifest file (for example .alfred.yml).

    It returns None, if there is no obsolete manifest file. Otherwise, it returns the path to the
    obsolete manifest file.
    """
    alfred_manifest_path = os.path.join(project_dir, ".alfred.yml")
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


def subprojects(_manifest: Optional[AlfredManifest] = None) -> List[str]:
    """
    Retrieves the list of glob expression to scan alfred subprojects.
    """

    configuration = _manifest_configuration(_manifest)
    _default = []

    if 'alfred' not in configuration:
        return _default

    if 'subprojects' not in configuration['alfred']:
        return _default

    return configuration['alfred']['subprojects']


def project_commands(_manifest: Optional[AlfredManifest] = None) -> List[str]:
    """
    Retrieves the list of glob expression to scan alfred commands.

    :return:
    """
    configuration = _manifest_configuration(_manifest)

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

def prefix(_manifest: Optional[AlfredManifest] = None) -> str:
    configuration = _manifest_configuration(_manifest)
    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'prefix' not in configuration['alfred']:
        return _default

    return configuration['alfred']['prefix']


def python_path_project_root(_manifest: Optional[AlfredManifest] = None) -> Optional[bool]:
    configuration = _manifest_configuration(_manifest)
    _default = True
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    if 'python_path_project_root' not in configuration['alfred']['project']:
        return _default

    return configuration['alfred']['project']['python_path_project_root']


def name(_manifest: Optional[AlfredManifest] = None) -> str:
    configuration = _manifest_configuration(_manifest)
    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'name' not in configuration['alfred']:
        return _default

    return configuration['alfred']['name']


def description(_manifest: Optional[AlfredManifest] = None) -> str:
    configuration = _manifest_configuration(_manifest)
    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'description' not in configuration['alfred']:
        return _default

    return configuration['alfred']['description']


def _is_manifest_directory(directory: str) -> Optional[str]:
    alfred_configuration_path = os.path.join(directory, ".alfred.toml")
    if os.path.isfile(alfred_configuration_path):
        return alfred_configuration_path

    return None


def _manifest_configuration(_manifest: Optional[AlfredManifest] = None) -> dict:
    if _manifest is None:
        _manifest = lookup()
    configuration = _manifest.configuration()
    return configuration
