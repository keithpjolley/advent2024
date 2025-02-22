#!/usr/bin/env python3

import os
import sys
from collections import defaultdict
from typing import Iterator, Never, Self

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._data = [int(d) for d in self._get_raw.raw_data.strip().split()]
        # self.p1 = self._part1()
        self.p1 = -1
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _secret(self: Self, secret: int) -> int:
        secret = (secret * 64 ^ secret) % 16777216
        secret = (secret // 32 ^ secret) % 16777216
        secret = (secret * 2048 ^ secret) % 16777216
        return secret

    def _twokth_secret(self: Self, secret: int) -> int:
        for _ in range(2000):
            secret = self._secret(secret)
        return secret

    def _part1(self: Self) -> int:
        secret_sum = sum(self._twokth_secret(secret) for secret in self._data)
        return secret_sum

    def _deltas(self: Self, secret: int) -> Iterator[tuple[int, int]]:
        last_ones = secret % 10
        for _ in range(2000):
            secret = self._secret(secret)
            ones = secret % 10
            yield (ones, ones - last_ones)
            last_ones = ones

    def _part2(self: Self) -> int:
        # I am not understanding something fundamental here.
        seq_len = 4
        _bananas = defaultdict(int)
        for seller in [list(self._deltas(secret)) for secret in self._data]:
            for i in range(seq_len, len(seller)):
                seq = tuple(p[1] for p in seller[i - seq_len : i])
                _bananas[seq] += seller[i][0]
                # print(f"t: {seq}, v: {seller[i][0]}")
        return max(_bananas.values())


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
