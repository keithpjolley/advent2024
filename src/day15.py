#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._maze, self._moves, self._loc = self._parse_data()
        self._orientation = 0
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(
        self: Self, data: str | None = None
    ) -> tuple[list[list[str]], str, list[int]]:
        if data is None:
            data = self._raw_data
        maze, moves = re.split(r"\n\n", data)
        maze = [
            [row[col] for col in range(1, len(row) - 1)]
            for row in maze.replace(".", "0").replace("O", "1").split("\n")
        ][1:-1]
        moves = moves.replace("\n", "")
        loc = [c for r in maze for c in r].index("@")
        x, y = loc % len(maze[0]), loc // len(maze[0])
        maze[y][x] = "0"
        return (
            maze,
            moves,
            [x, y],
        )

    def _move(self: Self) -> None:
        row = self._maze[self._loc[1]][: self._loc[0]]
        if len(row) == 0 or row[-1] == "#":
            # Up against a wall. Can't move.
            return
        if row[-1] == "0":
            # No box to move, no wall. Just move "left" and go.
            self._maze[self._loc[1]][self._loc[0]] = "0"
            self._loc[0] -= 1
            return
        try:
            # Find the rightmost wall in this row.
            wall = len(row) - list(reversed(row)).index("#")
            row = row[wall:]
        except ValueError:
            pass
        if "0" not in row:
            # No empty space to move to.
            return
        first_space = len(row[:-1]) - list(reversed(row[:-1])).index("0") - 1
        self._maze[self._loc[1]][self._loc[0] - len(row) + first_space] = "1"
        self._maze[self._loc[1]][self._loc[0]] = "0"
        self._loc[0] -= 1

    def _rotate(self: Self, direction: int) -> None:
        width, height = len(self._maze[0]) - 1, len(self._maze) - 1
        x, y = self._loc
        if direction == 90:
            self._maze = list(map(list, zip(*reversed(self._maze))))
            self._loc = [height - y, x]
            self._orientation += 1
            return
        if direction == -90:
            self._maze = list(map(list, reversed(list(zip(*self._maze)))))
            self._loc = [y, width - x]
            self._orientation -= 1
            return
        if direction == 180:
            for i in range(len(self._maze)):
                self._maze[i] = list(reversed(self._maze[i]))
            self._maze = list(reversed(self._maze))
            self._loc = [width - x, height - y]
            self._orientation += 2

    def _print_maze(self: Self) -> None:
        for j, row in enumerate(self._maze):
            for i, char in enumerate(row):
                if [i, j] == self._loc:
                    fmt = f"{1};{33};{40}"
                    char = "@"
                elif char == "0":
                    fmt = "1;30"
                    char = "."
                elif char == "#":
                    fmt = "0;31"
                elif char == "1":
                    char = "O"
                    fmt = "0;37"
                else:
                    fmt = "0;32"
                print(f"\x1b[{fmt};40m{char}\x1b[0m", end="")
            if j == 0:
                print(
                    f"  loc: {self._loc}, orientation: {self._orientation}",
                    end="",
                )
            print()

    def _part1(self: Self) -> int:
        last_move = "<"
        moves = {"<": 0, "^": 1, ">": 2, "v": 3}
        for move in self._moves:
            dist = moves[move] - moves[last_move]
            if dist < 0:
                dist += 4
            if dist == 1:
                self._rotate(-90)
            elif dist == 2:
                self._rotate(180)
            if dist == 3:
                self._rotate(90)
            self._move()
            last_move = move
        # Return the maze to the upright and locked position.
        # Done like this because a) all lines get tested. b) only
        # happens once.
        while (self._orientation % 4) != 0:
            self._rotate(90)
        self._orientation = 0
        self._print_maze()
        return sum(
            100 * (i + 1) + 1 + j
            for i, row in enumerate(self._maze)
            for j, col in enumerate(row)
            if col == "1"
        )

    def _part2(self: Self) -> int:
        print("Part 2")
        data = (
            self._raw_data.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )
        self._maze, self._moves, self._loc = self._parse_data(data)
        self._print_maze()
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
