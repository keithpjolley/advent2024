#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys
from itertools import pairwise, product

import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._init_keypads()

        self._data = self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        return self._raw_data.split()

    def _init_keypads(self: Self) -> None:
        ## Keypad 0 is the numeric keypad.
        self._numeric_kp = nx.DiGraph()
        # '>' is the direction of the edge.
        for i, j in pairwise(range(1, 11, 3)):
            for a, b in pairwise(range(i, j)):
                a, b = str(a), str(b)
                self._numeric_kp.add_edges_from([(a, b)])
                self._numeric_kp.add_edges_from([(b, a)])
                nx.set_edge_attributes(
                    self._numeric_kp, {(a, b): {"dir": ">"}}
                )
                nx.set_edge_attributes(
                    self._numeric_kp, {(b, a): {"dir": "<"}}
                )
        for i in range(1, 10, 3):
            for j in range(i, i + 3):
                if j < 7:
                    self._numeric_kp.add_edges_from([(str(j), str(j + 3))])
                    nx.set_edge_attributes(
                        self._numeric_kp, {(str(j), str(j + 3)): {"dir": "^"}}
                    )
                if j > 3:
                    self._numeric_kp.add_edges_from([(str(j), str(j - 3))])
                    nx.set_edge_attributes(
                        self._numeric_kp, {(str(j), str(j - 3)): {"dir": "v"}}
                    )
        # Stragglers.
        self._numeric_kp.add_edges_from(
            [
                ("0", "A"),
                ("A", "0"),
                ("0", "2"),
                ("2", "0"),
                ("A", "3"),
                ("3", "A"),
            ]
        )
        nx.set_edge_attributes(
            self._numeric_kp,
            {
                ("0", "A"): {"dir": ">"},
                ("A", "0"): {"dir": "<"},
                ("0", "2"): {"dir": "^"},
                ("2", "0"): {"dir": "v"},
                ("A", "3"): {"dir": "^"},
                ("3", "A"): {"dir": "v"},
            },
        )

        # Keypad 1 is the first directional keypad.
        self._directional_kp = nx.DiGraph()
        pairs = [("^", "A"), ("<", "v"), ("v", ">"), ("^", "v"), ("A", ">")]
        self._directional_kp.add_edges_from(pairs + [(b, a) for a, b in pairs])
        nx.set_edge_attributes(
            self._directional_kp,
            {
                (">", "v"): {"dir": "<"},
                ("A", "^"): {"dir": "<"},
                ("v", "<"): {"dir": "<"},
                ("<", "v"): {"dir": ">"},
                ("^", "A"): {"dir": ">"},
                ("v", ">"): {"dir": ">"},
                (">", "A"): {"dir": "^"},
                ("v", "^"): {"dir": "^"},
                ("A", ">"): {"dir": "v"},
                ("^", "v"): {"dir": "v"},
            },
        )

        # The starting point for each keypad is "A".
        self._current_location = ["A", "A", "A", "A"]

    def _draw(self: Self, graph) -> None:
        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos=pos, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos=pos)

    def _get_directions(
        self: Self, keypresses: set[str], keypad: int
    ) -> set[str]:
        directional_kp_dirs = nx.get_edge_attributes(
            self._directional_kp, "dir"
        )
        combinations = set()
        for combination in keypresses:
            keypresses = [""]
            for to_key in combination:
                paths = nx.all_shortest_paths(
                    self._directional_kp,
                    self._current_location[keypad],
                    to_key,
                )
                keys = [
                    "".join(
                        directional_kp_dirs[pair] for pair in pairwise(path)
                    )
                    + "A"
                    for path in paths
                ]
                keypresses = ["".join(_) for _ in product(keypresses, keys)]
                self._current_location[keypad] = to_key
            for kp in keypresses:
                combinations.add(kp)
        return combinations

    def _part1(self: Self) -> int:
        numeric_kp_dirs = nx.get_edge_attributes(self._numeric_kp, "dir")
        nx.get_edge_attributes(self._directional_kp, "dir")
        total = 0
        # Each combination is a list of keys to press on keypad0.
        for combination in self._data:
            keypresses = [""]
            for to_key in combination:
                paths = nx.all_shortest_paths(
                    self._numeric_kp, self._current_location[0], to_key
                )
                keys = [
                    "".join(numeric_kp_dirs[pair] for pair in pairwise(path))
                    + "A"
                    for path in paths
                ]
                keypresses = ["".join(_) for _ in product(keypresses, keys)]
                self._current_location[0] = to_key

            # `keypresses` is a list of all keypresses needed on keypad1
            # for this combination. It's a list because there are
            # multiple paths to get from one key to another. We don't
            # know yet which one is ultimately the best (shortest) one.
            directional_kps = self._get_directions(set(keypresses), 1)
            directional_kps = self._get_directions(directional_kps, 2)
            total += min(len(kp) for kp in directional_kps) * int(
                combination[:-1]
            )

        return total

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
