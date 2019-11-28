import argparse
import csv
import datetime
import time
from operator import itemgetter

TIME_FORMAT = "%Y-%m-%d %H:%M"


class IO:
    """Custom wrapper for all input/output interactions"""
    def write(self, text: str, *args) -> None:
        raise NotImplementedError

    def read(self) -> str:
        raise NotImplementedError

    def read_file(self) -> iter:
        raise NotImplementedError


class ConsoleIO(IO):
    def __init__(self, path) -> None:
        super().__init__()
        self._path = path

    def write(self, text: str, *args):
        print(text, *args)

    def read(self) -> str:
        return input()

    def read_file(self) -> iter:
        try:
            with open(self._path) as f:
                return f.readlines()
        except FileNotFoundError:
            return []


def migrate():
    pass


def run_main():
    path = _file_path()
    run_main_(ConsoleIO(path))


def run_main_(io: IO):
    path = _file_path()
    not_yet, succeeds, fails = _read_file(io)
    # evaluate measurements
    now = datetime.datetime.now()
    delayed = list()
    for status, created, timestamp, text in not_yet:
        evaluate_time = datetime.datetime(*(time.strptime(timestamp, TIME_FORMAT)[:6]))
        if evaluate_time < now:
            io.write("Time to evaluate: {}\n Is it true? (Yes/No/Delay)".format(text))
            user_input = io.read().capitalize()
            if user_input.startswith("Y"):
                status = "S"
                succeeds.append((status, created, timestamp, text))
            elif user_input.startswith("D"):
                io.write("When to evaluate (YYYY-mm-dd HH:MM):")
                eval_time = io.read()
                delayed.append(("N", created, eval_time, text))
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
        not_yet.append(("N", now.strftime(TIME_FORMAT), eval_time, prediction))
    # overwrite predictions file
    with open(path, "wt") as f:
        writer = csv.writer(f)
        for row in sorted(fails + succeeds + not_yet, key=itemgetter(1)):
            writer.writerow(row)


def _read_file(io):
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


def _file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args.path
