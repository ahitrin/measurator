import datetime

from measurator.domain import IO


class ConsoleIO(IO):
    def __init__(self, path) -> None:
        super().__init__()
        self._path = path

    def write(self, text: str, *args):
        print(text, *args)

    def read(self) -> str:
        return input()

    def write_file(self, data: iter) -> None:
        with open(self._path, "w") as f:
            for line in data:
                f.write(line)

    def read_file(self) -> iter:
        try:
            with open(self._path) as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()
