#!/usr/bin/env python3

import os
import sys
from itertools import combinations
from typing import Never, Self

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data
        self._data = self._parse_data()
        self._w = len(self._data[0])
        self._h = len(self._data)
        # The different types of antennas on the map.
        self._nodes = set(c for r in self._data for c in r if c != ".")
        self._antinodes = [[0 for _ in range(self._w)] for _ in range(self._h)]
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _get_antennas(self: Self) -> dict[str, list[list[int]]]:
        return {
            n: [
                [r, c]
                for r, row in enumerate(self._data)
                for c, _ in enumerate(row)
                if row[c] == n
            ]
            for n in self._nodes
        }

    def _within_bounds(self: Self, node: list[int]) -> bool:
        return all(
            (node[0] >= 0, node[1] >= 0, node[0] < self._h, node[1] < self._w)
        )

    def _get_antinodes(
        self: Self, a: list[int], b: list[int], part: int
    ) -> list[list[int]] | set[tuple[int, int]]:
        distance = [i - j for i, j in zip(a, b)]
        if part == 1:
            return [
                anti
                for anti in [
                    [i + j for i, j in zip(a, distance)],
                    [i - j for i, j in zip(b, distance)],
                ]
                if self._within_bounds(anti)
            ]
        if part == 2:
            # Pick a node and move in one direction until off the map.
            antis = set()
            location = a
            while self._within_bounds(location):
                antis.add(tuple(location))
                location = [i - j for i, j in zip(location, distance)]
            # Now go the other direction.
            location = a
            while self._within_bounds(location):
                antis.add(tuple(location))
                location = [i + j for i, j in zip(location, distance)]
            return antis

    def _part1(self: Self) -> int:
        for _n, locations in self._get_antennas().items():
            for a, b in combinations(locations, 2):
                for anti in self._get_antinodes(a, b, 1):
                    self._antinodes[anti[0]][anti[1]] = 1
        return sum(sum(row) for row in self._antinodes)

    def _part2(self: Self) -> int:
        for locations in self._get_antennas().values():
            for a, b in combinations(locations, 2):
                for anti in self._get_antinodes(a, b, 2):
                    self._antinodes[anti[0]][anti[1]] = 1
        return sum(sum(row) for row in self._antinodes)

    def _parse_data(self: Self) -> list[list[str]]:
        """! Parse the input data into a numpy array.
        @param data: The input map, a string.
        @return: A tuple containing the map and the starting point.
        """
        return [[c for c in r] for r in self._raw_data.splitlines()]


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
