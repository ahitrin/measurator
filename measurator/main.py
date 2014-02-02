import argparse, csv, datetime, time

def run_main():
    fails = list()
    succeeds = list()
    not_yet = list()
    path = file_path()
    # read file
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            status = row[0]
            if status == 'F':
                fails.append(row)
            elif status == 'S':
                succeeds.append(row)
            else:
                not_yet.append(row)
    # evaluate measurements
    now = datetime.datetime.now()
    for row in list(not_yet):
        evaluate_time = datetime.datetime(*(time.strptime(row[1], '%Y-%m-%d %H:%M:%S')[:6]))
        if evaluate_time < now:
            print "Time to evaluate:", row[2], "\n Is it true?"
            user_input = raw_input()
            if user_input.capitalize().startswith('Y'):
                row[0] = 'S'
                succeeds.append(row)
            else:
                row[0] = 'F'
                fails .append(row)
            not_yet.remove(row)
    # overwrite predictions file
    all_rows = list()
    all_rows.extend(fails)
    all_rows.extend(succeeds)
    all_rows.extend(not_yet)
    with open(path, 'wt') as f:
        writer = csv.writer(f)
        for row in all_rows:
            writer.writerow(row)
    # print total statistics
    total_done = len(fails) + len(succeeds)
    if total_done > 0:
        percentage = '%d%%' % (float(100 * len(succeeds)) / float(total_done))
    else:
        percentage = 'N/A'
    print "Succesful predictions:", percentage, ", not done yet:", len(not_yet)

def file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args.path
