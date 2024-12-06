#!/usr/bin/env python3

import argparse
import os
import sys
import typing
from collections import defaultdict


def part1(rules, updates) -> int:
    befores = defaultdict(list)
    for rule in rules:
        befores[rule[0]].append(rule[1])
    total = sum(
        update[len(update) // 2]
        for update in updates
        if all(
            after_page in befores[this_page]
            for i, this_page in enumerate(update)
            for after_page in update[i + 1 :]
        )
    )
    return total


def part2(rules, updates) -> int:
    # befores = defaultdict(list)
    # afters = defaultdict(list)
    # for rule in rules:
    #    befores[rule[0]].append(rule[1])
    #    afters[rule[1]].append(rule[0])
    # broken = [
    #    update
    #    for update in updates
    #    if not all(
    #        after_page in befores[this_page]
    #        for i, this_page in enumerate(update)
    #        for after_page in update[i + 1 :]
    #    )
    # ]
    # for update in broken:
    #    new_update = update[:1]
    #
    return 0


def parse_data(data: str) -> tuple[list[list[int]], list[list[int]]]:
    rules, updates = data.split("\n\n")
    rules = [[int(r) for r in rule.split("|")] for rule in rules.splitlines()]
    updates = [
        [int(u) for u in update.split(",")] for update in updates.splitlines()
    ]
    return (rules, updates)


def parse_args(args: list[typing.Never]) -> argparse.Namespace:
    me, _ = os.path.splitext(os.path.basename(__file__))
    default_input = os.path.join("data", me + ".txt")
    p = argparse.ArgumentParser(description="Advent of Code 2024")
    p.add_argument(
        "--input",
        default=default_input,
        help=f"input file (default: {default_input})",
    )
    return p.parse_args(args)


def day05(args) -> tuple((int, int)):
    with open(args.input, "r") as f:
        (rules, updates) = parse_data(f.read())

    p1 = part1(rules, updates)
    p2 = part2(rules, updates)
    print(f"part one: {p1}")
    print(f"part two: {p2}")
    return (p1, p2)


if __name__ == "__main__":
    day05(parse_args(sys.argv[1:]))


# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
