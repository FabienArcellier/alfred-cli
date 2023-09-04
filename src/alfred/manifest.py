import io
import os
from typing import Optional, List, Any

import toml

from alfred import echo
from alfred.domain.manifest import AlfredManifest, ManifestParameter
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

    if path != project_directory:
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

def _format_command(project_dir: str, value: Any) -> List[str]:  # pylint: disable=unused-argument
    parameter_def = [p for p in PROJECT_PARAMETERS if p.parameter == 'command'][0]

    if not isinstance(value, list):
        echo.warning(f"The command in the manifest must be a list of string, use {parameter_def.default} instead")
        return parameter_def.default

    return value

PROJECT_PARAMETERS = [
    ManifestParameter('pythonpath_extends', section='project', default=[], legacy_aliases=['python_path_extends']),
    ManifestParameter('pythonpath_project_root', section='project', default=True, legacy_aliases=['python_path_project_root']),
    ManifestParameter('command', section='project', default=["alfred/*.py"], formatter=_format_command),
    ManifestParameter('venv', section='project', default=None, formatter=lambda projectdir, value: os.path.realpath(os.path.join(projectdir, value))),
    ManifestParameter('venv_dotvenv_ignore', section='project', default=False),
]

def lookup_parameter_project(parameter: str, project_dir: Optional[str] = None) -> Any:
    """
    Retrieves a setting from the project section in the manifest.

    >>> from alfred import manifest
    >>>
    >>> pythonpath_extend = manifest.lookup_parameter_project('pythonpath_extends')
    >>> venv_dotvenv_ignore = manifest.lookup_parameter_project('venv_dotvenv_ignore', project_dir='~/myprojects/project1')
    """
    parameter_defs = [p for p in PROJECT_PARAMETERS if p.parameter == parameter]
    if len(parameter_defs) == 0:
        raise AlfredException(f"Unknown project parameter {parameter}")

    if project_dir is None:
        project_dir = lookup_project_dir()

    parameter_def = parameter_defs[0]
    value = _lookup_project_section(project_dir, parameter, default=parameter_def.default)
    if value != parameter_def.default:
        return parameter_def.formatter(project_dir, value)
    else:
        for alias in parameter_def.legacy_aliases:
            value = _lookup_project_section(project_dir, alias, default=parameter_def.default)
            if value != parameter_def.default:
                echo.warning(f"Use of legacy parameter {alias}, please use {parameter} instead")
                return parameter_def.formatter(project_dir, value)

        return value

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


def prefix(project_dir: Optional[str] = None) -> str:
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration

    _default = ''
    if 'alfred' not in configuration:
        return _default

    if 'prefix' not in configuration['alfred']:
        return _default

    return configuration['alfred']['prefix']

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


def _lookup_project_section(project_dir: str, key: str, default: Optional[Any] = None):
    """
    searches for a parameter in the alfred.project section.

    If the section does not exist or the parameter does not exist, we return the default value.
    """
    alfred_manifest = lookup(project_dir)
    configuration = alfred_manifest.configuration
    if 'alfred' not in configuration:
        return default
    if 'project' not in configuration['alfred']:
        return default
    if key not in configuration['alfred']['project']:
        return default

    value = configuration['alfred']['project'][key]
    return value
