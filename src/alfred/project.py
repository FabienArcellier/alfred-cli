import glob
import os
from typing import Optional, List

from alfred import manifest
from alfred.domain.project import AlfredProject


def list_all(project_dir: Optional[str] = None) -> List[AlfredProject]:
    """
    lists all projects related to a main project, including itself.
    """
    if project_dir is None:
        project_dir = manifest.lookup_project_dir()

    name = manifest.name(project_dir)
    main_project = AlfredProject(name, project_dir)
    projects = [main_project]
    projects_to_scan = [main_project]
    while len(projects_to_scan) > 0:
        next_projects_to_scan = []
        for project in projects_to_scan:
            subproject_globs = manifest.subprojects(project.directory)
            for subproject_glob in subproject_globs:
                directories = glob.glob(subproject_glob)
                for directory in directories:
                    if os.path.isdir(directory) and manifest.contains_manifest(directory):
                        subproject_name = manifest.name(directory)
                        subproject = AlfredProject(subproject_name, directory)
                        projects.append(subproject)
                        next_projects_to_scan.append(subproject)

        projects_to_scan = next_projects_to_scan

    return projects
