#!/usr/bin/env python3

import argparse
import os


def rot45(data):
    outer = []
    for i in range(len(data)):
        inner = []
        j = i
        k = 0
        while k < len(data[0]) and j >= 0:
            inner.append(data[j][k])
            k += 1
            j -= 1
        outer.append("".join(inner))
    for i in range(1, len(data[0])):
        inner = []
        j = len(data) - 1
        k = i
        while k < len(data[0]) and j >= 0:
            inner.append(data[j][k])
            k += 1
            j -= 1
        outer.append("".join(inner))
    return outer


def rot90(data):
    return ["".join(x) for x in zip(*data[::-1])]


def part1(data):
    # Find `XMAS` in each row forwards:
    search_for = "XMAS"
    # Search forwards then backwards across rows.
    found = sum(row.count(search_for) for row in data)
    found += sum(row.count(search_for[::-1]) for row in data)
    # Rotate the data 90 degrees and do the same.
    data = rot90(data)
    found += sum(row.count(search_for) for row in data)
    found += sum(row.count(search_for[::-1]) for row in data)
    # Now rotate the data 45 degrees and do the same.
    rotated = rot45(data)
    found += sum(row.count(search_for) for row in rotated)
    found += sum(row.count(search_for[::-1]) for row in rotated)
    # And one last time across the other diagonal.
    rotated = rot45(rot90(data))
    found += sum(row.count(search_for) for row in rotated)
    found += sum(row.count(search_for[::-1]) for row in rotated)
    return found


def part2(data):
    # Find 'M M'
    #      ' A '
    #      'S S'
    # Return how many found.
    # Starting at 1,1 to M-1,N-1 look for all "A"s.
    # This is slightly faster than using what's in the "if" as
    # what's returned, that is, letting the boolean be converted
    # to 1 or 0.
    return sum(
        1
        for j in range(1, len(data[0]) - 1)
        for i in range(1, len(data) - 1)
        if data[i][j] == "A"
        and data[i - 1][j - 1] + data[i + 1][j + 1] in ("MS", "SM")
        and data[i - 1][j + 1] + data[i + 1][j - 1] in ("MS", "SM")
    )


def main(input_file):
    with open(input_file, "r") as f:
        data = [row.rstrip("\n") for row in f]
    return (
        part1(data),
        part2(data),
    )


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
    p1, p2 = main(input_file=args.input)
    print(f"part one: XMAS: {p1}")
    print(f"part two: X-MAS: {p2}")


# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
