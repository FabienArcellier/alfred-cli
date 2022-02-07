class AlfredException(Exception):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(args, kwargs)
        self.message = message

class NotInitialized(AlfredException):
    pass
