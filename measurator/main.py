import argparse
import csv
import datetime
import time
from contextlib import ContextDecorator
from operator import attrgetter
from typing import List, Tuple

from measurator.console import ConsoleIO
from measurator.domain import IO

TIME_FORMAT = "%Y-%m-%d %H:%M"


def migrate():
    pass


def run_main():
    args = _process_args()
    run_main_(ConsoleIO(args))


class FileWriteProxy(ContextDecorator):
    def __init__(self, io: IO):
        self.io = io
        self.cache = []

    def write(self, data) -> None:
        self.cache.append(data)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.io.write_file(self.cache)


class Prediction:
    def __init__(self, row):
        if len(row) == 5:
            self.status, self.created, self.timestamp, _, self.text = row
        else:
            self.status, self.created, self.timestamp, self.text = row

    def changed(self, status):
        return Prediction([status, self.created, self.timestamp, self.text])

    def changed_at(self, status, timestamp):
        return Prediction([status, self.created, timestamp, self.text])

    def as_list(self):
        return [self.status, self.created, self.timestamp, "", self.text]


def run_main_(io: IO):
    raw_rows = _read_file(io)
    not_yet, succeeds, fails = _split_by_group(raw_rows)
    # evaluate measurements
    delayed = list()
    now = io.now()
    for prediction in not_yet:
        evaluate_time = datetime.datetime(
            *(time.strptime(prediction.timestamp, TIME_FORMAT)[:6])
        )
        if evaluate_time >= now:
            delayed.append(prediction)
            continue
        io.write(
            f"Time to evaluate: {prediction.text}\n Is it true? (Delay/Reject/Yes/*No*)"
        )
        user_input = io.read().capitalize()
        if user_input.startswith("Y"):
            status = "S"
            succeeds.append(prediction.changed(status))
        elif user_input.startswith("D"):
            io.write("When to evaluate (YYYY-mm-dd HH:MM):")
            eval_time = io.read()
            delayed.append(prediction.changed_at("N", eval_time))
        elif user_input.startswith("R"):
            io.write("Evaluation rejected")
        else:
            status = "F"
            fails.append(prediction.changed(status))
    # print total statistics
    total_done = len(fails) + len(succeeds)
    if total_done > 0:
        percentage = "%d%%" % (float(100 * len(succeeds)) / float(total_done))
    else:
        percentage = "N/A"
    io.write("Successful predictions:", percentage, ", not done yet:", len(delayed))
    # add another prediction when needed
    io.write("Add another prediction? Yes/*No*/List")
    user_input = io.read().capitalize()
    if user_input.startswith("Y"):
        io.write("Prediction:")
        text = io.read()
        io.write("When to evaluate (YYYY-mm-dd HH:MM):")
        eval_time = io.read()
        try:
            when = datetime.datetime.strptime(eval_time, TIME_FORMAT)
            if when > now:
                delayed.append(
                    Prediction(["N", now.strftime(TIME_FORMAT), eval_time, text])
                )
            else:
                io.write("This date is in past, prediction is not saved!")
        except ValueError:
            io.write("Wrong time format, prediction is not saved!")
    elif user_input.startswith("L"):
        for prediction in delayed:
            io.write(f"{prediction.timestamp}: {prediction.text}")
    # overwrite predictions file
    with FileWriteProxy(io) as f:
        writer = csv.writer(f)
        for prediction in sorted(fails + succeeds + delayed, key=attrgetter("created")):
            writer.writerow(prediction.as_list())


def _read_file(io: IO) -> List[Prediction]:
    result: List[Prediction] = []
    reader = csv.reader(io.read_file())
    for row in reader:
        p = Prediction(row)
        result.append(p)
    return result


def _split_by_group(rows: List[Prediction]) -> Tuple[List[Prediction], List[Prediction], List[Prediction]]:
    fails: List[Prediction] = list()
    succeeds: List[Prediction] = list()
    not_yet: List[Prediction] = list()
    for p in rows:
        if p.status == "F":
            fails.append(p)
        elif p.status == "S":
            succeeds.append(p)
        else:
            not_yet.append(p)
    return not_yet, succeeds, fails


def _process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args
