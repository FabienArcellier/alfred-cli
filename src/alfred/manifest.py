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
    alfred_project_dir = lookup_project_dir(path=path, search=search)
    alfred_manifest_path = os.path.join(alfred_project_dir, ".alfred.toml")

    with io.open(alfred_manifest_path,  encoding="utf8") as file:
        alfred_configuration = toml.load(file)
        return AlfredManifest(alfred_manifest_path, alfred_configuration)


def lookup_project_dir(path: Optional[str] = None, search: bool = True) -> str:
    """
    Finds the path to the nearest alfred project directory. The nearest project directory is the
    first directory that contains an alfred manifest. The search starts at the current folder,
    then goes up from parent to parent. If the manifest is found, the path of alfred project directory is returned.
    """
    if path is None:
        path = os.getcwd()

    project_directory = None
    alfred_configuration_path = None
    if search is True:
        hierarchy_directories = list_hierarchy_directory(path)
        for directory in hierarchy_directories:
            alfred_configuration_path = _is_manifest_directory(directory)
            if alfred_configuration_path is not None:
                project_directory = os.path.realpath(directory)
                break

        if not alfred_configuration_path:
            raise NotInitialized("not an alfred project (or any of the parent directories), you should run alfred init")
    else:
        if _is_manifest_directory(path):
            project_directory = os.path.realpath(path)

        if not alfred_configuration_path:
            raise AlfredException(f"{path} is not an alfred project")

    logger.debug(f"alfred project directory : {project_directory}")
    return project_directory


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
    _default = None

    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration
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


def subprojects(project_dir: Optional[str] = None) -> List[str]:
    """
    Retrieves the list of glob expression to scan alfred subprojects.
    """
    _default = []

    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    if 'alfred' not in configuration:
        return _default

    if 'subprojects' not in configuration['alfred']:
        return _default

    return configuration['alfred']['subprojects']


def project_commands(project_dir: Optional[str] = None) -> List[str]:
    """
    Retrieves the list of glob expression to scan alfred commands.

    :return:
    """
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

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

def prefix(project_dir: Optional[str] = None) -> str:
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'prefix' not in configuration['alfred']:
        return _default

    return configuration['alfred']['prefix']


def pythonpath_project_root(project_dir: Optional[str] = None) -> Optional[bool]:
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    _default = True
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    official_parameter = 'pythonpath_project_root'
    if official_parameter in configuration['alfred']['project']:
        return configuration['alfred']['project'][official_parameter]

    legacy_parameters = ['python_path_project_root']
    for legacy_parameter in legacy_parameters:
        if legacy_parameter in configuration['alfred']['project']:
            logger.warning(f"project parameter {legacy_parameter} is deprecated in {project_dir}, use {official_parameter} instead")
            return configuration['alfred']['project'][legacy_parameter]

    return _default


def pythonpath_extends(project_dir: Optional[str] = None) -> List[str]:
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    _default = []
    if 'alfred' not in configuration:
        return _default

    if 'project' not in configuration['alfred']:
        return _default

    official_parameter = 'pythonpath_extends'
    if official_parameter in configuration['alfred']['project']:
        return configuration['alfred']['project'][official_parameter]


    legacy_parameters = ['python_path_extends']
    for legacy_parameter in legacy_parameters:
        if legacy_parameter in configuration['alfred']['project']:
            logger.warning(f"project parameter {legacy_parameter} is deprecated in {project_dir}, use {official_parameter} instead")
            return configuration['alfred']['project'][legacy_parameter]

    return _default


def name(project_dir: Optional[str] = None) -> Optional[str]:
    """
    Récupère le nom du projet depuis le manifest ``.alfred.toml``.

    >>> project_name = manifest.name()

    If the ``name`` parameter is missing from the manifest, the name of the parent folder is returned.
    """
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    project_name = os.path.basename(alfred_manifest.project_directory)
    if 'alfred' in configuration:
        if 'name' in configuration['alfred']:
            project_name = configuration['alfred']['name']

    return project_name


def description(project_dir: Optional[str] = None) -> str:
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

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
