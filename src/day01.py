#!/usr/bin/env python3

import argparse
import os
from collections import Counter


def main(input_file):
    column1 = []
    column2 = []
    with open(input_file, "r") as f:
        for line in f:
            a, b = line.strip().split()
            column1.append(int(a))
            column2.append(int(b))
    distances = zip(sorted(column1), sorted(column2))
    distances = sum(abs(a - b) for a, b in distances)

    # part one
    print(f"part one: distance: {distances}")

    # part two
    counts1 = Counter(column1)
    counts2 = Counter(column2)
    sums = sum(d1 * c1 * counts2[d1] for d1, c1 in counts1.items())
    print(f"part two: similarty score: {sums}")
    return (distances, sums)


if __name__ == "__main__":
    me, _ = os.path.splitext(os.path.basename(__file__))
    default_input = os.path.join("data", me + ".txt")
    p = argparse.ArgumentParser(description="Advent of Code 2024")
    p.add_argument(
        "--input",
        default=default_input,
        help=f"input file (default: {default_input})",
    )
    args = p.parse_args()
    main(input_file=args.input)

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
