"""
Detect when a project use poetry. He retrieve the virtual environment it created.

If the parameter venv_poetry_ignore is set in the section project, then the code move on to the next plugin.
"""
from typing import Optional

def venv_lookup(project_dir: str) -> Optional[str]:  # pylint: disable=unused-argument
    return None
