import logging
from typing import List

class Environment:  # pylint: disable=too-few-public-methods

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class AlfredManifest:

    def __init__(self, alfred_configuration: dict):
        self._alfred_configuration = alfred_configuration

    def configuration(self) -> dict:
        return self._alfred_configuration

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
