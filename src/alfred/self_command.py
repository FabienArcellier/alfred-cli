"""
This module brings together Alfred's commands. These commands are prefixed with `--`.
They are implemented by Alfred and not by the user. They are therefore reserved.

>>> # check the command integrity
>>> # alfred --check
"""
import io
import os
from typing import List, Optional

import shellingham
from click.exceptions import Exit

from alfred import logger, echo, commands, alfred_prompt, manifest, resource
from alfred.lib import slugify


def check():
    logger.debug("Checking commands integrity...")
    is_ok = commands.check_integrity()
    if is_ok is True:
        logger.debug("Commands integrity is ok")
        raise Exit(code=0)
    else:
        echo.error("Fail to load some commands")
        raise Exit(code=1)

def new(shell_cmd: Optional[str] = None, project_dir: Optional[str] = None):
    if project_dir is None:
        project_dir = manifest.lookup_project_dir()

    if shell_cmd is None:
        code = 'pass'
    else:
        code = f"alfred.run('{shell_cmd}')"

    all_commands = commands.list_all()
    all_commands_names = sorted([cmd.original_name for cmd in all_commands])
    new_cmd_name = alfred_prompt.prompt('What command do you want to create ? ', all_commands_names, validation_func=lambda p: _check_cmd_should_be_unique(p, all_commands_names))
    new_cmd_description = alfred_prompt.prompt(f'What the command `{new_cmd_name}` will do ? ', default="")

    all_modules = commands.list_modules()
    all_command_directories = commands.list_command_directories()
    default_command_module = os.path.join(all_command_directories[0], 'commands.py')

    module_target = alfred_prompt.prompt(f'In which module do you want to create the `{new_cmd_name}` command ? ',
                                     all_modules,
                                     default=default_command_module,
                                     validation_func=lambda p: _check_module_is_valid(p, all_command_directories))

    new_cmd_name_slug = slugify(new_cmd_name)
    tpl_command_variables = {
        'cmd': new_cmd_name,
        'cmd_slug': new_cmd_name_slug,
        'cmd_description': new_cmd_description,
        'cmd_module': module_target,
        'code': code
    }
    command_presentation = resource.template('command_presentation.tpl', variables=tpl_command_variables)

    scaffhold = alfred_prompt.confirm(command_presentation.strip('\n'), default='y')
    if scaffhold is True:
        _scaffhold_command(project_dir, module_target, tpl_command_variables)
        echo.message(f"Command `{new_cmd_name}` created in `{module_target}`")

    raise Exit(code=0)

def version():
    import alfred  # pylint: disable=import-outside-toplevel
    echo.message(f"{alfred.__version__}")
    raise Exit(code=0)


def completion():
    try:
        shell = shellingham.detect_shell()
        if shell[0] in completion_supported_shells():
            if resource.exists(shell[0]):
                file_content = resource.template(shell[0], variables = {
                    'shell': shell[1]
                })
                echo.message(file_content)
                raise Exit(code=0)
            else:
                echo.error(f"unable to find completion file for {shell[0]}")
        else:
            echo.error(f"unable to propose completion for {shell[0]}")
            raise Exit(code=1)
    except shellingham.ShellDetectionFailure as exception:
        echo.error("unable to detect your shell to propose completion instructions")
        raise Exit(code=1) from exception


def completion_supported_shells() -> List[str]:
    return ["bash", "zsh", "fish"]


def _scaffhold_command(project_dir: str, module_target: str, tpl_command_variables: dict):
    target_file = os.path.join(project_dir, module_target)
    if os.path.isfile(target_file) is False:
        new_module = resource.template('command_module_new.tpl', variables=tpl_command_variables)
        with io.open(target_file, 'w', encoding='utf-8') as filep:
            filep.write(new_module)
    else:
        append_in_module = resource.template('command_module_existing.tpl', variables=tpl_command_variables)
        with io.open(target_file, 'a', encoding='utf-8') as filep:
            filep.write(append_in_module)


def _check_cmd_should_be_unique(cmd: str, available_commands: List[str]) -> Optional[str]:
    if cmd == "":
        return "propose a command name that is not empty"

    if cmd in available_commands:
        return "propose a command name that is original"

    return None


def _check_module_is_valid(module: str, command_directories: List[str]) -> Optional[str]:

    if os.path.dirname(module) not in command_directories:
        return "propose a module that is in existing commands directory"

    if not module.endswith('.py'):
        return "propose a module that ends with `.py`"

    return None
