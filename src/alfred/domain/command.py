from typing import Optional

from click import BaseCommand


class AlfredCommand:

    def __init__(self, _command: BaseCommand):
        self.command: BaseCommand = _command
        self.plugin: Optional[str] = None
        self._original_name = _command.name
        self.path: Optional[str] = None

    def __repr__(self):
        return f"<AlfredCommand {self.name}, {self.path}>"

    @property
    def name(self):
        return self.command.name

    @property
    def original_name(self):
        return self._original_name
