"""
Detect when the project contains a virtual environment mount in .venv. He retrieve the virtual environment.

If the parameter venv_dotvenv_ignore is set in the section project, then the code move on to the next plugin.
"""
import os.path
from typing import Optional

from alfred import manifest, logger
from alfred.venv_plugins.base import venv_is_valid


def venv_lookup(project_dir: str) -> Optional[str]:
    venv_dotvenv_ignore = manifest.lookup_parameter_project('venv_dotvenv_ignore', project_dir)
    if venv_dotvenv_ignore is True:
        return None

    dotvenv_path = os.path.join(project_dir, '.venv')
    if os.path.isdir(dotvenv_path) and venv_is_valid(dotvenv_path):
        return dotvenv_path
    elif os.path.isdir(dotvenv_path):
        logger.debug(f"venv {dotvenv_path} is not valid")

    return None
