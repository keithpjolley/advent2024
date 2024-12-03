#!/usr/bin/env python3

import argparse
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
    distances = [abs(a - b) for a, b in distances]

    # part one
    print(f"part one: distance: {sum(distances)}")

    # part two
    counts1 = Counter(column1)
    counts2 = Counter(column2)
    sums = sum(d1 * c1 * counts2[d1] for d1, c1 in counts1.items())
    print(f"part two: similarty score: {sums}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Do something")
    p.add_argument("--input", default="input.txt", help="input file")
    args = p.parse_args()
    main(input_file=args.input)
