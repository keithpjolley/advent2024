#!/usr/bin/env python3

import argparse
import os
import re
from typing import Any, Generator


def main(input_file: str) -> Generator[int, Any, Any]:
    with open(input_file, "r") as f:
        data = f.read().replace("\n", "X")

    # part one
    regex_0 = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    mults = sum(int(a) * int(b) for a, b in regex_0.findall(data))
    yield mults

    # part two.
    # Remove everything between "don't()" and "do()".
    regex_1 = re.compile(r"don't\(\).*?do\(\)")
    data = regex_1.sub("X", data)
    # Remove everthing after the last "don't()" (there will not be any "do()" after this).
    regex_2 = re.compile(r"don't\(\).*")
    data = regex_2.sub("X", data)

    mults = sum(int(a) * int(b) for a, b in regex_0.findall(data))
    yield mults


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
    print(f"part one: sum of mults: {p1}")
    print(f"part two: sum of mults: {p2}")


# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
