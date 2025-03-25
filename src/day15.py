#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import sys

import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:
    """! Create a graph with nodes. Create and destroy edges as needed."""

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._graph = nx.DiGraph()
        self.p1 = 10092  # Need to reimpliment p1!
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

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
        print("<" if move_left else ">", end="")
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
        print("^" if move_up else "v", end="")
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
        self._draw()

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
        self._parse_data2()
        self._update_locations()
        for move in self._moves:
            print(move, end="")
            if move in ["<", ">"] and self._move_left_or_right(move == "<"):
                self._update_locations()
            elif move in ["^", "v"] and self._move_up_or_down(move == "^"):
                self._update_locations()
            # self._draw()
            # _ = input()
        print()
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
