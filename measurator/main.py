import argparse, csv, datetime, time

def run_main():
    fails = 0
    succeeds = 0
    not_yet = list()
    path = file_path()
    # read file
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            status = row[0]
            if status == 'F':
                fails = fails + 1
            elif status == 'S':
                succeeds = succeeds + 1
            else:
                not_yet.append(row)
    # evaluate measurements
    now = datetime.datetime.now()
    for row in not_yet:
        evaluate_time = datetime.datetime(*(time.strptime(row[1], '%Y-%m-%d %H:%M:%S')[:6]))
        if evaluate_time < now:
            print "Time to evaluate:", row[2]
    # print total statistics
    total_done = fails + succeeds
    if total_done > 0:
        percentage = '%d%%' % (float(100 * succeeds) / float(total_done))
    else:
        percentage = 'N/A'
    print "Succesful predictions:", percentage, ", not done yet:", len(not_yet)

def file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args.path
