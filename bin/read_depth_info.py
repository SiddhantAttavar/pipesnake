#!/usr/bin/env python3

import sys
import argparse
import csv
from matplotlib import pyplot as plt


def read_depth_statistics(read_depth_statistics, threshold):
    data = []
    with open(read_depth_statistics, 'r') as in_file:
        reader = csv.reader(in_file)
        next(reader)
        for row in reader:
            data += list(map(float, row[1:-3]))

    filtered = sum([i >= threshold for i in data])
    n = len(data)
    data = [i for i in data if i >= threshold]
    print(f'Contigs preserved: {filtered} / {n} ({filtered/n*100:.2f}%)')
    plt.hist(data, bins = range(0, 205, 5))
    plt.xlabel('Avg. read depth')
    plt.ylabel('No. of contigs')
    plt.savefig('read_depth_info.png')
    plt.show()

def parse_args(argv=None):
    """Define and immediately parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate read depth information to decide threshold for PRGs",
        epilog="Example: python read_depth_info.py read_depth_statistics.txt 8"
    )
    parser.add_argument(
        "read_depth_statistics",
        metavar="FILE_IN",
        type=str,
        help="Read depth statistics file"
    )
    parser.add_argument(
        "threshold",
        type=float,
        help="Read depth filter threshold"

    )
    return parser.parse_args(argv)


def main(argv=None):
    """Coordinate argument parsing and program execution."""
    args = parse_args(argv)
    read_depth_statistics(
        args.read_depth_statistics,
        args.threshold
    )


if __name__ == "__main__":
    sys.exit(main())
