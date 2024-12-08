#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class day06:

    _empty_space = 0
    _traversed = 1
    _blockage = 2
    _current_location = 3

    def __init__(self, args):
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data
        self._data = self._parse_data()
        self._start = self._location()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self):
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"Day 6: part 1: {self.p1}\nDay 6: part 2: {self.p2}"
        return message

    def _part1(self):
        row, col = self._location()
        barriers = np.where(self._data[row][col:] == self._blockage)[0]
        if len(barriers) == 0:
            # No barriers - go to end of row.
            self._data[row][col:] = np.full(
                len(self._data[row][col:]), self._traversed
            )
            self._data_p1 = self._data.copy()
            return np.count_nonzero(self._data == self._traversed)
        barrier = barriers[0]
        # Fill the path from the current location to the barrier.
        self._data[row][col : col + barrier] = np.full(
            barrier, self._traversed
        )
        # Mark our current location.
        self._data[row][col + barrier - 1] = self._current_location
        # Turn right (rotate map -90 degrees) so we are facing East.
        self._data = np.rot90(self._data, k=1)
        return self._part1()

    def _part2(self):
        # Start from the beginning.
        data_org = self._parse_data()
        blocks = 0
        for point in np.argwhere(data_org != self._current_location):
            self._data = data_org.copy()
            self._data[point[0]][point[1]] = self._blockage
            try:
                self._part1()
            except RecursionError:
                # Hi! This is not elegant!
                blocks += 1
        return blocks

    def _location(self):
        """! Find the starting location of the guard.
        @return: The location of the guard.
        """
        return np.argwhere(self._data == self._current_location)[0]

    def _parse_data(self):
        """! Parse the input data into a numpy array.
        @param data: The input map, a string.
        @return: A tuple containing the map and the starting point.
        """
        data = np.array(
            [
                [
                    (
                        self._empty_space
                        if _ == "."
                        else (
                            self._blockage
                            if _ == "#"
                            else self._current_location
                        )
                    )
                    for _ in row
                ]
                for row in self._raw_data.split()
            ]
        )
        # Always have the guard facing East.
        if "^" in self._raw_data:
            # North
            data = np.rot90(data, k=-1)
        elif ">" in self._raw_data:
            # East
            pass
        elif "v" in self._raw_data:
            # South
            data = np.rot90(data, k=1)
        elif "<" in self._raw_data:
            # West
            data = np.rot90(data, k=2)
        else:
            raise ValueError("Invalid input data")
        return data


if __name__ == "__main__":
    print(day06(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
