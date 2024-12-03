#!/usr/bin/env python3

import argparse


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
    print(f"part one: safe rows: {safes}")

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
    print(f"part two: safe rows: {safes}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Do something")
    p.add_argument("--input", default="input.txt", help="input file")
    args = p.parse_args()
    main(input_file=args.input)
