#!/usr/bin/env python3

import argparse
import re


def main(input_file):
    with open(input_file, "r") as f:
        data = f.read().replace("\n", "X")

    # part one
    regex_0 = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    mults = sum(int(a) * int(b) for a, b in regex_0.findall(data))
    print(f"part one: sum of mults: {mults}")

    # part two.
    # Remove everything between "don't()" and "do()".
    regex_1 = re.compile(r"don't\(\).*?do\(\)")
    data = regex_1.sub("X", data)
    # Remove everthing after the last "don't()" (there will not be any "do()" after this).
    regex_2 = re.compile(r"don't\(\).*")
    data = regex_2.sub("X", data)

    mults = sum(int(a) * int(b) for a, b in regex_0.findall(data))
    print(f"part two: sum of mults: {mults}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Do something")
    p.add_argument("--input", default="input.txt", help="input file")
    args = p.parse_args()
    main(input_file=args.input)
