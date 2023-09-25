"""
Retrieves the virtual environment that is declared in the project manifest.

If the parameter venv is absent from the section project, then the code move on to the next plugin.
"""
from typing import Optional

from alfred import manifest, logger
from alfred.venv_plugins.base import venv_is_valid


def venv_lookup(project_dir: str) -> Optional[str]:
    venv = manifest.lookup_parameter_project('venv', project_dir)
    if venv is None:
        return None

    if venv_is_valid(venv):
        return venv

    logger.warning(f"venv {venv} declared in project manifest is not valid, you shoud install / reinstall it")
    return None
