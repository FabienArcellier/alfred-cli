class AlfredException(Exception):

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(args, kwargs)
        self.message = message

    def __str__(self):
        return self.message

class InvalidCommandModule(AlfredException):
    pass


class NotInitialized(AlfredException):
    pass


class NotInCommand(AlfredException):
    def __init__(self, instruction: str):
        super().__init__(f"alfred command is not running, {instruction} must be used in alfred command")


class UnknownCommand(AlfredException):
    def __init__(self, command: str):
        super().__init__(f"command {command} does not exists")
