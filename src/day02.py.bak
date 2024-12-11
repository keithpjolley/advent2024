#!/usr/bin/env python3

import argparse
import os


def dupes(row):
    """! Return True if there are duplicates in the row."""
    for num in row:
        if row.count(num) > 1:
            return True
    return False


def safe(row):
    """! Return True if the row is "safe." """
    for a, b in zip(row, row[1:]):
        # print(f"abs({a}-{b}): {abs(a-b)} ------------------")
        if abs(a - b) > 3:
            return False
    return True


def issafe(row):
    if dupes(row):
        # Contains duplicates.
        # print(f"dupe: {row}")
        return False
    if row != sorted(row, reverse=False) and row != sorted(row, reverse=True):
        # Not increasing or decreasing.
        # print(f"+-: {row}")
        return False
    return safe(row)


def main(input_file):
    safes = 0
    with open(input_file, "r") as f:
        rows = [[int(col) for col in row.strip().split()] for row in f]
    # part one
    safes = sum(issafe(row) for row in rows)
    yield safes

    # part two, wherein we resort to brute force and ignorance.
    safes = 0
    for row in rows:
        if issafe(row):
            safes += 1
        else:
            for i in range(len(row)):
                this_row = row.copy()
                this_row.pop(i)
                if issafe(this_row):
                    safes += 1
                    break
    yield safes


if __name__ == "__main__":  # pragma: no cover
    me, _ = os.path.splitext(os.path.basename(__file__))
    default_input = os.path.join("data", me + ".txt")
    p = argparse.ArgumentParser(description="Advent of Code 2024")
    p.add_argument(
        "--input",
        default=default_input,
        help=f"input file (default: {default_input})",
    )
    args = p.parse_args()
    p1, p2 = tuple(main(input_file=args.input))
    print(f"part one: safe rows: {p1}")
    print(f"part two: safe rows: {p2}")

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
