import datetime
from typing import List

from approvaltests import verify
from approvaltests.reporters import GenericDiffReporterFactory

from measurator import run_main_
from measurator.domain import IO


class TestableIO(IO):
    def __init__(self, inputs: List[str], timestamps: List[datetime.datetime], file_content: iter):
        self.file_content = file_content
        self.inputs = inputs
        self.timestamps = timestamps
        self.log: List[str] = []

    def write(self, text: str, *args) -> None:
        self.log.append(f" {text}{''.join(str(x) for x in args)}")

    def read(self) -> str:
        output = self.inputs.pop()
        self.log.append(f"> {output}")
        return output

    def write_file(self, data: iter) -> None:
        self.log.append(f"! {'|'.join(data)}")

    def read_file(self) -> iter:
        self.log.append("* READ FILE")
        return self.file_content

    def now(self) -> datetime.datetime:
        timestamp = self.timestamps.pop()
        self.log.append(f"@ {timestamp}")
        return timestamp


def test_approve():
    inputs = ['N']
    timestamps = []
    file_content = []
    io = TestableIO(inputs, timestamps, file_content)
    run_main_(io)
    reporter = GenericDiffReporterFactory().get_first_working()
    verify("\n".join(io.log), reporter)
