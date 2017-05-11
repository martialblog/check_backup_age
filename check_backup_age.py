#!/usr/bin/env python3


import sys
import os
import argparse
import re
import datetime


class EXIT():
    """
    Exit codes from:
    https://docs.icinga.com/latest/en/pluginapi.html
    """

    OK = 0
    WARN = 1
    CRIT = 2
    UNKOWN = 3


def commandline(args):
    """
    Settings for the commandline arguments.
    Returns the parsed arguments.
    """

    parser = argparse.ArgumentParser(description='Checks the last time the offline backup has run')

    parser.add_argument("-p", "--path", required=True,
                        help="Path to offline backup list file")

    parser.add_argument("-w", "--warning",
                        help="Threshold for warnings in days. Default: 2 Days")

    parser.add_argument("-c", "--critical",
                        help="Threshold for criticals in days. Default: 5 Days")

    parser.add_argument("-f", "--format",
                        help="Format of the date in the file. Default: Y-m-d")

    parser.add_argument("-r", "--regex",
                        help="Regular Expression to extract date from file. Default: [0-9]{4}-[0-9]{2}-[0-9]{2}")

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")

    parser.set_defaults(verbose=False,
                        critical=5,
                        warning=2)

    return parser.parse_args(args)


def readfile(path):
    """
    Checks if the file exists at the given path, then reads the file and returns the data.
    """

    if not os.path.exists(path):
        print('No such file {0}'.format(path))
        sys.exit(EXIT.WARN)

    with open(path) as f:
        data = f.read()

    return data


def extract_dates(data, date_format='%Y-%m-%d', date_regex='[0-9]{4}-[0-9]{2}-[0-9]{2}'):
    """
    Extracts dates from a string using regular expressions, then converts the dates to datetime objects and returns a list.
    """

    dates = []

    regex = re.compile(date_regex)
    date_strings = regex.findall(data)

    for date_string in date_strings:
        dates.append(datetime.datetime.strptime(date_string, date_format).date())

    return sorted(dates)


def check_delta(delta, warn, crit):
    """
    Checks the category of the calculated delta (OK, WARN, FAIL) and exits the program accordingly.
    """

    last_backup = 'Last backup was {0} days ago'.format(delta.days)

    isokay = delta.days < warn
    iswarn = delta.days >= warn and delta.days < crit
    iscrit = delta.days >= crit

    if isokay:
        print('OK - ' + last_backup)
        sys.exit(EXIT.OK)
    elif iswarn:
        print('WARN - ' + last_backup)
        sys.exit(EXIT.WARN)
    elif iscrit:
        print('CRIT - ' + last_backup)
        sys.exit(EXIT.CRIT)
    else:
        print('UNKNOWN - Not really sure what is happening')
        sys.exit(EXIT.UNKOWN)


def calculate_delta(dates):
    """
    Calculates how far the gives dates deviate from today's date. Returns a datetime.timedelta object.
    """

    today = datetime.datetime.today().date()
    delta = 0

    for i in range(0, len(dates)):
        delta = -(dates[i] - today)

    # If there are to dates in the file for example
    if not isinstance(delta, datetime.timedelta):
        print('UNKNOWN - Probably error while reading the file')
        sys.exit(EXIT.UNKOWN)

    return delta


def main(args):

    path = str(args.path)
    crit = int(args.critical)
    warn = int(args.warning)

    rdata = readfile(path)
    dates = extract_dates(rdata)
    delta = calculate_delta(dates)

    check_delta(delta=delta, warn=warn, crit=crit)


if __name__ == "__main__":

    args = commandline(sys.argv[1:])
    main(args)
