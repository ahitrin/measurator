import argparse
import csv
import datetime
import time


def migrate():
    pass


def run_main():
    path = _file_path()
    not_yet, succeeds, fails = _read_file(path)
    # evaluate measurements
    now = datetime.datetime.now()
    delayed = list()
    for status, timestamp, text in not_yet:
        evaluate_time = datetime.datetime(*(time.strptime(timestamp, "%Y-%m-%d %H:%M")[:6]))
        if evaluate_time < now:
            print("Time to evaluate: {}\n Is it true? (Yes/No/Delay)".format(text))
            user_input = input().capitalize()
            if user_input.startswith("Y"):
                status = "S"
                succeeds.append((status, timestamp, text))
            elif user_input.startswith("D"):
                print("When to evaluate (YYYY-mm-dd HH:MM):")
                eval_time = input()
                delayed.append(("N", eval_time, text))
            else:
                status = "F"
                fails.append((status, timestamp, text))
    not_yet = delayed
    # print total statistics
    total_done = len(fails) + len(succeeds)
    if total_done > 0:
        percentage = "%d%%" % (float(100 * len(succeeds)) / float(total_done))
    else:
        percentage = "N/A"
    print("Succesful predictions:", percentage, ", not done yet:", len(not_yet))
    # add another prediction when needed
    print("Add another prediction? Y/N")
    user_input = input()
    if user_input.capitalize().startswith("Y"):
        print("Prediction:")
        prediction = input()
        print("When to evaluate (YYYY-mm-dd HH:MM):")
        eval_time = input()
        not_yet.append(("N", eval_time, prediction))
    # overwrite predictions file
    all_rows = list()
    all_rows.extend(fails)
    all_rows.extend(succeeds)
    all_rows.extend(not_yet)
    with open(path, "wt") as f:
        writer = csv.writer(f)
        for row in all_rows:
            writer.writerow(row)


def _read_file(path):
    fails = list()
    succeeds = list()
    not_yet = list()
    try:
        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                status = row[0]
                if status == "F":
                    fails.append(row)
                elif status == "S":
                    succeeds.append(row)
                else:
                    not_yet.append(row)
    except FileNotFoundError:
        pass
    return not_yet, succeeds, fails


def _file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args.path
