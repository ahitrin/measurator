import datetime
import os
from typing import List, Tuple

from approvaltests import verify
from approvaltests.reporters import GenericDiffReporterFactory

from measurator import run_main_, TIME_FORMAT
from measurator.domain import IO


class DummyIO(IO):
    def __init__(self, inputs: List[str], timestamps: List[str], file_content: iter):
        self.file_content = file_content
        self.inputs = inputs
        self.timestamps = timestamps
        self.log: List[Tuple[str, str]] = []

    def write(self, text: str, *args) -> None:
        self.log.append(("write", f"{text}{''.join(str(x) for x in args)}"))

    def read(self) -> str:
        output = self.inputs.pop(0)
        self.log.append(("read", output))
        return output

    def write_file(self, data: iter) -> None:
        self.log.append(("write_file", "\n".join(x.strip() for x in data)))

    def read_file(self) -> iter:
        self.log.append(("read_file", ""))
        return self.file_content

    def now(self) -> datetime.datetime:
        timestamp = self.timestamps.pop(0)
        self.log.append(("time", timestamp))
        return datetime.datetime.strptime(timestamp, TIME_FORMAT)


def _generate_report(io: DummyIO):
    text: List[str] = []
    report_part: str = ""
    for event_type, event_content in io.log:
        if "write" == event_type:
            report_part = " " + event_content
        elif "read" == event_type:
            report_part = "> " + event_content
        elif "write_file" == event_type:
            rows = event_content.split("\n")
            report_part = "! " + "\n! ".join(rows)
        elif "read_file" == event_type:
            report_part = "* READ FILE"
        elif "time" == event_type:
            report_part = "@ " + event_content
        text.append(report_part)
    return "\n".join(text)


def _run_test(file_content, inputs, timestamps):
    io = DummyIO(inputs, timestamps, file_content)
    run_main_(io)
    reporter = GenericDiffReporterFactory().get_first_working()
    report = _generate_report(io)
    verify(report, reporter)


def _sample_content(file_format=1):
    file_name = {1: "example.csv", 2: "example2.csv"}
    sample_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), file_name[file_format]
    )
    file_content = []
    with open(sample_file) as f:
        file_content.extend(f.readlines())
    return file_content


def test_empty_file_no_predictions():
    _run_test(file_content=[], inputs=["N"], timestamps=["2020-01-31 12:00"])


def test_empty_file_add_prediction():
    _run_test(
        file_content=[],
        inputs=["Y", "Prediction 1", "2020-02-01 09:00"],
        timestamps=["2020-01-31 12:00"],
    )


def test_no_predictions():
    _run_test(
        file_content=_sample_content(), inputs=["N"], timestamps=["2020-01-31 12:00"]
    )


def test_add_prediction():
    _run_test(
        file_content=_sample_content(),
        inputs=["Y", "Prediction 1", "2020-02-01 09:00"],
        timestamps=["2020-01-31 12:00"],
    )


def test_add_prediction_new_format():
    _run_test(
        file_content=_sample_content(2),
        inputs=["Y", "Prediction 1", "2020-02-01 09:00"],
        timestamps=["2020-01-31 12:00"],
    )


def test_list_predictions():
    _run_test(
        file_content=_sample_content(), inputs=["L"], timestamps=["2020-01-31 12:00"],
    )


def test_validate_prediction_true():
    _run_test(
        file_content=_sample_content(),
        inputs=["Y", "Y", "N"],
        timestamps=["2020-04-01 12:00"],
    )


def test_validate_prediction_delay():
    _run_test(
        file_content=_sample_content(),
        inputs=["D", "2020-04-02 09:00", "D", "2020-05-01 12:00", "N"],
        timestamps=["2020-04-01 12:00"],
    )


def test_validate_prediction_false():
    _run_test(
        file_content=_sample_content(),
        inputs=["N", "N", "N"],
        timestamps=["2020-04-01 12:00"],
    )


def test_validate_prediction_reject():
    _run_test(
        file_content=_sample_content(),
        inputs=["R", "R", "N"],
        timestamps=["2020-04-01 12:00"],
    )


def test_reject_invalid_prediction_date_format():
    _run_test(
        file_content=[],
        inputs=["Y", "prediction", "2020-04-01"],
        timestamps=["2020-04-01 12:00"],
    )


def test_reject_prediction_date_in_past():
    _run_test(
        file_content=[],
        inputs=["Y", "prediction", "2020-04-01 11:59"],
        timestamps=["2020-04-01 12:00"],
    )
