import contextlib
import functools
from typing import Optional, Callable, Generator

from click import BaseCommand


class AlfredCommand:

    def __init__(self, _command: Optional[BaseCommand] = None):
        self.command: Optional[BaseCommand] = _command
        self._original_name: Optional[str] = None
        if _command is not None:
            self._original_name = _command.name

        self.subproject: Optional[str] = None
        self.module: Optional[str] = None
        self.path: Optional[str] = None
        self.project_dir: Optional[str] = None # alfred project directory where the command is attached

        self._context_middleware: Optional[Callable[[], Generator[None, None, None]]] = None

    def __repr__(self):
        return f"<AlfredCommand '{self.name}', '{self.path}', {self.project_dir}>"


    @property
    def fullname(self):
        name = ""
        if self.subproject is not None:
            name += f"{self.subproject} "

        name += self.command.name
        return name


    @property
    def name(self):
        return self.command.name


    @property
    def original_name(self):
        return self._original_name

    def register_click(self, click_command: BaseCommand) -> None:
        """
        Registers the click command to execute when called.

        :param click_command:
        :return:
        """
        self.command = click_command
        self._original_name = click_command.name

    def register_context(self, middleware: Optional[Callable[[], Generator[None, None, None]]]) -> None:
        """
        Before executing the command, alfred injects a context from the project manifest. This context is mounted,
        then unmounted at the end of the execution of the command before moving on to the next one.
        """
        self._context_middleware = middleware

    @contextlib.contextmanager
    def mount_context(self):
        """
        Monte le context avant d'exécuter la commande click.

        :return:
        """
        if self._context_middleware is not None:
            with self._context_middleware():
                yield
        else:
            yield


def make_context(alfred_command: AlfredCommand, func: Callable) -> Callable:

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with alfred_command.mount_context():
            return func(*args, **kwargs)

    return wrapper
