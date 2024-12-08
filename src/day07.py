#!/usr/bin/env python3

import operator
import os
import sys
from itertools import product

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    ops = {
        "+": operator.add,
        "*": operator.mul,
        # "c" for concatenation.
        "c": lambda a, b: int(str(a) + str(b)),
        # '-' : operator.sub,
        # '/' : operator.truediv,
        # '%' : operator.mod,
        # '^' : operator.xor,
    }

    def __init__(self, args):
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data
        self._data = self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self):
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _comp_p1(self, ok_ops):
        for total, values in self._data:
            values_save = values
            for operators in product(ok_ops, repeat=len(values) - 1):
                values = list(reversed(values_save))
                for op in operators:
                    values.append(self.ops[op](values.pop(), values.pop()))
                    if values[-1] > total:
                        continue
                if values[-1] == total:
                    yield total
                    break

    def _part1(self):
        return sum(self._comp_p1("+*"))

    def _part2(self):
        return sum(self._comp_p1("+*c"))

    def _parse_data(self):
        """! Parse the input data into a numpy array.
        @param data: The input map, a string.
        @return: A tuple containing the map and the starting point.
        """
        return [
            [int(a), [int(_) for _ in b.split()]]
            for a, b in (row.split(":") for row in self._raw_data.splitlines())
        ]


if __name__ == "__main__":
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
