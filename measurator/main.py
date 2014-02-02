import argparse, csv

def run_main():
    fails = 0
    succeeds = 0
    not_yet = 0
    path = file_path()
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            status = row[0]
            if status == 'F':
                fails = fails + 1
            elif status == 'S':
                succeeds = succeeds + 1
            else:
                not_yet = not_yet + 1
    total_done = fails + succeeds
    if total_done > 0:
        percentage = '%d%%' % (float(100 * succeeds) / float(total_done))
    else:
        percentage = 'N/A'
    print "Succesful predictions:", percentage, ", not done yet:", not_yet

def file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args.path
