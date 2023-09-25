import dataclasses
import os
import shlex
import shutil
import subprocess
import sys
from threading import Thread
from typing import List, Union, Optional, Tuple, IO

import click

import alfred.os
from alfred import logger

@dataclasses.dataclass
class Command:
    executable: str

@dataclasses.dataclass
class ProcessResult:
    return_code: int
    stdout: Optional[str]
    stderr: Optional[str]

def run(command: Union[str, Command], args: Optional[List[str]], stream_stdout: bool = True, stream_stderr: bool = True) -> ProcessResult:
    """
    Executes a program in a subprocess and retrieves its result (return code, stdout, stderr). The call is blocking.

    Par défaut, la sortie standard est streamé dans le terminal. Pour désactiver ce comportement, il faut passer `stream_stdout=False`.
    Par défaut, la sortie d'erreur est streamé dans le terminal. Pour désactiver ce comportement, il faut passer `stream_stderr=False`.

    >>> process.run("mypy src/alfred/process.py")
    >>> process.run("mypy", ["src/alfred/process.py"])

    >>> process.run("mypy", ["src/alfred/process.py"], stream_stdout=False, stream_stderr=False)
    :param sync:
    :return:
    """
    if isinstance(command, str):
        executable, args = parse_text_command(command)
        command = sh(executable)

    if args is None:
        args = []

    full_command = [command.executable] + args
    text_command = ' '.join(full_command)
    working_directory = os.getcwd()
    logger.debug(f'{text_command} - wd: {working_directory}')

    # run the command
    with subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pid:
        stdout_capture = capture_output(pid, pid.stdout, sys.stdout, stream=stream_stdout)
        stderr_capture = capture_output(pid, pid.stderr, sys.stderr, stream=stream_stderr)
        return_code = pid.wait()

    return ProcessResult(return_code, stdout_capture.output(), stderr_capture.output())


def parse_text_command(command: str) -> Tuple[str, List[str]]:
    """
    Parse a text command and return the executable and the list of arguments

    >>> command, args = _parse_text_command("echo hello world")
    >>> # command == "echo"
    >>> # args == ["hello", "world"]

    This function does not handle shell operations like `|`, `>`, `>>`, etc...
    These operations depend on the user's shell.
    """
    cmd_parser = shlex.shlex(command, punctuation_chars=True)
    cmd_parser.whitespace_split = True
    cmd_parts = list(cmd_parser)
    for index, part in enumerate(cmd_parts):
        cmd_parts[index] = unquote_litteral_string(part)

    contain_shell = any(True for part in cmd_parts if part in ['&', '|', '&&', '||', '>', '>>', '<', '<<'])
    if contain_shell:
        exception = click.ClickException(f"shell operations are not supported: `{command}`")
        exception.exit_code = 1
        raise exception
    executable = cmd_parts[0]
    args = cmd_parts[1:]
    return executable, args


def unquote_litteral_string(quoted_string: str):
    """
    Remove the quotes from a litteral string

    The shlex parser preserves quotes around character strings.

    >>> value = unquote_litteral_string("'hello world'")
    >>> # value == "hello world"
    """
    unquoted_string = quoted_string
    if quoted_string[0] == "'" and quoted_string[-1] == "'":
        unquoted_string = quoted_string[1:-1]
    elif quoted_string[0] == '"' and quoted_string[-1] == '"':
        unquoted_string = quoted_string[1:-1]

    return unquoted_string


def sh(command: Union[str, List[str]], fail_message: str = None) -> Command:  # pylint: disable=invalid-name
    """
    Load an executable program from the local system. If the command does not exists, it
    will show an error `fail_message` to the console.

    >>> echo = alfred.sh("echo", "echo is missing on your system")
    >>> alfred.run(echo, ["hello", "world"])

    If many commands are provided as command name, it will try the command one by one
    until one of them is present on the system. This behavior is require when you target
    different platform for example (Ubuntu is using `open` to open an url, when MacOs support `xdg-open`
    with the same behavior)

    >>> open = alfred.sh(["open", "xdg-open"], "Either open, either xdg-open is missing on your system. Are you using a compatible platform ?")  # pylint: disable=line-too-long
    >>> alfred.run(open, "http://www.github.com")

    :param command: command or list of command name to lookup
    :param fail_message: failure message show to the user if no command has been found
    :return: a command you can use with alfred.run
    """
    if isinstance(command, str):
        command = [command]

    executable_command = None
    possible_suffixes = [""]
    if alfred.os.is_windows():
        possible_suffixes.append(".exe")

    for _command in command:
        for suffix in possible_suffixes:
            fullpath_command = shutil.which(_command + suffix)
            if fullpath_command is not None:
                executable_command = Command(fullpath_command)
                break



    if not executable_command:
        complete_fail_message = f" - {fail_message}" if fail_message is not None else ""
        raise click.ClickException(f"unknow command {command}{complete_fail_message}")

    return executable_command


class capture_output:  # pylint: disable=invalid-name
    """
    Capture the output of a subprocess and stream it to the terminal

    >>> p = subprocess.Popen(["./spy_stdout_and_stderr"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    >>> stdout_capture = capture_output(p, p.stdout, sys.stdout)
    >>> stderr_capture = capture_output(p, p.stderr, sys.stderr)
    >>> return_code = p.wait()

    >>> stdout = stdout_capture.output()
    >>> stderr = stderr_capture.output()
    """

    def __init__(self, process, capture_stream: Optional[IO] = None, output_stream: Optional[IO] = None, stream: bool = True):
        self.capture_logs = []
        self.subprocess = process
        self.capture_stream = capture_stream
        self.output_stream = output_stream
        self.stream = stream
        self.thread = Thread(target=self._run_capture)
        self.thread.start()

    def _run_capture(self):
        if self.capture_stream is not None:
            while True:
                line = self.capture_stream.readline().decode('utf-8')

                if line != '' and self.stream is True:
                    self.output_stream.write(line)
                    self.output_stream.flush()

                if line != '':
                    self.capture_logs.append(line)

                if self.subprocess.poll() is not None:
                    break

    def output(self):
        self.thread.join()
        return '\n'.join(self.capture_logs)
