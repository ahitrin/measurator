import datetime
import os
from typing import List

from approvaltests import verify
from approvaltests.reporters import GenericDiffReporterFactory

from measurator import run_main_, TIME_FORMAT
from measurator.domain import IO


class DummyIO(IO):
    def __init__(self, inputs: List[str], timestamps: List[str], file_content: iter):
        self.file_content = file_content
        self.inputs = inputs
        self.timestamps = timestamps
        self.log: List[str] = []

    def write(self, text: str, *args) -> None:
        self.log.append(f" {text}{''.join(str(x) for x in args)}")

    def read(self) -> str:
        output = self.inputs.pop(0)
        self.log.append(f"> {output}")
        return output

    def write_file(self, data: iter) -> None:
        self.log.append(f"! {'|'.join(data)}")

    def read_file(self) -> iter:
        self.log.append("* READ FILE")
        return self.file_content

    def now(self) -> datetime.datetime:
        timestamp = self.timestamps.pop(0)
        self.log.append(f"@ {timestamp}")
        return datetime.datetime.strptime(timestamp, TIME_FORMAT)


def _run_test(file_content, inputs, timestamps):
    io = DummyIO(inputs, timestamps, file_content)
    run_main_(io)
    reporter = GenericDiffReporterFactory().get_first_working()
    verify("\n".join(io.log), reporter)


def test_empty_file_no_predictions():
    _run_test([], ['N'], ['2020-01-31 12:00'])


def test_empty_file_add_prediction():
    _run_test([], ['Y', 'Prediction 1', '2020-02-01 09:00'], ['2020-01-31 12:00'])


def test_no_predictions():
    sample_file = os.path.join(os.getcwd(), 'example.csv')
    file_content = []
    with open(sample_file) as f:
        file_content.extend(f.readlines())
    _run_test(file_content, ['N'], ['2020-01-31 12:00'])
