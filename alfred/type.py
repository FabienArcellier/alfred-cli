# pylint: disable=pointless-string-statement

from typing import NewType, List

import click

"""
path of object (directory or file) in filesystem
/root
"""
path = NewType('path', str)  # pylint: disable=invalid-name


class Environment:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class AlfredConfiguration:

    def __init__(self, alfred_configuration: dict):
        self._alfred_configuration = alfred_configuration

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
                        click.echo(exception, err=True)

        return environments

    def plugins(self) -> List[str]:
        alfred_configuration = self._alfred_configuration
        return alfred_configuration["plugins"]
