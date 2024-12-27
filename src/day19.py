#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import sys
from functools import cache

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._used = []
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._patterns = (
            self._raw_data.splitlines()[0].replace(" ", "").split(",")
        )
        self._designs = self._raw_data.splitlines()[2:]
        self._reduced_patterns = self._reduce_patterns()
        self._max_len = max(len(pat) for pat in self._patterns)
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _reduce_patterns(self: Self) -> dict[str, int]:
        pats = {pat: 0 for pat in self._patterns if len(pat) == 1}
        for pat in sorted(self._patterns, key=lambda x: len(x), reverse=False):
            if len(pat) > 1 and not self._is_doable(pat, pats):
                pats[pat] = 0
        return pats

    def _is_doable(self: Self, design: str, patterns: dict[str, int]) -> bool:
        if len(design) == 0:
            return True
        patterns = {pattern: 0 for pattern in patterns if pattern in design}
        for pattern in patterns:
            if design.startswith(pattern):
                if self._is_doable(design.removeprefix(pattern), patterns):
                    self._used.append(pattern)
                    return True
        return False

    def _part1(self: Self) -> int:
        return sum(
            self._is_doable(design, self._reduced_patterns)
            for design in self._designs
        )

    def _start_finish(self: Self, design: str) -> tuple[str, str]:
        for p_len in range(1, min(self._max_len, len(design)) + 1):
            yield design[:p_len], design[p_len:]

    @cache  # noqa B019
    def _possibles3(self: Self, design: str) -> bool:
        possibilities = int(design in self._patterns)
        for prefix, rest in self._start_finish(design):
            if prefix in self._patterns:
                possibilities += self._possibles3(rest)
        return possibilities

    def _part2(self: Self) -> int:
        return sum(self._possibles3(design) for design in self._designs)


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
