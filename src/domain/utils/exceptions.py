import traceback
from typing import Optional


class ApplicationError(Exception):
    def __init__(self, code: int, message: str, data: Optional[dict] = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(self.message)


def get_trace(exception: Exception) -> str:
    return "".join(traceback.TracebackException.from_exception(exception).format())
