import io
import os
from typing import Optional, List, Any

import toml

from alfred import echo
from alfred.domain.manifest import AlfredManifest, ManifestParameter
from alfred.exceptions import NotInitialized, AlfredException
from alfred.lib import list_hierarchy_directory
from alfred.logger import logger

def manifest_definitions():
    return [
        ManifestParameter('name', section='alfred'),
        ManifestParameter('description', section='alfred'),
        ManifestParameter('prefix', section='alfred', default=""),
        ManifestParameter('subprojects', section='alfred', default=[], formatter=_format_path_list, checker=_check_path_list),
        ManifestParameter('pythonpath_extends', section='alfred.project', default=[], legacy_aliases=['python_path_extends'], formatter=_format_path_list, checker=_check_path_list),  # pylint: disable=line-too-long
        ManifestParameter('pythonpath_project_root', section='alfred.project', default=True, legacy_aliases=['python_path_project_root']),
        ManifestParameter('command', section='alfred.project', default=["alfred/*.py"], formatter=_format_path_list, checker=_check_path_list),
        ManifestParameter('path_extends', section='alfred.project', default=[], formatter=_format_path_list, checker=_check_path_list),
        ManifestParameter('venv', section='alfred.project', default=None, formatter=_format_path),
        ManifestParameter('venv_dotvenv_ignore', section='alfred.project', default=False),
        ManifestParameter('venv_poetry_ignore', section='alfred.project', default=False),
    ]


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

def lookup_parameter(parameter: str, section: Optional['str'] = 'alfred', project_dir: Optional[str] = None) -> Any:
    """
    Retrieves a setting from the manifest.

    >>> from alfred import manifest
    >>> name = manifest.lookup_parameter('name')
    >>> description = manifest.lookup_parameter('description')
    >>> venv = manifest.lookup_parameter('venv', section='alfred.project')

    """
    parameter_defs = [p for p in MANIFEST_PARAMETERS if p.parameter == parameter and p.section == section]
    if len(parameter_defs) == 0:
        raise AlfredException(f"Unknown project parameter {parameter} in {section}")

    if project_dir is None:
        project_dir = lookup_project_dir()

    section_record = _lookup_manifest_section(project_dir, section)
    parameter_def = parameter_defs[0]
    value = section_record.get(parameter, parameter_def.default)
    if value != parameter_def.default:
        checks = parameter_def.checker(value)
        if checks is not None:
            for check in checks:
                echo.error(f"error in '{parameter}' from '{section}': {check}")

            # We use formatter on default value to get the correct value for windows
            # environment for example.
            return parameter_def.formatter(parameter_def.default, project_dir)

        return parameter_def.formatter(value, project_dir)
    else:
        for alias in parameter_def.legacy_aliases:
            value = section_record.get(alias, parameter_def.default)
            if value != parameter_def.default:
                echo.warning(f"Use of legacy parameter {alias}, please use {parameter} instead")
                checks = parameter_def.checker(value)
                if checks is not None:
                    for check in checks:
                        echo.error(f"error in '{parameter}' from '{section}': {check}")


                    # We use formatter on default value to get the correct value for windows
                    # environment for example.
                    return parameter_def.formatter(parameter_def.default, project_dir)

                return parameter_def.formatter(value, project_dir)

        return parameter_def.formatter(value, project_dir)


def lookup_parameter_project(parameter: str, project_dir: Optional[str] = None) -> Any:
    """
    Retrieves a setting from the project section in the manifest.

    >>> from alfred import manifest
    >>>
    >>> pythonpath_extend = manifest.lookup_parameter_project('pythonpath_extends')
    >>> venv_dotvenv_ignore = manifest.lookup_parameter_project('venv_dotvenv_ignore', project_dir='~/myprojects/project1')
    """
    return lookup_parameter(parameter, section='alfred.project', project_dir=project_dir)


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

def _lookup_manifest_section(project_dir: str, section: str) -> dict:
    """
    retrieves the section of the manifest that matches the requested section.

    If the section is absent, this function returns an empty dictionary to be able to use it with get().

    >>> section = _lookup_section(project_dir, 'alfred.project')
    >>> param = section.get('pythonpath_extends')
    """
    alfred_manifest = lookup(project_dir)
    section_parts = section.split('.')
    configuration = alfred_manifest.configuration
    for section_part in section_parts:
        configuration = configuration.get(section_part, {})

    return configuration


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

def _check_path_list(value: Any) -> Optional[List[str]]:
    if not isinstance(value, list):
        return ["must be a list of string, use [] instead"]
    result = []
    for item in value:
        if not isinstance(item, str):
            result.append(f"item {item} must be a path")

    if len(result) > 0:
        return result

    return None

def _format_path_list(value: Any, project_dir: str) -> List[str]:  # pylint: disable=unused-argument
    """
    format a list of path read from the manifest to use the separator from the current OS.

    """
    values = []
    for item in value:
        path_parts = item.split('/')
        values.append(os.path.join(*path_parts))

    return values

def _format_path(value: Any, project_dir: str) -> Optional[str]:
    """
    format a path read from the manifest to use the separator from the current OS.

    """
    if value is None:
        return None

    path_parts = value.split('/')
    return os.path.realpath(os.path.join(project_dir, *path_parts))


MANIFEST_PARAMETERS = manifest_definitions()
