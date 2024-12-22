#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._patterns = (
            self._raw_data.splitlines()[0].replace(" ", "").split(",")
        )
        self._designs = self._raw_data.splitlines()[2:]
        self._reduce_patterns()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _reduce_patterns(self: Self) -> None:
        pats = {
            pat: i for i, pat in enumerate(self._patterns) if len(pat) == 1
        }
        for pat in sorted(self._patterns, key=lambda x: len(x), reverse=False):
            if len(pat) > 1 and not self._is_doable(pat, pats):
                pats[pat] = 0
        self.reduced_patterns = {v: i for i, v in enumerate(pats)}

    def _is_doable(
        self: Self, design: str, patterns: dict[str, int], indent: int = 0
    ) -> bool:
        # print(f"{len(patterns):4d} {indent:4d} design: {design}, patterns: {patterns}")
        if design == "":
            return True
        patterns = {
            pattern: i
            for i, pattern in enumerate(patterns)
            if pattern in design
        }
        for pattern in patterns.keys():
            if design.startswith(pattern):
                if self._is_doable(
                    design[len(pattern) :], patterns, indent + 1
                ):
                    return True
        return False

    def _part1(self: Self) -> int:
        return sum(
            self._is_doable(design, self.reduced_patterns)
            for design in self._designs
        )

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python