#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import re
import sys

import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.common import GetRawData

# from timeit import default_timer as timer


class Day:

    VALID_MOVES = {c: i for i, c in enumerate(("<", "^", ">", "v"))}

    def __init__(self: Self, args: list[Never]) -> None:
        self._in_p2 = False
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._maze, self._moves, self._loc = self._parse_data()
        self._graph = nx.DiGraph()
        self._orientation = 0
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> tuple[list[list[str]], str, list[int]]:
        data = self._raw_data
        maze, moves = re.split(r"\n\n", data)
        if self._in_p2:
            maze = (
                maze.replace("#", "##")
                .replace("O", "⇉⇇")
                .replace(".", "..")
                .replace("@", "@.")
            )
        maze = [
            [row[col] for col in range(1, len(row) - 1)]
            for row in maze.replace(".", "0").replace("O", "1").split("\n")
        ][1:-1]

        if self._in_p2:
            # Take the edge(s) off.
            maze = list(map(list, zip(*reversed(maze))))[1:-1]
            maze = list(map(list, reversed(list(zip(*maze)))))

        moves = re.sub(
            r"[^" + "".join(self.VALID_MOVES.keys()) + r"]", "", moves
        )
        loc = [c for r in maze for c in r].index("@")
        x, y = loc % len(maze[0]), loc // len(maze[0])
        # Replace the robot "@" with an empty space "0" to start.
        maze[y][x] = "0"
        return (
            maze,
            moves,
            [x, y],
        )

    def _move(self: Self) -> None:
        """! `_move()` always moves the robot one space to the left.
        The map is rotated prior to calling `_move()` to make this
        "the right move."
        """
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
        first_space = len(row) - list(reversed(row[:-1])).index("0") - 2
        self._maze[self._loc[1]][self._loc[0] - len(row) + first_space] = "1"
        self._maze[self._loc[1]][self._loc[0]] = "0"
        self._loc[0] -= 1

    def _p2rotate(self: Self, rotation: int) -> None:
        def swapper(*swaps: tuple[str, str]) -> None:
            # Swap old_x for new_x
            ret_swaps = (("u", "⇈"), ("l", "⇇"), ("d", "⇊"), ("r", "⇉"))
            for ov, nv in swaps + ret_swaps:
                self._maze = [
                    [nv if c == ov else c for c in r] for r in self._maze
                ]

        # Have to use intermediate values.
        # a -> tmp, b -> a, tmp -> b.
        match rotation:
            case 0 | 360:
                pass
            case 90:
                swapper(("⇉", "d"), ("⇊", "l"), ("⇈", "r"), ("⇇", "u"))
            case 180:
                swapper(("⇊", "u"), ("⇉", "l"), ("⇈", "d"), ("⇇", "r"))
            case 270:
                swapper(("⇉", "u"), ("⇊", "r"), ("⇈", "l"), ("⇇", "d"))
            case _:
                raise ValueError(f"Unsupported rotation: {rotation}.")

    def _rotate(self: Self, direction: int) -> None:

        while direction < 0:
            direction += 360
        while direction >= 360:
            direction -= 360

        if direction == 0:
            return

        width, height = len(self._maze[0]) - 1, len(self._maze) - 1
        x, y = self._loc
        if self._in_p2:
            self._p2rotate(direction)

        match direction:
            case 90:
                self._maze = list(map(list, zip(*reversed(self._maze))))
                self._loc = [height - y, x]
                self._orientation += 1
            case 270:
                self._maze = list(map(list, reversed(list(zip(*self._maze)))))
                self._loc = [y, width - x]
                self._orientation -= 1
            case 180:
                for i in range(len(self._maze)):
                    self._maze[i] = list(reversed(self._maze[i]))
                self._maze = list(reversed(self._maze))
                self._loc = [width - x, height - y]
                self._orientation += 2
            case _:
                # For 0 or 360 degree rotation.
                pass

    def _print(self: Self) -> None:
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
        for move in self._moves:
            self._rotate(
                -90 * (self.VALID_MOVES[move] - self.VALID_MOVES[last_move])
            )
            self._move()
            last_move = move
        # Return the maze to the upright and locked position.
        # Done like this because a) all lines get tested. b) only
        # happens once.
        while (self._orientation % 4) != 0:
            self._rotate(90)
        self._orientation = 0
        return sum(
            100 * (i + 1) + 1 + j
            for i, row in enumerate(self._maze)
            for j, col in enumerate(row)
            if col == "1"
        )

    def _parse_data2(self: Self) -> None:
        data = (
            self._raw_data.replace("#", "##")
            .replace("O", "<>")
            .replace(".", "..")
            .replace("@", "@.")
        )
        grid, moves = data.split("\n\n")

        self._moves = moves.replace("\n", "")

        grid = [row[1:-1] for row in grid.split("\n")]
        for j, row in enumerate(grid):
            for i, col in enumerate(row):
                if col == "<":
                    self._graph.add_node(
                        f"box_{i}.{j}", type="box", x=i, x1=i + 1, y=j
                    )
                if col == "#":
                    self._graph.add_node(
                        f"wall_{i}.{j}", type="wall", x=i, y=j
                    )
                if col == "@":
                    self._graph.add_node("robot", type="robot", x=i, y=j)

    def _draw(self: Self) -> None:
        boxes = nx.Graph()
        robot = nx.Graph()
        walls = nx.Graph()
        for node, data in self._graph.nodes(data=True):
            if data["type"] == "box":
                boxes.add_node(f"fake_{node}_a", x=data["x"], y=-data["y"])
                boxes.add_node(f"fake_{node}_b", x=data["x1"], y=-data["y"])
            elif data["type"] == "robot":
                robot.add_node(node, x=data["x"], y=-data["y"])
            elif data["type"] == "wall":
                walls.add_node(node, x=data["x"], y=-data["y"])

        # Shape is one of: 'so^>v<dph8'
        # Draw the boxes.
        pos = {n: [d["x"], d["y"]] for n, d in boxes.nodes(data=True)}
        nx.draw_networkx_nodes(
            boxes, pos=pos, node_color="blue", node_shape="s"
        )

        # Draw the walls.
        pos = {
            n: [d["x"], d["y"]] for n, d in walls.nodes(data=True) if "x" in d
        }
        nx.draw_networkx_nodes(
            walls, pos=pos, node_color="grey", node_shape="s"
        )

        # Draw the robot.
        pos = {n: [d["x"], d["y"]] for n, d in robot.nodes(data=True)}
        nx.draw_networkx_nodes(
            robot, pos=pos, node_color="orange", node_shape="^"
        )

        # Draw the edges.
        pos = {
            node: [
                self._graph.nodes()[node]["x"],
                -self._graph.nodes()[node]["y"],
            ]
            for node in set(
                n for n0, n1 in self._graph.edges for n in (n0, n1)
            )
        }
        nx.draw_networkx_edges(self._graph, pos)

        # Draw labels on anything with an edge
        g = self._graph.copy()
        g.remove_nodes_from(
            [
                node
                for node in self._graph.nodes
                if node
                not in set(n for n0, n1 in self._graph.edges for n in (n0, n1))
            ]
        )
        nx.draw_networkx_labels(
            g,
            pos={
                node: [g.nodes()[node]["x"], -g.nodes()[node]["y"]]
                for node in g.nodes
            },
        )

    def _move_left_or_right(self: Self, move_left: bool) -> None:
        """! No graph theory here kids. :/"""
        col, row = (
            self._graph.nodes()["robot"]["x"],
            self._graph.nodes()["robot"]["y"],
        )
        # Iterate over each position to the left or right until we hit
        # either a wall (can't move) or an empty space (can move).
        # Get nodes in this row and to the left of the robot:
        if move_left:
            this_row = ["empty"] * col
            shift = 0
        else:
            grid_width = max(
                d["x"] for _, d in self._graph.nodes(data=True) if "x" in d
            )
            shift = col + 1
            this_row = ["empty"] * (grid_width - col)

        for node, data in self._graph.nodes(data=True):
            if data["y"] != row:
                continue
            if (move_left and data["x"] >= col) or (
                not move_left and data["x"] <= col
            ):
                continue
            this_row[data["x"] - shift] = node
            if "x1" in data:
                this_row[data["x1"] - shift] = data["type"]

        boxes_to_move = []
        if move_left:
            this_row = reversed(this_row)
        for item in this_row:
            if item.startswith("wall"):
                # Can't move. Do nothing.
                return
            if item == "box":
                # Filler item, ignore.
                continue
            if item.startswith("box"):
                boxes_to_move.append(item)
                continue
            if item == "empty":
                # We can move!
                # Move the boxes...
                direction = -1 if move_left else 1
                for box in boxes_to_move:
                    self._graph.nodes()[box]["x"] += direction
                    self._graph.nodes()[box]["x1"] += direction
                # Move the robot
                self._graph.nodes()["robot"]["x"] += direction
                self._update_locations()
                return

    def _move_up_or_down(self: Self, move_up: bool) -> None:
        direction = 1 if move_up else -1
        self._graph.remove_edges_from(list(self._graph.edges))
        for (x, y), node in self._locations.items():
            if (
                node.startswith("wall")
                or (move_up and y > self._graph.nodes()["robot"]["y"])
                or (not move_up and y < self._graph.nodes()["robot"]["y"])
            ):
                continue
            if (x, y - direction) in self._locations:
                self._graph.add_edge(node, self._locations[(x, y - direction)])
            if (
                self._graph.nodes()[node]["type"] == "box"
                and (self._graph.nodes()[node]["x1"], y - direction)
                in self._locations
            ):
                self._graph.add_edge(
                    node,
                    self._locations[
                        (self._graph.nodes()[node]["x1"], y - direction)
                    ],
                )
            if (
                (x + 1, y) in self._locations
                and self._locations[(x + 1, y)] == node
                and (x + 1, y - direction) in self._locations
            ):
                self._graph.add_edge(
                    node, self._locations[(x + 1, y - direction)]
                )

        descendants = nx.descendants(self._graph, "robot")
        if "wall" in [
            self._graph.nodes()[node]["type"] for node in descendants
        ]:
            # We are blocked. Can't move.
            return
        for node in descendants:
            self._graph.nodes()[node]["y"] -= direction
        self._graph.nodes()["robot"]["y"] -= direction
        self._update_locations()

    def _update_locations(self: Self) -> None:
        self._graph.remove_edges_from(list(self._graph.edges))
        self._locations = {
            (d["x"], d["y"]): n for n, d in self._graph.nodes(data=True)
        }
        self._locations |= {
            (d["x1"], d["y"]): n
            for n, d in self._graph.nodes(data=True)
            if "x1" in d
        }

    def _part2(self: Self) -> int:
        # begin = timer()
        self._parse_data2()
        self._update_locations()
        # n = 1
        for move in self._moves:
            # print(
            #     f"{move} - {n:5d} of {len(self._moves)}, {(n/len(self._moves)):7.2%}",
            #     end="",
            # )
            # start = timer()
            if (
                move in ["<", ">"] and self._move_left_or_right(move == "<")
            ) or (move in ["^", "v"] and self._move_up_or_down(move == "^")):
                self._update_locations()
            # end = timer()
            # print(
            #     f", step: {end - start:.5f}s, total: {end - begin:.2f}s",
            #     flush=True,
            # )
            # n += 1
        self._draw()
        return sum(
            [
                100 * d["y"] + d["x"] + 1
                for n, d in self._graph.nodes(data=True)
                if d["type"] == "box"
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
