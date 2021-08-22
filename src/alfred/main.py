import io
import logging
import os
from typing import Optional

import click
import plumbum
import yaml
from click import BaseCommand
from click.exceptions import Exit
from plumbum import CommandNotFound, ProcessExecutionError, FG
from plumbum.machines import LocalCommand
from yaml import SafeLoader

from alfred.decorator import ALFRED_COMMANDS
from alfred.lib import list_hierarchy_directory
from alfred.type import path


@click.pass_context
def invoke_command(ctx, command_label: str, **kwargs) -> None:
    click_command = None
    origin_alfred_command = None
    for alfred_command in ALFRED_COMMANDS:
        if ctx.command.name == alfred_command.name:
            origin_alfred_command = alfred_command

    plugin = origin_alfred_command.plugin
    plugin_click_command=lookup_plugin_command(ALFRED_COMMANDS, command_label, plugin)
    global_click_command=lookup_global_command(ALFRED_COMMANDS, command_label)

    available_plugins_commands = [command.original_name for command in ALFRED_COMMANDS if command.plugin == plugin]
    available_global_commands = [command.name for command in ALFRED_COMMANDS]
    if plugin_click_command is None and global_click_command is None:
        message = [
            f"command {command_label} does not exists.",
            f"Available plugin commands for plugin `{plugin}`: {available_plugins_commands}",
            f"Available global commands: {available_global_commands}",
        ]

        raise click.ClickException("\n".join(message))

    if plugin_click_command:
        click_command = plugin_click_command
    elif global_click_command:
        click_command = global_click_command

    click.echo(click.style(f"$ alfred {click_command.name} : {click_command.help}", fg='green'))
    ctx.invoke(click_command, **kwargs)


def lookup_plugin_command(all_commands, command_label, plugin) -> Optional[BaseCommand]:
    click_command = None
    for alfred_command in all_commands:
        if alfred_command.original_name == command_label and alfred_command.plugin == plugin:
            click_command = alfred_command.command
    return click_command


def lookup_global_command(all_commands, command_label) -> Optional[BaseCommand]:
    click_command = None
    for alfred_command in all_commands:
        if alfred_command.name == command_label:
            click_command = alfred_command.command
    return click_command


def sh(command_name: str, fail_message: str = None) -> LocalCommand:  # pylint: disable=invalid-name
    try:
        return plumbum.local[command_name]
    except CommandNotFound as exception:
        complete_fail_message = f" - {fail_message}" if fail_message is not None else ""
        raise click.ClickException(f"unknow command {command_name}{complete_fail_message}") from exception


def run(command: LocalCommand, args: [str], exit_on_error=True) -> None:
    """
    Most of the process run by alfred are supposed to stop
    if the excecution process is finishing with an exit code of 0

    There is one or two exception as the execution of migration by alembic through honcho.
    exit_on_error allow to manage them

    :param exit_on_error: break the flow if the exit code is different of 0
    """
    try:
        complete_command = command[args]
        working_directory = os.getcwd()
        logging.debug(f'{complete_command} - wd: {working_directory}')
        complete_command & FG  # pylint: disable=pointless-statement
    except ProcessExecutionError as exception:
        if exit_on_error:
            raise Exit(code=exception.retcode) from exception


def lookup_alfred_configuration() -> dict:
    workingdir = path(os.getcwd())
    hierarchy_directories = list_hierarchy_directory(workingdir)

    alfred_configuration_path = None
    for directory in hierarchy_directories:
        alfred_configuration_path = path_contains_alfred_configuration(directory)
        if alfred_configuration_path is not None:
            break

    if alfred_configuration_path is None:
        raise click.ClickException(".alfred.yml configuration is missing, use alfred init to initialize alfred")

    with io.open(alfred_configuration_path,  encoding="utf8") as file:
        alfred_configuration = yaml.load(file, Loader=SafeLoader)
        return alfred_configuration


def path_contains_alfred_configuration(alfred_configuration_path: path) -> Optional[path]:
    alfred_configuration_path = path(os.path.join(alfred_configuration_path, ".alfred.yml"))
    if os.path.isfile(alfred_configuration_path):
        return alfred_configuration_path

    return None
