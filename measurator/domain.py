import datetime


class IO:
    """Custom wrapper for all input/output interactions"""

    def write(self, text: str, *args) -> None:
        raise NotImplementedError

    def read(self) -> str:
        raise NotImplementedError

    def write_file(self, data: iter) -> None:
        raise NotImplementedError

    def read_file(self) -> iter:
        raise NotImplementedError

    def now(self) -> datetime.datetime:
        raise NotImplementedError
