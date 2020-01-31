import argparse
import csv
import datetime
import time
from contextlib import ContextDecorator
from operator import itemgetter

from measurator.console import ConsoleIO
from measurator.domain import IO

TIME_FORMAT = "%Y-%m-%d %H:%M"


def migrate():
    pass


def run_main():
    args = _process_args()
    run_main_(ConsoleIO(args.path))


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


def run_main_(io: IO):
    not_yet, succeeds, fails = _read_file(io)
    # evaluate measurements
    delayed = list()
    for status, created, timestamp, text in not_yet:
        evaluate_time = datetime.datetime(*(time.strptime(timestamp, TIME_FORMAT)[:6]))
        if evaluate_time < io.now():
            io.write(f"Time to evaluate: {text}\n Is it true? (Delay/Reject/Yes/*No*)")
            user_input = io.read().capitalize()
            if user_input.startswith("Y"):
                status = "S"
                succeeds.append((status, created, timestamp, text))
            elif user_input.startswith("D"):
                io.write("When to evaluate (YYYY-mm-dd HH:MM):")
                eval_time = io.read()
                delayed.append(("N", created, eval_time, text))
            elif user_input.startswith('R'):
                io.write("Evaluation rejected")
            else:
                status = "F"
                fails.append((status, created, timestamp, text))
        else:
            delayed.append((status, created, timestamp, text))
    not_yet = delayed
    # print total statistics
    total_done = len(fails) + len(succeeds)
    if total_done > 0:
        percentage = "%d%%" % (float(100 * len(succeeds)) / float(total_done))
    else:
        percentage = "N/A"
    io.write("Successful predictions:", percentage, ", not done yet:", len(not_yet))
    # add another prediction when needed
    io.write("Add another prediction? Y/N")
    user_input = io.read()
    if user_input.capitalize().startswith("Y"):
        io.write("Prediction:")
        prediction = io.read()
        io.write("When to evaluate (YYYY-mm-dd HH:MM):")
        eval_time = io.read()
        not_yet.append(("N", io.now().strftime(TIME_FORMAT), eval_time, prediction))
    # overwrite predictions file
    with FileWriteProxy(io) as f:
        writer = csv.writer(f)
        for row in sorted(fails + succeeds + not_yet, key=itemgetter(1)):
            writer.writerow(row)


def _read_file(io: IO):
    fails = list()
    succeeds = list()
    not_yet = list()
    reader = csv.reader(io.read_file())
    for row in reader:
        status = row[0]
        if status == "F":
            fails.append(row)
        elif status == "S":
            succeeds.append(row)
        else:
            not_yet.append(row)
    return not_yet, succeeds, fails


def _process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args
