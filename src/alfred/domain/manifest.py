import dataclasses
import logging
import os.path
from typing import List, Optional, Any, Callable


class Environment:  # pylint: disable=too-few-public-methods

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

@dataclasses.dataclass
class ManifestParameter:
    parameter: str
    section: Optional[str] = None
    default: Optional[Any] = None
    formatter: Callable[[str, Any], Any] = lambda projectdir, value: value
    legacy_aliases: List[str] = dataclasses.field(default_factory=list)

class AlfredManifest:

    def __init__(self, path: str, alfred_configuration: dict):
        self.path = os.path.realpath(path)
        self._alfred_configuration = alfred_configuration

    @property
    def configuration(self) -> dict:
        return self._alfred_configuration

    @property
    def project_directory(self) -> str:
        return os.path.dirname(self.path)

    def environments(self) -> List[Environment]:
        environments = []
        if 'environment' in self._alfred_configuration:
            environment_values: List[str] = self._alfred_configuration['environment']
            if isinstance(environment_values, list):
                for environment in environment_values:
                    try:
                        environment_splitted = environment.split("=")
                        if len(environment_splitted) == 1:
                            environments.append(Environment(environment_splitted[0], ""))
                        else:
                            environments.append(Environment(environment_splitted[0], environment_splitted[1]))

                    except Exception as exception:  # pylint: disable=broad-except
                        logging.exception(exception)

        return environments
