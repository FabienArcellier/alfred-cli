"""
Detect when a project use poetry. He retrieve the virtual environment it created.

If the parameter venv_poetry_ignore is set in the section project, then the code move on to the next plugin.
"""
import io
import os
import shutil
import subprocess
from typing import Optional

import toml

from alfred import manifest, logger
from alfred.exceptions import AlfredException
from alfred.venv_plugins.base import venv_is_valid


def venv_lookup(project_dir: str) -> Optional[str]:
    ignore = manifest.lookup_parameter_project('venv_poetry_ignore', project_dir)
    if ignore is True:
        return None

    _is_poetry_project = is_poetry_project(project_dir)
    if _is_poetry_project:
        poetry = shutil.which('poetry')
        if poetry is None:
            logger.warning('Poetry manages this project. Poetry is missing from your system.: https://python-poetry.org/docs/#installation')
            return None

        result = subprocess.run([poetry, 'env', 'info', '--path'], cwd=project_dir, capture_output=True, check=False)
        if result.returncode != 0:
            logger.warning('Poetry virtual environment is missing. You should run poetry install.')
            return None

        venv = result.stdout.decode('utf-8').strip()
        if venv_is_valid(venv):
            return venv
        else:
            logger.warning(f"Poetry virtual environment {venv} is not valid")
    else:
        logger.debug(f"{project_dir} is not recognize as a poetry project")

    return None


def is_poetry_project(project_dir: str) -> bool:
    """
    Check if the project is a poetry project.

    :param project_dir: project directory
    :return:
    """

    _is_poetry_project = False
    pyproject_path = os.path.join(project_dir, 'pyproject.toml')
    if os.path.isfile(pyproject_path) is False:
        return False

    with io.open(pyproject_path, 'r', encoding='utf-8') as pyproject_filep:
        try:
            pyproject_dict = toml.load(pyproject_filep)
            build_system = pyproject_dict.get('build-system', {})
            build_backend = build_system.get('build-backend', None)
            if build_backend == 'poetry.core.masonry.api':
                _is_poetry_project = True
        except BaseException as exception:
            raise AlfredException(f'fail to parse {pyproject_path}') from exception

    return _is_poetry_project
